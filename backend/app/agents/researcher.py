"""
Researcher agent implementation with web search capabilities.
"""

import logging
from typing import Dict, Any, List
from pathlib import Path

from app.agents.base import BaseAgent
from app.models.message import AgentRole
from app.tools.web_search import TavilySearchTool
from app.tools.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class ResearcherAgent(BaseAgent):
    """
    Researcher agent that gathers information from web sources.
    
    Uses Tavily API for web search and synthesizes findings into
    structured insights for other agents to process.
    """
    
    def __init__(self):
        super().__init__(
            role=AgentRole.RESEARCHER,
            name="Research Agent",
            description="Specializes in web research and information gathering"
        )
        
        self.capabilities = [
            "Web search and information retrieval",
            "Data analysis and summarization",
            "Source verification and fact-checking",
            "Trend identification and pattern recognition",
            "Multi-source information synthesis"
        ]
        
        # Load system prompt from file
        prompt_path = Path(__file__).parent / "prompts" / "researcher.txt"
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()
            
        self.search_tool = TavilySearchTool()
        self.llm_client = get_llm_client()
    
    async def process(self, task_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a research task by searching the web and synthesizing findings.
        
        Args:
            task_id: Task identifier
            context: Task context with title and description
            
        Returns:
            Research findings and synthesized insights
        """
        task_title = context.get("title", "")
        task_description = context.get("description", "")
        
        # Send initial message
        await self.send_message(
            task_id,
            f"Starting research on: {task_title}\n\nI'll search for relevant information and synthesize my findings."
        )
        
        try:
            # Formulate search queries based on the task
            search_queries = await self._generate_search_queries(task_title, task_description)
            
            # Perform web searches
            all_results = []
            for query in search_queries[:3]:  # Limit to 3 searches for MVP
                await self.send_message(task_id, f"Searching for: {query}")
                results = await self.search_tool.search(query)
                all_results.extend(results)
            
            # Synthesize findings
            synthesis = await self._synthesize_research(
                task_title, 
                task_description,
                all_results
            )
            
            # Send final research summary
            await self.send_message(
                task_id,
                f"Research completed! Here's what I found:\n\n{synthesis}"
            )
            
            return {
                "role": self.role.value,
                "search_queries": search_queries,
                "sources_found": len(all_results),
                "synthesis": synthesis,
                "raw_results": all_results  # For other agents to reference
            }
            
        except Exception as e:
            logger.error(f"Research error for task {task_id}: {str(e)}")
            await self.send_message(
                task_id,
                f"I encountered an error during research: {str(e)}\n\nI'll provide what information I can based on my knowledge."
            )
            
            # Fallback to general knowledge
            fallback_response = await self._generate_fallback_research(task_title, task_description)
            
            return {
                "role": self.role.value,
                "error": str(e),
                "synthesis": fallback_response,
                "sources_found": 0
            }
    
    async def _generate_search_queries(self, title: str, description: str) -> List[str]:
        """Generate relevant search queries based on the task."""
        prompt = f"""Based on this task, generate 3-5 specific search queries that would help gather comprehensive information:

Title: {title}
Description: {description}

Generate search queries that would find:
1. Current/recent information (2024-2025)
2. Key players, companies, or entities involved
3. Market data, statistics, or trends
4. Technical details or specifications
5. Expert opinions or analysis

Return only the search queries, one per line."""
        
        response = await self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=prompt
        )
        
        queries = [q.strip() for q in response.split("\n") if q.strip()]
        return queries[:5]  # Max 5 queries
    
    async def _synthesize_research(self, title: str, description: str, results: List[Dict[str, Any]]) -> str:
        """Synthesize research findings into a structured report."""
        # Format search results for the LLM
        formatted_results = "\n\n".join([
            f"Source: {r.get('title', 'Unknown')}\n"
            f"URL: {r.get('url', 'N/A')}\n"
            f"Content: {r.get('content', '')[:500]}..."
            for r in results[:10]  # Limit to top 10 results
        ])
        
        prompt = f"""Based on the following search results, create a comprehensive research synthesis for this task:

Task Title: {title}
Task Description: {description}

Search Results:
{formatted_results}

Create a well-structured research report that includes:
1. Executive Summary (key findings in 2-3 sentences)
2. Main Findings (organized by relevance)
3. Key Data Points and Statistics
4. Notable Trends or Patterns
5. Important Considerations or Caveats

Format the response in clear markdown with proper headings."""
        
        synthesis = await self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=prompt
        )
        
        return synthesis
    
    async def _generate_fallback_research(self, title: str, description: str) -> str:
        """Generate research based on general knowledge when web search fails."""
        prompt = f"""Without access to current web search, provide the best research insights you can for:

Title: {title}
Description: {description}

Based on your knowledge, provide:
1. Background information and context
2. Key concepts and considerations
3. General trends and patterns in this area
4. Important factors to consider
5. Recommendations for further research

Be clear that this is based on general knowledge without current web data."""
        
        response = await self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=prompt
        )
        
        return response