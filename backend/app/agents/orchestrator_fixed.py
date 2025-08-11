"""
Multi-agent orchestrator using LangGraph with supervisor pattern (Updated for 2025).

Based on LangGraph latest best practices for multi-agent systems.
"""

import logging
from typing import Dict, Any, List, TypedDict, Annotated, Literal, Optional
from datetime import datetime
import json

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.agents.researcher import ResearcherAgent
from app.agents.writer import WriterAgent
from app.agents.analyst import AnalystAgent
from app.models.message import AgentRole, Message
from app.models.task import Task, TaskStatus
from app.websocket.manager import notify_task_started, notify_task_completed, notify_error, notify_agent_message
from app.config import settings

logger = logging.getLogger(__name__)


# Define state schema using TypedDict for type safety
class AgentState(MessagesState):
    """State schema for multi-agent collaboration."""
    task_id: str
    task_title: str
    task_description: str
    next_agent: Optional[str]
    research_output: Optional[Dict[str, Any]]
    writer_output: Optional[Dict[str, Any]]
    analyst_output: Optional[Dict[str, Any]]
    final_deliverable: Optional[str]
    error: Optional[str]


class MultiAgentOrchestrator:
    """
    Orchestrates multi-agent collaboration using LangGraph supervisor pattern.
    
    Implements the latest LangGraph patterns including:
    - Supervisor-based coordination with Command objects
    - Dynamic control flow with proper routing
    - Proper state management
    - Async support throughout
    """
    
    def __init__(self):
        # Initialize agents
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.analyst = AnalystAgent()
        
        # Initialize supervisor LLM with proper error handling
        try:
            self.supervisor_llm = ChatOpenAI(
                model="gpt-4o-mini",  # Use a more available model
                temperature=0.3,
                openai_api_key=settings.openai_api_key
            )
        except Exception as e:
            logger.error(f"Failed to initialize supervisor LLM: {e}")
            # Fallback to gpt-3.5-turbo if gpt-4 not available
            self.supervisor_llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.3,
                openai_api_key=settings.openai_api_key
            )
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the multi-agent workflow using LangGraph with Command pattern."""
        # Create workflow with our state schema
        builder = StateGraph(AgentState)
        
        # Add nodes for each agent and supervisor
        builder.add_node("supervisor", self._supervisor_node)
        builder.add_node("researcher", self._researcher_node)
        builder.add_node("writer", self._writer_node)
        builder.add_node("analyst", self._analyst_node)
        builder.add_node("finalize", self._finalize_node)
        
        # Set entry point to supervisor
        builder.add_edge(START, "supervisor")
        
        # Add edges from agents back to supervisor
        builder.add_edge("researcher", "supervisor")
        builder.add_edge("writer", "supervisor")
        builder.add_edge("analyst", "supervisor")
        builder.add_edge("finalize", END)
        
        # Compile the workflow
        return builder.compile()
    
    async def _supervisor_node(self, state: AgentState) -> Command[Literal["researcher", "writer", "analyst", "finalize", "__end__"]]:
        """
        Supervisor node that coordinates agent activities using Command pattern.
        
        Uses LLM to decide next agent based on current state.
        """
        try:
            # Build context for supervisor decision
            context = self._build_supervisor_context(state)
            
            # System message for supervisor
            system_msg = SystemMessage(content="""You are a supervisor coordinating a multi-agent research and writing task.

Available agents:
- researcher: Gathers information from web sources (call FIRST if no research done)
- writer: Creates content from research findings (call AFTER researcher)
- analyst: Reviews and refines content for quality (call AFTER writer)

Decision rules:
1. If no research has been done yet, respond with: researcher
2. If research is done but no content written, respond with: writer
3. If content is written but not reviewed, respond with: analyst
4. If content has been reviewed and refined, respond with: finalize
5. If an error occurred, respond with: end

Respond with ONLY the agent name or action (one word).""")
            
            # Create user message with task and context
            user_msg = HumanMessage(content=f"""Task: {state['task_title']}
Description: {state['task_description']}

Current Progress:
{context}

Which agent should work next? Respond with only: researcher, writer, analyst, finalize, or end""")
            
            # Get supervisor decision
            response = await self.supervisor_llm.ainvoke([system_msg, user_msg])
            
            next_action = response.content.strip().lower()
            
            # Validate response
            valid_actions = ["researcher", "writer", "analyst", "finalize", "end"]
            if next_action not in valid_actions:
                # Default to researcher if invalid response
                logger.warning(f"Invalid supervisor response: {next_action}, defaulting to researcher")
                next_action = "researcher" if not state.get("research_output") else "finalize"
            
            logger.info(f"Supervisor decision for task {state['task_id']}: {next_action}")
            
            # Send notification about agent assignment
            await notify_agent_message(state['task_id'], {
                "agent_role": "supervisor",
                "content": f"Assigning task to {next_action}",
                "timestamp": datetime.now().isoformat()
            })
            
            # Return Command with goto
            if next_action == "end":
                return Command(goto="__end__")
            else:
                return Command(goto=next_action)
                
        except Exception as e:
            logger.error(f"Supervisor error: {str(e)}")
            return Command(goto="finalize", update={"error": str(e)})
    
    def _build_supervisor_context(self, state: AgentState) -> str:
        """Build context summary for supervisor decision making."""
        context_parts = []
        
        if state.get("research_output"):
            sources = state['research_output'].get('sources_found', 0)
            context_parts.append(f"✅ Research completed: {sources} sources found")
        else:
            context_parts.append("⏳ Research not yet started")
            
        if state.get("writer_output"):
            context_parts.append("✅ Content drafted by writer")
        else:
            context_parts.append("⏳ Content not yet written")
            
        if state.get("analyst_output"):
            context_parts.append("✅ Content reviewed and refined by analyst")
        else:
            context_parts.append("⏳ Content not yet reviewed")
            
        if state.get("error"):
            context_parts.append(f"❌ Error occurred: {state['error']}")
        
        return "\n".join(context_parts)
    
    async def _researcher_node(self, state: AgentState) -> Command[Literal["supervisor"]]:
        """Execute researcher agent with Command pattern."""
        try:
            logger.info(f"Researcher starting for task {state['task_id']}")
            
            context = {
                "title": state["task_title"],
                "description": state["task_description"]
            }
            
            # Notify that researcher is working
            await notify_agent_message(state['task_id'], {
                "agent_role": "researcher",
                "content": "Starting research on the topic...",
                "timestamp": datetime.now().isoformat()
            })
            
            result = await self.researcher.process(
                state["task_id"],
                context
            )
            
            # Send research summary
            await notify_agent_message(state['task_id'], {
                "agent_role": "researcher",
                "content": f"Research completed. Found {result.get('sources_found', 0)} sources. Key findings: {result.get('synthesis', '')[:200]}...",
                "timestamp": datetime.now().isoformat()
            })
            
            # Message already saved by agent's send_message method
            
            # Return Command with state update
            return Command(
                goto="supervisor",
                update={
                    "research_output": result,
                    "messages": state.get("messages", []) + [
                        AIMessage(
                            content=f"Research completed with {result.get('sources_found', 0)} sources",
                            name="researcher"
                        )
                    ]
                }
            )
            
        except Exception as e:
            logger.error(f"Researcher error: {str(e)}")
            return Command(
                goto="supervisor",
                update={
                    "error": f"Researcher error: {str(e)}",
                    "messages": state.get("messages", []) + [
                        AIMessage(
                            content=f"Error in research: {str(e)}",
                            name="researcher"
                        )
                    ]
                }
            )
    
    async def _writer_node(self, state: AgentState) -> Command[Literal["supervisor"]]:
        """Execute writer agent with Command pattern."""
        try:
            logger.info(f"Writer starting for task {state['task_id']}")
            
            context = {
                "title": state["task_title"],
                "description": state["task_description"],
                "research_output": state.get("research_output", {})
            }
            
            # Notify that writer is working
            await notify_agent_message(state['task_id'], {
                "agent_role": "writer",
                "content": "Drafting content based on research...",
                "timestamp": datetime.now().isoformat()
            })
            
            result = await self.writer.process(
                state["task_id"],
                context
            )
            
            # Send writing update
            await notify_agent_message(state['task_id'], {
                "agent_role": "writer",
                "content": f"Content draft completed. Length: {len(result.get('content', ''))} characters",
                "timestamp": datetime.now().isoformat()
            })
            
            # Message already saved by agent's send_message method
            
            return Command(
                goto="supervisor",
                update={
                    "writer_output": result,
                    "messages": state.get("messages", []) + [
                        AIMessage(
                            content="Content drafted successfully",
                            name="writer"
                        )
                    ]
                }
            )
            
        except Exception as e:
            logger.error(f"Writer error: {str(e)}")
            return Command(
                goto="supervisor",
                update={
                    "error": f"Writer error: {str(e)}",
                    "messages": state.get("messages", []) + [
                        AIMessage(
                            content=f"Error in writing: {str(e)}",
                            name="writer"
                        )
                    ]
                }
            )
    
    async def _analyst_node(self, state: AgentState) -> Command[Literal["supervisor"]]:
        """Execute analyst agent with Command pattern."""
        try:
            logger.info(f"Analyst starting for task {state['task_id']}")
            
            context = {
                "title": state["task_title"],
                "description": state["task_description"],
                "research_output": state.get("research_output", {}),
                "writer_output": state.get("writer_output", {})
            }
            
            # Notify that analyst is working
            await notify_agent_message(state['task_id'], {
                "agent_role": "analyst",
                "content": "Reviewing and refining content...",
                "timestamp": datetime.now().isoformat()
            })
            
            result = await self.analyst.process(
                state["task_id"],
                context
            )
            
            # Send analyst update
            await notify_agent_message(state['task_id'], {
                "agent_role": "analyst",
                "content": "Content reviewed and refined. Final deliverable ready.",
                "timestamp": datetime.now().isoformat()
            })
            
            # Message already saved by agent's send_message method
            
            return Command(
                goto="supervisor",
                update={
                    "analyst_output": result,
                    "final_deliverable": result.get("deliverable", ""),
                    "messages": state.get("messages", []) + [
                        AIMessage(
                            content="Content reviewed and refined",
                            name="analyst"
                        )
                    ]
                }
            )
            
        except Exception as e:
            logger.error(f"Analyst error: {str(e)}")
            return Command(
                goto="supervisor",
                update={
                    "error": f"Analyst error: {str(e)}",
                    "messages": state.get("messages", []) + [
                        AIMessage(
                            content=f"Error in analysis: {str(e)}",
                            name="analyst"
                        )
                    ]
                }
            )
    
    async def _finalize_node(self, state: AgentState) -> Dict[str, Any]:
        """Finalize the task with the deliverable."""
        deliverable = state.get("final_deliverable", "")
        
        if not deliverable and state.get("writer_output"):
            # Fallback to writer output if analyst didn't produce deliverable
            deliverable = state["writer_output"].get("content", "")
        
        logger.info(f"Finalizing task {state['task_id']} with deliverable")
        
        # Send completion notification
        await notify_agent_message(state['task_id'], {
            "agent_role": "supervisor",
            "content": "Task completed successfully!",
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "final_deliverable": deliverable,
            "messages": state.get("messages", []) + [
                AIMessage(
                    content="Task completed successfully!",
                    name="supervisor"
                )
            ]
        }
    
    async def process_task(self, task: Task, db_session) -> str:
        """
        Process a task through the multi-agent workflow.
        
        Args:
            task: Task to process
            db_session: Database session for persistence
            
        Returns:
            Final deliverable content
        """
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=f"Process this task: {task.title}\n\nDescription: {task.description}")],
            "task_id": task.id,
            "task_title": task.title,
            "task_description": task.description,
            "next_agent": None,
            "research_output": None,
            "writer_output": None,
            "analyst_output": None,
            "final_deliverable": None,
            "error": None
        }
        
        # Store db session for message saving
        self._db_session = db_session
        
        try:
            # Notify task started
            await notify_task_started(task.id, {
                "id": task.id,
                "title": task.title,
                "description": task.description
            })
            
            # Update task status
            task.status = TaskStatus.IN_PROGRESS
            db_session.commit()
            
            logger.info(f"Starting workflow for task {task.id}")
            
            # Execute workflow with async iteration
            final_state = await self.workflow.ainvoke(initial_state)
            
            # Extract deliverable
            deliverable = final_state.get("final_deliverable", "")
            
            if deliverable:
                # Update task with deliverable
                task.deliverable = deliverable
                task.status = TaskStatus.COMPLETED
                db_session.commit()
                
                # Notify completion
                await notify_task_completed(task.id, deliverable)
                
                logger.info(f"Task {task.id} completed successfully")
                return deliverable
            else:
                # Handle failure
                error_msg = final_state.get("error", "No deliverable produced")
                task.status = TaskStatus.FAILED
                db_session.commit()
                
                await notify_error(task.id, error_msg)
                
                logger.error(f"Task {task.id} failed: {error_msg}")
                return f"Task failed: {error_msg}"
                
        except Exception as e:
            logger.error(f"Orchestrator error for task {task.id}: {str(e)}")
            
            task.status = TaskStatus.FAILED
            db_session.commit()
            
            await notify_error(task.id, str(e))
            
            return f"Task processing error: {str(e)}"
    
    async def _save_agent_message(self, task_id: str, agent_role: AgentRole, content: str):
        """Save agent message to database."""
        try:
            if hasattr(self, '_db_session'):
                message = Message(
                    task_id=task_id,
                    agent_role=agent_role,
                    content=content
                )
                self._db_session.add(message)
                self._db_session.commit()
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")


# Global orchestrator instance
_orchestrator = None


def get_orchestrator() -> MultiAgentOrchestrator:
    """Get or create the global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = MultiAgentOrchestrator()
    return _orchestrator