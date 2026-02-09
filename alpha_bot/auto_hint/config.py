"""Configuration for Auto Hint System"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class AutoHintConfig:
    """Configuration for Auto Hint System"""
    
    # Enable/disable the system
    enabled: bool = True
    
    # Persistence settings
    enable_persistence: bool = True
    hints_storage_path: Optional[str] = None
    
    # Analysis settings
    min_history_length: int = 3
    analysis_interval: int = 5
    min_frequency_threshold: int = 2
    min_confidence_threshold: float = 0.7
    success_rate_threshold: float = 0.8
    
    # Generation settings
    max_hints_per_category: int = 5
    max_hints_per_skill: int = 3
    
    # Cleanup settings
    auto_cleanup_enabled: bool = True
    cleanup_max_age_days: int = 30
    cleanup_min_effectiveness: float = 0.3


def load_auto_hint_config() -> AutoHintConfig:
    """
    Load auto hint configuration from environment variables or defaults
    
    Returns:
        AutoHintConfig instance
    """
    config = AutoHintConfig()
    
    # Load from environment variables
    config.enabled = os.getenv("AUTO_HINT_ENABLED", "true").lower() == "true"
    config.enable_persistence = os.getenv("AUTO_HINT_PERSISTENCE", "true").lower() == "true"
    
    hints_path = os.getenv("AUTO_HINT_STORAGE_PATH")
    if hints_path:
        config.hints_storage_path = hints_path
    
    # Analysis settings
    try:
        config.min_history_length = int(os.getenv("AUTO_HINT_MIN_HISTORY", "3"))
        config.analysis_interval = int(os.getenv("AUTO_HINT_ANALYSIS_INTERVAL", "5"))
        config.min_frequency_threshold = int(os.getenv("AUTO_HINT_MIN_FREQUENCY", "2"))
        config.min_confidence_threshold = float(os.getenv("AUTO_HINT_MIN_CONFIDENCE", "0.7"))
        config.success_rate_threshold = float(os.getenv("AUTO_HINT_SUCCESS_RATE", "0.8"))
    except ValueError:
        pass  # Use defaults if conversion fails
    
    # Generation settings
    try:
        config.max_hints_per_category = int(os.getenv("AUTO_HINT_MAX_PER_CATEGORY", "5"))
        config.max_hints_per_skill = int(os.getenv("AUTO_HINT_MAX_PER_SKILL", "3"))
    except ValueError:
        pass
    
    # Cleanup settings
    config.auto_cleanup_enabled = os.getenv("AUTO_HINT_AUTO_CLEANUP", "true").lower() == "true"
    try:
        config.cleanup_max_age_days = int(os.getenv("AUTO_HINT_CLEANUP_AGE", "30"))
        config.cleanup_min_effectiveness = float(os.getenv("AUTO_HINT_CLEANUP_EFFECTIVENESS", "0.3"))
    except ValueError:
        pass
    
    return config


def get_auto_hint_config() -> AutoHintConfig:
    """
    Get the global auto hint configuration
    
    Returns:
        AutoHintConfig instance
    """
    global _config
    if _config is None:
        _config = load_auto_hint_config()
    return _config


def set_auto_hint_config(config: AutoHintConfig):
    """
    Set the global auto hint configuration
    
    Args:
        config: AutoHintConfig instance
    """
    global _config
    _config = config


# Global config instance
_config: Optional[AutoHintConfig] = None