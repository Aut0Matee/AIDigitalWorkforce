"""
Web search tool using Tavily API for research capabilities.
"""

import logging
from typing import List, Dict, Any
from tavily import TavilyClient
from app.config import settings

logger = logging.getLogger(__name__)


class TavilySearchTool:
    """Web search tool using Tavily API for agent research."""
    
    def __init__(self):
        self.client = TavilyClient(api_key=settings.tavily_api_key)
    
    async def search(
        self, 
        query: str, 
        max_results: int = 5,
        include_domains: List[str] = None,
        exclude_domains: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search the web using Tavily API.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            include_domains: Optional list of domains to include
            exclude_domains: Optional list of domains to exclude
            
        Returns:
            List of search results with title, url, and content
        """
        try:
            # Tavily search is synchronous, but we wrap for consistency
            response = self.client.search(
                query=query,
                max_results=max_results,
                include_domains=include_domains or [],
                exclude_domains=exclude_domains or []
            )
            
            # Extract and format results
            results = []
            for result in response.get('results', []):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0.0)
                })
            
            logger.info(f"Found {len(results)} results for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Tavily search error: {str(e)}")
            # Return empty results on error rather than failing
            return []
    
    async def get_answer(self, query: str) -> str:
        """
        Get a direct answer to a question using Tavily's QA search.
        
        Args:
            query: Question to answer
            
        Returns:
            Direct answer text
        """
        try:
            response = self.client.qna_search(query=query)
            return response.get('answer', 'No direct answer found.')
        except Exception as e:
            logger.error(f"Tavily QA search error: {str(e)}")
            return f"Error getting answer: {str(e)}"