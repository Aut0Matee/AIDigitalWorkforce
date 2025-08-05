"""
Analyst agent implementation for content review and refinement.
"""

import logging
from typing import Dict, Any, List
from pathlib import Path

from app.agents.base import BaseAgent
from app.models.message import AgentRole
from app.tools.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class AnalystAgent(BaseAgent):
    """
    Analyst agent that reviews, critiques, and refines content.
    
    Ensures quality, accuracy, and alignment with task requirements.
    """
    
    def __init__(self):
        super().__init__(
            role=AgentRole.ANALYST,
            name="Quality Analyst",
            description="Reviews and improves content quality and accuracy"
        )
        
        self.capabilities = [
            "Content review and quality assessment",
            "Fact-checking and accuracy verification",
            "Logical consistency analysis",
            "Clarity and readability improvement",
            "Professional editing and refinement",
            "Constructive feedback and suggestions"
        ]
        
        # Load system prompt from file
        prompt_path = Path(__file__).parent / "prompts" / "analyst.txt"
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()
            
        self.llm_client = get_llm_client()
    
    async def process(self, task_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process content for review and refinement.
        
        Args:
            task_id: Task identifier
            context: Task context including writer's output
            
        Returns:
            Refined content and quality assessment
        """
        task_title = context.get("title", "")
        task_description = context.get("description", "")
        writer_output = context.get("writer_output", {})
        research_output = context.get("research_output", {})
        
        content = writer_output.get("content", "")
        
        # Send initial message
        await self.send_message(
            task_id,
            "I've received the content from the Writer. Now I'll review it for quality, accuracy, and alignment with the task requirements."
        )
        
        try:
            # Perform quality assessment
            assessment = await self._assess_content_quality(
                content,
                task_title,
                task_description,
                research_output
            )
            
            await self.send_message(
                task_id,
                f"Quality Assessment:\n{self._format_assessment(assessment)}\n\nNow refining the content..."
            )
            
            # Refine the content based on assessment
            refined_content = await self._refine_content(
                content,
                assessment,
                task_title,
                task_description
            )
            
            # Generate final summary
            summary = await self._generate_final_summary(
                refined_content,
                assessment
            )
            
            await self.send_message(
                task_id,
                f"Content refinement completed!\n\n{summary}"
            )
            
            return {
                "role": self.role.value,
                "refined_content": refined_content,
                "assessment": assessment,
                "summary": summary,
                "deliverable": refined_content  # Final deliverable
            }
            
        except Exception as e:
            logger.error(f"Analysis error for task {task_id}: {str(e)}")
            await self.send_message(
                task_id,
                f"I encountered an error during analysis: {str(e)}\n\nReturning the original content with basic review notes."
            )
            
            return {
                "role": self.role.value,
                "refined_content": content,
                "error": str(e),
                "deliverable": content
            }
    
    async def _assess_content_quality(
        self, 
        content: str, 
        title: str,
        description: str,
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess content quality across multiple dimensions."""
        prompt = f"""Assess this content for quality and alignment with requirements:

Task Title: {title}
Task Requirements: {description}

Content to Review:
{content}

Research Sources Available: {research_data.get('sources_found', 0)}

Assess the following:
1. Accuracy: Are facts correct and properly sourced?
2. Completeness: Does it address all requirements?
3. Clarity: Is it clear and well-structured?
4. Engagement: Is it engaging and valuable to readers?
5. Technical Quality: Grammar, spelling, formatting?

Provide scores (1-10) and specific feedback for each dimension.
Format as:
Accuracy: [score] - [feedback]
Completeness: [score] - [feedback]
Clarity: [score] - [feedback]
Engagement: [score] - [feedback]
Technical Quality: [score] - [feedback]
Overall: [score] - [summary]"""
        
        response = await self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=prompt
        )
        
        # Parse assessment
        assessment = {
            "accuracy": {"score": 0, "feedback": ""},
            "completeness": {"score": 0, "feedback": ""},
            "clarity": {"score": 0, "feedback": ""},
            "engagement": {"score": 0, "feedback": ""},
            "technical_quality": {"score": 0, "feedback": ""},
            "overall": {"score": 0, "feedback": ""}
        }
        
        for line in response.split("\n"):
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    dimension = parts[0].strip().lower().replace(" ", "_")
                    value_parts = parts[1].strip().split(" - ", 1)
                    
                    if dimension in assessment and len(value_parts) >= 1:
                        try:
                            score = int(value_parts[0].strip())
                            feedback = value_parts[1].strip() if len(value_parts) > 1 else ""
                            assessment[dimension] = {"score": score, "feedback": feedback}
                        except ValueError:
                            pass
        
        return assessment
    
    async def _refine_content(
        self,
        content: str,
        assessment: Dict[str, Any],
        title: str,
        description: str
    ) -> str:
        """Refine content based on quality assessment."""
        # Focus on dimensions that need improvement
        improvement_areas = []
        for dimension, data in assessment.items():
            if data["score"] < 8:
                improvement_areas.append(f"{dimension}: {data['feedback']}")
        
        prompt = f"""Refine this content based on the quality assessment:

Task: {title}
Requirements: {description}

Areas for Improvement:
{chr(10).join(improvement_areas)}

Original Content:
{content}

Create an improved version that:
1. Addresses all identified issues
2. Maintains the writer's voice and style
3. Enhances clarity and engagement
4. Ensures accuracy and completeness
5. Polishes technical quality

Provide the complete refined content:"""
        
        refined_content = await self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
            temperature=0.5  # Lower temperature for more controlled refinement
        )
        
        return refined_content
    
    def _format_assessment(self, assessment: Dict[str, Any]) -> str:
        """Format assessment for display."""
        lines = []
        for dimension, data in assessment.items():
            dim_name = dimension.replace("_", " ").title()
            score = data["score"]
            feedback = data["feedback"]
            
            # Add emoji based on score
            if score >= 9:
                emoji = "✅"
            elif score >= 7:
                emoji = "🔶"
            else:
                emoji = "⚠️"
                
            lines.append(f"{emoji} **{dim_name}**: {score}/10 - {feedback}")
        
        return "\n".join(lines)
    
    async def _generate_final_summary(
        self,
        refined_content: str,
        assessment: Dict[str, Any]
    ) -> str:
        """Generate a summary of the refinement process."""
        overall_score = assessment["overall"]["score"]
        
        prompt = f"""Based on the content refinement process, create a brief summary:

Overall Quality Score: {overall_score}/10

Summarize:
1. Key improvements made
2. Content strengths
3. Final quality assessment
4. Any remaining considerations

Keep it concise (3-4 sentences)."""
        
        summary = await self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=prompt
        )
        
        return summary