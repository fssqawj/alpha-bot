"""LLM 客户端基类"""

from abc import ABC, abstractmethod
from typing import Optional, List, Callable

from ..models.types import LLMResponse, ExecutionResult, Message


class BaseLLMClient(ABC):
    """LLM 客户端基类"""
    
    def __init__(self):
        pass
    
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, stream_callback: Optional[Callable[[str], None]] = None, response_class=None):
        pass
