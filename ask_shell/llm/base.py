"""LLM 客户端基类"""

from abc import ABC, abstractmethod
from typing import Optional, List, Callable

from ..models.types import LLMResponse, ExecutionResult, Message


class BaseLLMClient(ABC):
    """LLM 客户端基类"""
    
    def __init__(self):
        self.direct_mode: bool = False  # 是否为直接LLM模式
        self.custom_system_prompt: Optional[str] = None  # 自定义系统提示词
    
    def reset(self):
        """重置对话历史（子类可重写以实现具体逻辑）"""
        pass
    
    def set_direct_mode(self, direct_mode: bool):
        """设置直接LLM模式"""
        self.direct_mode = direct_mode
    
    def set_system_prompt(self, prompt: str):
        """设置自定义系统提示词"""
        self.custom_system_prompt = prompt
    
    def reset_system_prompt(self):
        """重置为默认系统提示词"""
        self.custom_system_prompt = None
    
    @property
    def system_prompt(self) -> str:
        """返回系统提示，优先使用自定义提示词"""
        if self.custom_system_prompt is not None:
            return self.custom_system_prompt
        return self.SYSTEM_PROMPT_DIRECT_MODE if self.direct_mode else self.SYSTEM_PROMPT_COMMAND_MODE
    
    def _build_result_message(self, result: ExecutionResult, task: str = "") -> str:
        """
        构建执行结果消息
        
        Args:
            result: 命令执行结果
            task: 原始任务描述（用于判断是否需要更多内容）
        """
        status = "成功" if result.success else "失败"
        
        # 总是使用完整输出以提供最多信息给LLM
        output = result.get_output_for_llm()  # 使用完整内容
        
        return f"""上一条命令执行{status}：
命令: {result.command}
返回码: {result.returncode}
输出:
{output}

请根据执行结果决定下一步操作。"""

    def _build_task_message(self, task: str) -> str:
        """构建任务消息"""
        return f"请帮我完成以下任务: {task}"
    
    @abstractmethod
    def generate(self, user_input: str, last_result: Optional[ExecutionResult] = None, stream_callback: Optional[Callable[[str], None]] = None, history: Optional[List[ExecutionResult]] = None) -> LLMResponse:
        """
        生成下一步命令
        
        Args:
            user_input: 用户输入的任务描述
            last_result: 上一次命令执行的结果
            stream_callback: 流式输出回调函数
            
        Returns:
            LLMResponse: LLM 响应
        """
        pass
