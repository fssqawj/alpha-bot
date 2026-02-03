"""Memory system data types"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


@dataclass
class MemoryEntry:
    """
    Represents a single memory entry with metadata
    
    Contains information from a skill execution step that can be stored,
    summarized, and retrieved as needed.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    skill_name: str = ""
    thinking: str = ""
    command: str = ""
    result: str = ""
    summary: str = ""  # Auto-generated summary
    importance: float = 0.5  # 0.0-1.0 rating of importance
    tags: List[str] = field(default_factory=list)  # Keywords for categorization
    step_number: int = 0  # The step number in the task execution
    
    def __post_init__(self):
        if self.summary == "":
            # Generate a default summary from available information
            parts = []
            if self.thinking:
                parts.append(f"Thinking: {self.thinking[:100]}{'...' if len(self.thinking) > 100 else ''}")
            if self.command:
                parts.append(f"Command: {self.command[:100]}{'...' if len(self.command) > 100 else ''}")
            if self.result:
                parts.append(f"Result: {self.result[:100]}{'...' if len(self.result) > 100 else ''}")
            self.summary = "; ".join(parts) if parts else "No information"


@dataclass
class MemorySummary:
    """
    Represents a compressed summary of multiple memory entries
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    title: str = ""
    content: str = ""
    source_entries: List[str] = field(default_factory=list)  # IDs of entries that were summarized
    tags: List[str] = field(default_factory=list)


@dataclass
class MemoryQuery:
    """
    Query parameters for retrieving memories
    """
    keywords: List[str] = field(default_factory=list)
    min_importance: float = 0.0
    max_results: int = 10
    tags: List[str] = field(default_factory=list)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None