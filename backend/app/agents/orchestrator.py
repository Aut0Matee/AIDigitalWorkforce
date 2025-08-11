"""
Multi-agent orchestrator using LangGraph with supervisor pattern.

Based on LangGraph 2025 best practices for multi-agent systems.
"""

import logging
from typing import Dict, Any, List, TypedDict, Annotated, Sequence, Optional
from datetime import datetime
import json

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI

from app.agents.researcher import ResearcherAgent
from app.agents.writer import WriterAgent
from app.agents.analyst import AnalystAgent
from app.models.message import AgentRole, Message
from app.models.task import Task, TaskStatus
from app.websocket.manager import notify_task_started, notify_task_completed, notify_error
from app.config import settings

logger = logging.getLogger(__name__)


# Define state schema using TypedDict for type safety
class AgentState(TypedDict):
    """State schema for multi-agent collaboration."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
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
    - Supervisor-based coordination
    - Dynamic control flow with handoffs
    - Proper state management
    - Streaming support
    """
    
    def __init__(self):
        # Initialize agents
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.analyst = AnalystAgent()
        
        # Initialize supervisor LLM
        self.supervisor_llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.3,
            openai_api_key=settings.openai_api_key
        )
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the multi-agent workflow using LangGraph."""
        # Create workflow with our state schema
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent and supervisor
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("writer", self._writer_node)
        workflow.add_node("analyst", self._analyst_node)
        workflow.add_node("finalize", self._finalize_node)
        
        # Set entry point to supervisor
        workflow.set_entry_point("supervisor")
        
        # Add conditional edges based on supervisor decisions
        workflow.add_conditional_edges(
            "supervisor",
            self._route_supervisor,
            {
                "researcher": "researcher",
                "writer": "writer",
                "analyst": "analyst",
                "finalize": "finalize",
                "end": END
            }
        )
        
        # Add edges from agents back to supervisor
        workflow.add_edge("researcher", "supervisor")
        workflow.add_edge("writer", "supervisor")
        workflow.add_edge("analyst", "supervisor")
        workflow.add_edge("finalize", END)
        
        # Compile the workflow
        return workflow.compile()
    
    async def _supervisor_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Supervisor node that coordinates agent activities.
        
        Uses LLM to decide next agent based on current state.
        """
        # Build context for supervisor decision
        context = self._build_supervisor_context(state)
        
        # Supervisor prompt
        supervisor_prompt = f"""You are a supervisor coordinating a multi-agent research and writing task.

Task: {state['task_title']}
Description: {state['task_description']}

Current Progress:
{context}

Available agents:
- researcher: Gathers information from web sources
- writer: Creates content from research findings  
- analyst: Reviews and refines content for quality

Based on the current progress, which agent should work next?
If the task is complete with a polished deliverable, respond with "finalize".
If an unrecoverable error occurred, respond with "end".

Respond with only the agent name or action."""

        response = await self.supervisor_llm.ainvoke([
            HumanMessage(content=supervisor_prompt)
        ])
        
        next_action = response.content.strip().lower()
        logger.info(f"Supervisor decision for task {state['task_id']}: {next_action}")
        
        return {"next_agent": next_action}
    
    def _build_supervisor_context(self, state: AgentState) -> str:
        """Build context summary for supervisor decision making."""
        context_parts = []
        
        if state.get("research_output"):
            context_parts.append(f"✅ Research completed: {state['research_output'].get('sources_found', 0)} sources found")
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
    
    def _route_supervisor(self, state: AgentState) -> str:
        """Route to next agent based on supervisor decision."""
        return state.get("next_agent", "end")
    
    async def _researcher_node(self, state: AgentState) -> Dict[str, Any]:
        """Execute researcher agent."""
        try:
            context = {
                "title": state["task_title"],
                "description": state["task_description"]
            }
            
            result = await self.researcher.process(
                state["task_id"],
                context
            )
            
            # Store result in state
            state_update = {
                "research_output": result,
                "messages": [AIMessage(
                    content=f"Research completed with {result.get('sources_found', 0)} sources",
                    name="researcher"
                )]
            }
            
            # Save to database
            await self._save_agent_message(
                state["task_id"],
                AgentRole.RESEARCHER,
                result.get("synthesis", "")
            )
            
            return state_update
            
        except Exception as e:
            logger.error(f"Researcher error: {str(e)}")
            return {
                "error": f"Researcher error: {str(e)}",
                "messages": [AIMessage(
                    content=f"Error in research: {str(e)}",
                    name="researcher"
                )]
            }
    
    async def _writer_node(self, state: AgentState) -> Dict[str, Any]:
        """Execute writer agent."""
        try:
            context = {
                "title": state["task_title"],
                "description": state["task_description"],
                "research_output": state.get("research_output", {})
            }
            
            result = await self.writer.process(
                state["task_id"],
                context
            )
            
            # Store result in state
            state_update = {
                "writer_output": result,
                "messages": [AIMessage(
                    content="Content drafted successfully",
                    name="writer"
                )]
            }
            
            # Save to database
            await self._save_agent_message(
                state["task_id"],
                AgentRole.WRITER,
                result.get("content", "")[:500] + "..."  # Preview
            )
            
            return state_update
            
        except Exception as e:
            logger.error(f"Writer error: {str(e)}")
            return {
                "error": f"Writer error: {str(e)}",
                "messages": [AIMessage(
                    content=f"Error in writing: {str(e)}",
                    name="writer"
                )]
            }
    
    async def _analyst_node(self, state: AgentState) -> Dict[str, Any]:
        """Execute analyst agent."""
        try:
            context = {
                "title": state["task_title"],
                "description": state["task_description"],
                "research_output": state.get("research_output", {}),
                "writer_output": state.get("writer_output", {})
            }
            
            result = await self.analyst.process(
                state["task_id"],
                context
            )
            
            # Store result in state
            state_update = {
                "analyst_output": result,
                "final_deliverable": result.get("deliverable", ""),
                "messages": [AIMessage(
                    content="Content reviewed and refined",
                    name="analyst"
                )]
            }
            
            # Save to database
            await self._save_agent_message(
                state["task_id"],
                AgentRole.ANALYST,
                result.get("summary", "")
            )
            
            return state_update
            
        except Exception as e:
            logger.error(f"Analyst error: {str(e)}")
            return {
                "error": f"Analyst error: {str(e)}",
                "messages": [AIMessage(
                    content=f"Error in analysis: {str(e)}",
                    name="analyst"
                )]
            }
    
    async def _finalize_node(self, state: AgentState) -> Dict[str, Any]:
        """Finalize the task with the deliverable."""
        deliverable = state.get("final_deliverable", "")
        
        if not deliverable and state.get("writer_output"):
            # Fallback to writer output if analyst didn't produce deliverable
            deliverable = state["writer_output"].get("content", "")
        
        logger.info(f"Finalizing task {state['task_id']} with deliverable")
        
        return {
            "final_deliverable": deliverable,
            "messages": [AIMessage(
                content="Task completed successfully!",
                name="supervisor"
            )]
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
            "messages": [HumanMessage(content=f"Process this task: {task.title}")],
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
            
            # Execute workflow
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
                error_msg = final_state.get("error", "Unknown error occurred")
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
            message = Message(
                task_id=task_id,
                agent_role=agent_role,
                content=content
            )
            self._db_session.add(message)
            self._db_session.commit()
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")


# Import the fixed orchestrator
from app.agents.orchestrator_fixed import MultiAgentOrchestrator as FixedOrchestrator

# Global orchestrator instance
_orchestrator = None


def get_orchestrator() -> MultiAgentOrchestrator:
    """Get or create the global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        # Use the fixed orchestrator implementation
        _orchestrator = FixedOrchestrator()
    return _orchestrator