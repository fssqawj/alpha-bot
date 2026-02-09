"""Auto Hint System - Automatically extract skill hints from execution history"""

from .types import HintPattern, HintCategory, HintMetadata
from .analyzer import ExecutionResultAnalyzer
from .generator import HintGenerator
from .persistence import HintPersistenceManager
# Import system after other modules to avoid circular imports

def get_auto_hint_system(enable_persistence=True):
    """Get or create the global auto hint system instance"""
    from .system import get_auto_hint_system as _get_auto_hint_system
    return _get_auto_hint_system(enable_persistence)

def initialize_auto_hint_system(enable_persistence=True, hints_path=None):
    """Initialize the global auto hint system"""
    from .system import initialize_auto_hint_system as _initialize_auto_hint_system
    return _initialize_auto_hint_system(enable_persistence, hints_path)

__all__ = [
    'HintPattern',
    'HintCategory', 
    'HintMetadata',
    'ExecutionResultAnalyzer',
    'HintGenerator',
    'HintPersistenceManager',
    'get_auto_hint_system',
    'initialize_auto_hint_system'
]