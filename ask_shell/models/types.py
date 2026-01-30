"""数据模型定义"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SkillCapability(Enum):
    """Types of capabilities a skill can provide"""
    COMMAND_GENERATION = "command_generation"  # Generate and execute shell commands
    LLM_PROCESSING = "llm_processing"  # Process content with LLM (translate, summarize, etc.)
    FILE_GENERATION = "file_generation"  # Generate files (PPT, images, videos, etc.)
    WEB_INTERACTION = "web_interaction"  # Interact with web services/APIs
    DATA_ANALYSIS = "data_analysis"  # Analyze and visualize data


@dataclass
class SkillSelectResponse:
    skill_name: str = ""
    skill: Optional["BaseSkill"] = None
    select_reason: str = ""
    task_complete: Optional[bool] = None  # Whether the overall task is complete (determined by skill selector)


@dataclass
class SkillExecutionResponse:
    thinking: str = ""  # Reasoning process
    # Command execution fields (for command generation skills)
    command: str = ""  # Shell command to execute
    explanation: str = ""  # Command explanation
    next_step: str = ""  # Next planned step
    is_dangerous: bool = False  # Safety flag
    danger_reason: str = ""  # Danger explanation
    error_analysis: str = ""  # Error analysis if previous command failed
    
    # Direct response fields (for LLM/content processing skills)
    direct_response: str = ""  # Direct content output
    
    # File generation fields (for file creation skills)
    generated_files: List[str] = None  # Paths to generated files
    file_metadata: Dict[str, Any] = None  # Additional file information
    
    # API/Service fields (for external service skills)
    api_response: Dict[str, Any] = None  # Response from external APIs
    service_status: str = ""  # Status of service interaction

    def __post_init__(self):
        if self.generated_files is None:
            self.generated_files = []
        if self.file_metadata is None:
            self.file_metadata = {}
        if self.api_response is None:
            self.api_response = {}


@dataclass
class SkillResponse(SkillSelectResponse, SkillExecutionResponse):
    """
    Unified response format for all skills
    
    This replaces the old LLMResponse and provides a common interface
    for all skill types.
    """
    pass


@dataclass
class ExecutionResult:
    """命令执行结果"""
    command: str
    returncode: int
    stdout: str
    stderr: str
    skill_response: Optional[SkillResponse] = None
    
    @property
    def success(self) -> bool:
        return self.returncode == 0
    
    @property
    def output(self) -> str:
        """获取合并的输出"""
        parts = []
        if self.stdout:
            parts.append(self.stdout)
        if self.stderr:
            parts.append(f"[stderr] {self.stderr}")
        return "\n".join(parts) if parts else "(无输出)"
    
    def truncated_output(self, max_length: int = 2000) -> str:
        """获取截断的输出"""
        output = self.output
        if len(output) > max_length:
            return output[:max_length] + "\n...(输出已截断)"
        return output
    
    def get_output_for_llm(self, max_length: int = 10000) -> str:
        """获取用于LLM处理的输出（更大的限制）"""
        output = self.output
        if len(output) > max_length:
            return output[:max_length] + f"\n...(输出已截断，仅显示前{max_length}字符)"
        return output


@dataclass
class LLMResponse:
    """LLM 响应结构"""
    thinking: str = ""
    command: str = ""
    explanation: str = ""
    next_step: str = ""
    error_analysis: str = ""
    is_dangerous: bool = False  # 是否为危险操作
    danger_reason: str = ""     # 危险原因说明
    is_direct_mode: bool = False  # 是否为直接LLM模式（非命令模式）
    direct_response: str = ""   # 直接LLM响应内容（用于翻译、总结、分析等任务）

    
    @classmethod
    def from_dict(cls, data: dict) -> "LLMResponse":
        return cls(
            thinking=data.get("thinking", ""),
            command=data.get("command", ""),
            explanation=data.get("explanation", ""),
            next_step=data.get("next_step", ""),
            error_analysis=data.get("error_analysis", ""),
            is_dangerous=data.get("is_dangerous", False),
            danger_reason=data.get("danger_reason", ""),
            is_direct_mode=data.get("is_direct_mode", False),
            direct_response=data.get("direct_response", ""),

        )


@dataclass
class Message:
    """对话消息"""
    role: str  # "system", "user", "assistant"
    content: str


@dataclass
class TaskContext:
    """任务上下文"""
    task_description: str
    status: TaskStatus = TaskStatus.PENDING
    iteration: int = 0
    history: List[ExecutionResult] = field(default_factory=list)
    
    def add_result(self, result: ExecutionResult):
        """添加执行结果到历史"""
        self.history.append(result)
    
    @property
    def last_result(self) -> Optional[ExecutionResult]:
        """获取最后一次执行结果"""
        return self.history[-1] if self.history else None
