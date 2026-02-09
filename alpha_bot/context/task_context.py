from loguru import logger
from dataclasses import dataclass, field
from typing import Optional, List
from ..models.types import TaskStatus, ExecutionResult
from ..memory.bank import MemoryBank
from ..memory.types import MemoryEntry



@dataclass
class TaskContext:
    """任务上下文"""
    task_description: str
    status: TaskStatus = TaskStatus.PENDING
    iteration: int = 0
    history: List[ExecutionResult] = field(default_factory=list)
    memory_bank: MemoryBank = field(default_factory=MemoryBank)
    
    def add_result(self, result: ExecutionResult):
        """添加执行结果到历史"""
        self.history.append(result)
        
        # Add to memory bank as well
        if result.skill_response:
            logger.info(f"Adding skill response to memory: {result.skill_response}")
            
            memory_entry = MemoryEntry(
                skill_name=result.skill_response.skill_name,
                thinking=result.skill_response.thinking,
                command=result.skill_response.command,
                result=result.get_output_for_llm(max_length=2000),  # Use truncated output to avoid memory bloat
                step_number=len(self.history)
            )
            self.memory_bank.add_entry(memory_entry)
            logger.info(f"Memory Bank Status: {self.memory_bank.get_stats()}")
    
    @property
    def last_result(self) -> Optional[ExecutionResult]:
        """获取最后一次执行结果"""
        return self.history[-1] if self.history else None
