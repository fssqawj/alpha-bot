"""Data types for Auto Hint System"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum
import uuid


class HintCategory(Enum):
    """Categories of hints"""
    SUCCESS_PATTERN = "success_pattern"      # 成功模式
    FAILURE_PATTERN = "failure_pattern"      # 失败模式
    BEST_PRACTICE = "best_practice"          # 最佳实践
    TROUBLESHOOTING = "troubleshooting"      # 故障排除
    OPTIMIZATION = "optimization"            # 优化建议
    SECURITY = "security"                    # 安全建议
    PERFORMANCE = "performance"              # 性能优化


@dataclass
class HintPattern:
    """
    Represents a discovered pattern from execution history
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    category: HintCategory = HintCategory.SUCCESS_PATTERN
    skill_name: str = ""                     # 相关技能名称
    pattern_description: str = ""            # 模式描述
    context_keywords: List[str] = field(default_factory=list)  # 上下文关键词
    success_rate: float = 0.0                # 成功率 (0.0-1.0)
    frequency: int = 1                       # 出现频率
    confidence: float = 0.0                  # 置信度 (0.0-1.0)
    examples: List[str] = field(default_factory=list)  # 示例
    anti_examples: List[str] = field(default_factory=list)  # 反例
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if isinstance(self.category, str):
            self.category = HintCategory(self.category)


@dataclass
class HintMetadata:
    """
    Metadata for generated hints
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    category: HintCategory = HintCategory.BEST_PRACTICE
    skill_name: str = ""
    pattern_id: str = ""                     # 关联的pattern ID
    version: str = "1.0"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    usage_count: int = 0                     # 使用次数
    effectiveness_score: float = 0.0         # 有效性评分
    
    def __post_init__(self):
        if isinstance(self.category, str):
            self.category = HintCategory(self.category)


@dataclass
class ExecutionAnalysisResult:
    """
    Result of execution history analysis
    """
    patterns: List[HintPattern] = field(default_factory=list)
    success_patterns: List[HintPattern] = field(default_factory=list)
    failure_patterns: List[HintPattern] = field(default_factory=list)
    improvement_opportunities: List[str] = field(default_factory=list)
    skill_insights: Dict[str, Any] = field(default_factory=dict)