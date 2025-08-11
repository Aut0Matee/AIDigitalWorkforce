"""
Writer agent implementation for content creation.
"""

import logging
from typing import Dict, Any
from pathlib import Path

from app.agents.base import BaseAgent
from app.models.message import AgentRole
from app.tools.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class WriterAgent(BaseAgent):
    """
    Writer agent that transforms research into polished content.
    
    Takes research findings and creates well-structured, engaging
    content based on the task requirements.
    """
    
    def __init__(self):
        super().__init__(
            role=AgentRole.WRITER,
            name="Content Writer",
            description="Creates high-quality written content from research findings"
        )
        
        self.capabilities = [
            "Content creation and copywriting",
            "Adapting tone and style for different audiences",
            "Structuring information logically",
            "Creating engaging narratives",
            "Technical writing and documentation",
            "Blog posts, reports, and articles"
        ]
        
        # Load system prompt from file
        prompt_path = Path(__file__).parent / "prompts" / "writer.txt"
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()
            
        self.llm_client = get_llm_client()
    
    async def process(self, task_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a writing task based on research findings.
        
        Args:
            task_id: Task identifier
            context: Task context including research findings
            
        Returns:
            Written content and metadata
        """
        task_title = context.get("title", "")
        task_description = context.get("description", "")
        research_data = context.get("research_output", {})
        
        # Send initial message
        await self.send_message(
            task_id,
            "I've received the research findings. Now I'll create a well-structured, engaging piece of content based on this information."
        )
        
        try:
            # Determine content type and requirements
            content_requirements = await self._analyze_content_requirements(
                task_title, 
                task_description
            )
            
            await self.send_message(
                task_id,
                f"Content requirements identified:\n- Type: {content_requirements['type']}\n- Tone: {content_requirements['tone']}\n- Length: {content_requirements['length']}\n\nDrafting content now..."
            )
            
            # Create the content
            content = await self._create_content(
                task_title,
                task_description,
                research_data.get("synthesis", ""),
                content_requirements
            )
            
            # Create metadata about the content
            metadata = await self._generate_content_metadata(content)
            
            # Send completion message with full content
            await self.send_message(
                task_id,
                f"Content creation completed!\n\n**Full Content:**\n{content}\n\n**Content Stats:**\n- Word count: {metadata['word_count']}\n- Sections: {metadata['sections']}\n- Reading time: {metadata['reading_time']}"
            )
            
            return {
                "role": self.role.value,
                "content": content,
                "content_type": content_requirements["type"],
                "metadata": metadata,
                "requirements": content_requirements
            }
            
        except Exception as e:
            logger.error(f"Writing error for task {task_id}: {str(e)}")
            await self.send_message(
                task_id,
                f"I encountered an error during content creation: {str(e)}\n\nI'll create a basic draft based on available information."
            )
            
            # Fallback content creation
            fallback_content = await self._create_fallback_content(
                task_title,
                task_description,
                research_data
            )
            
            return {
                "role": self.role.value,
                "content": fallback_content,
                "error": str(e)
            }
    
    async def _analyze_content_requirements(self, title: str, description: str) -> Dict[str, str]:
        """Analyze the task to determine content requirements."""
        prompt = f"""Analyze this task to determine content requirements:

Title: {title}
Description: {description}

Determine:
1. Content Type (e.g., blog post, report, article, analysis, guide)
2. Tone (e.g., professional, casual, technical, educational)
3. Approximate Length (e.g., short 500-1000 words, medium 1000-2000 words, long 2000+ words)
4. Key sections or structure needed

Return as:
Type: [content type]
Tone: [tone]
Length: [length]
Structure: [key sections]"""
        
        response = await self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=prompt
        )
        
        # Parse response into requirements
        requirements = {
            "type": "report",  # default
            "tone": "professional",
            "length": "medium",
            "structure": "standard"
        }
        
        for line in response.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                if key in requirements:
                    requirements[key] = value
        
        return requirements
    
    async def _create_content(
        self, 
        title: str, 
        description: str, 
        research: str,
        requirements: Dict[str, str]
    ) -> str:
        """Create content based on research and requirements."""
        prompt = f"""Create {requirements['type']} content based on this research:

Task: {title}
Requirements: {description}

Content Type: {requirements['type']}
Tone: {requirements['tone']}
Target Length: {requirements['length']}

Research Findings:
{research}

Create well-structured content that:
1. Has a compelling introduction
2. Organizes information logically
3. Uses appropriate headings and formatting (markdown)
4. Includes relevant data and insights from the research
5. Provides value to the reader
6. Has a strong conclusion with key takeaways

Write the complete content now:"""
        
        content = await self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
            temperature=0.7,  # Slightly more creative for writing
            max_tokens=4000   # Adjusted for gpt-4o-mini compatibility
        )
        
        return content
    
    async def _generate_content_metadata(self, content: str) -> Dict[str, Any]:
        """Generate metadata about the created content."""
        word_count = len(content.split())
        char_count = len(content)
        
        # Count sections (markdown headers)
        sections = content.count("#")
        
        # Estimate reading time (200 words per minute average)
        reading_time = f"{max(1, round(word_count / 200))} min read"
        
        return {
            "word_count": word_count,
            "character_count": char_count,
            "sections": sections,
            "reading_time": reading_time,
            "has_introduction": "introduction" in content.lower() or content.startswith("#"),
            "has_conclusion": "conclusion" in content.lower() or "summary" in content.lower()
        }
    
    async def _create_fallback_content(
        self, 
        title: str, 
        description: str,
        research_data: Dict[str, Any]
    ) -> str:
        """Create basic content when full process fails."""
        available_info = research_data.get("synthesis", "No research data available")
        
        prompt = f"""Create a basic content piece for:

Title: {title}
Description: {description}

Available Information:
{available_info}

Create a simple but complete piece of content with:
1. Introduction explaining the topic
2. Main points based on available information
3. Conclusion with key takeaways

Keep it professional and acknowledge any limitations in the information."""
        
        content = await self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
            max_tokens=2000   # Adjusted for fallback content
        )
        
        return content