"""Skill Manager for routing tasks to appropriate skills"""
from loguru import logger
from typing import List, Optional, Dict, Any, TYPE_CHECKING
from .skill_selector import SkillSelector
from .base_skill import BaseSkill
from ..models.types import SkillSelectResponse, SkillResponse

if TYPE_CHECKING:
    from ..ui.console import ConsoleUI


class SkillManager:
    """
    Manages all available skills and routes tasks to the appropriate skill
    
    The SkillManager:
    1. Registers available skills
    2. Uses LLM to intelligently select which skill should handle a task
    3. Executes the selected skill
    4. Manages skill lifecycle (reset, etc.)
    """
    
    def __init__(self, llm_client=None, ui=None):
        """
        Initialize SkillManager
        
        Args:
            llm_client: LLM client for intelligent skill selection
            ui: ConsoleUI instance for displaying selection process
        """
        self.skills: List[BaseSkill] = []
        self.default_skill: Optional[BaseSkill] = None
        self.skill_selector = SkillSelector(llm_client) if llm_client else None
        self.ui = ui
    
    def register_skill(self, skill: BaseSkill, is_default: bool = False):
        """
        Register a new skill
        
        Args:
            skill: The skill instance to register
            is_default: If True, this skill will be used as fallback
        """
        self.skills.append(skill)
        if is_default:
            self.default_skill = skill
    
    def select_skill(self, task: str, context: Optional[Dict[str, Any]] = None) -> Optional[SkillSelectResponse]:
        """
        Select the best skill to handle the given task using LLM-based intelligent selection
        
        Args:
            task: The task description
            context: Optional context for decision making
            
        Returns:
            SkillSelectResponse with the selected skill and selection information, or default skill if no match found
        """
        # Use intelligent LLM-based selection
        try:
            with self.ui.skill_selection_animation():
                selected_skill, confidence, reasoning, task_complete = self.skill_selector.select_skill(
                    task, self.skills, context
                )
            if task_complete:
                return SkillSelectResponse(skill=None, skill_name="none", task_complete=True, select_reason="Task completed")
            if selected_skill:
                self.ui.print_skill_selected(
                    skill_name=selected_skill.name,
                    confidence=confidence,
                    reasoning=reasoning,
                    capabilities=[c.value for c in selected_skill.capabilities]
                )
                return SkillSelectResponse(skill=selected_skill, skill_name=selected_skill.name, task_complete=task_complete, select_reason=reasoning)
        except Exception as e:
            logger.opt(exception=e).error(f"Intelligent selection failed: {e}, using default skill")
            if self.ui:
                self.ui.print_error(f"Intelligent selection failed: {e}, using default skill")
            else:
                logger.warning(f"[SkillManager] Intelligent selection failed: {e}, using default skill")
        return SkillSelectResponse(skill=self.default_skill, skill_name=self.default_skill.name if self.default_skill else "unknown", task_complete=False, select_reason="Fallback due to selection error")
    
    def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> SkillResponse:
        """
        Execute a task using the appropriate skill
        
        Args:
            task: The task to execute
            context: Execution context
            **kwargs: Additional parameters passed to skill
            
        Returns:
            SkillResponse from the executed skill
        """
        # Select skill
        skill_select_response = self.select_skill(task, context) 
        if not skill_select_response:
            return SkillResponse(
                skill_name="error",
                thinking="No suitable skill found and no default skill configured",
                task_complete=True,
                direct_response="Error: Unable to find a skill to handle this task."
            )
        if skill_select_response.task_complete:
            return SkillResponse(
                skill_name="none",
                thinking="Task completed",
                task_complete=True,
                direct_response="Task completed."
            ) 
        # Execute the selected skill
        try:
            with self.ui.streaming_display() as stream_callback:
                skill_exec_response = skill_select_response.skill.execute(task, context, stream_callback=stream_callback)
                skill_response = SkillResponse(
                    skill=skill_select_response.skill,
                    skill_name=skill_select_response.skill_name, 
                    select_reason=skill_select_response.select_reason,
                    task_complete=skill_select_response.task_complete, 
                    thinking=skill_exec_response.thinking,
                    command=skill_exec_response.command,
                    explanation=skill_exec_response.explanation,
                    next_step=skill_exec_response.next_step,
                    is_dangerous=skill_exec_response.is_dangerous,
                    danger_reason=skill_exec_response.danger_reason,
                    error_analysis=skill_exec_response.error_analysis,
                    direct_response=skill_exec_response.direct_response,
                    generated_files=skill_exec_response.generated_files,
                    file_metadata=skill_exec_response.file_metadata,
                    api_response=skill_exec_response.api_response,
                    service_status=skill_exec_response.service_status
                )
                return skill_response
        except Exception as e:
            logger.opt(exception=e).error(f"Skill execution failed: {str(e)}")
            return SkillResponse(
                skill=skill_select_response.skill,
                skill_name=skill_select_response.skill_name,
                select_reason=skill_select_response.select_reason,
                thinking=f"Skill execution failed: {str(e)}",
                task_complete=True,
                direct_response=f"Error executing {skill_select_response.skill_name}: {str(e)}"
            )
    
    def get_skill_by_name(self, name: str) -> Optional[BaseSkill]:
        """Get a skill by its name"""
        for skill in self.skills:
            if skill.name.lower() == name.lower():
                return skill
        return None
    
    def list_skills(self) -> List[Dict[str, Any]]:
        """
        List all registered skills with their information
        
        Returns:
            List of skill information dictionaries
        """
        return [
            {
                "name": skill.name,
                "capabilities": [c.value for c in skill.capabilities],
                "description": skill.get_description()
            }
            for skill in self.skills
        ]
    
    def reset_all(self):
        """Reset state for all skills"""
        for skill in self.skills:
            skill.reset()
