"""Auto Hint System CLI Interface and Utilities"""

import click
from typing import Optional
from pathlib import Path
from loguru import logger

from .system import get_auto_hint_system, initialize_auto_hint_system
from .config import AutoHintConfig, get_auto_hint_config, set_auto_hint_config


@click.group()
def auto_hint():
    """Auto Hint System CLI commands"""
    pass


@auto_hint.command()
@click.option('--enable/--disable', default=True, help='Enable or disable auto hint system')
@click.option('--persistence/--no-persistence', default=True, help='Enable/disable persistence')
@click.option('--storage-path', type=click.Path(), help='Custom storage path for hints')
@click.option('--min-history', default=3, help='Minimum history length for analysis')
@click.option('--analysis-interval', default=5, help='Analyze every N task completions')
def configure(enable: bool, persistence: bool, storage_path: Optional[str], 
              min_history: int, analysis_interval: int):
    """Configure auto hint system settings"""
    config = AutoHintConfig(
        enabled=enable,
        enable_persistence=persistence,
        hints_storage_path=storage_path,
        min_history_length=min_history,
        analysis_interval=analysis_interval
    )
    
    set_auto_hint_config(config)
    
    # Reinitialize system with new config
    if enable:
        initialize_auto_hint_system(
            enable_persistence=persistence,
            hints_path=storage_path
        )
    
    click.echo("Auto hint system configured successfully!")
    click.echo(f"Enabled: {enable}")
    click.echo(f"Persistence: {persistence}")
    if storage_path:
        click.echo(f"Storage path: {storage_path}")
    click.echo(f"Min history: {min_history}")
    click.echo(f"Analysis interval: {analysis_interval}")


@auto_hint.command()
def status():
    """Show current auto hint system status"""
    try:
        system = get_auto_hint_system()
        stats = system.get_system_statistics()
        
        click.echo("Auto Hint System Status:")
        click.echo(f"  Enabled: {stats.get('enabled', 'Unknown')}")
        click.echo(f"  Task completions: {stats.get('task_completion_count', 0)}")
        click.echo(f"  Analysis interval: {stats.get('analysis_interval', 'Unknown')}")
        click.echo(f"  Min history length: {stats.get('min_history_length', 'Unknown')}")
        
        if 'total_hints' in stats:
            click.echo(f"  Total hints: {stats['total_hints']}")
            click.echo(f"  Storage path: {stats.get('storage_path', 'Unknown')}")
            
            # Show hints by skill
            hints_by_skill = stats.get('hints_by_skill', {})
            if hints_by_skill:
                click.echo("  Hints by skill:")
                for skill, count in hints_by_skill.items():
                    click.echo(f"    {skill}: {count}")
        
        # Show cache info
        cache_info = stats.get('cache_info', {})
        if cache_info:
            click.echo(f"  Cached items: {cache_info.get('cached_items', 0)}")
            
    except Exception as e:
        click.echo(f"Error getting status: {e}")


@auto_hint.command()
@click.option('--skill', help='Show hints for specific skill')
@click.option('--max-hints', default=5, help='Maximum number of hints to show')
def show(skill: Optional[str], max_hints: int):
    """Show generated hints"""
    try:
        system = get_auto_hint_system()
        
        if skill:
            hints = system.get_hints_for_skill(skill, max_hints=max_hints)
            click.echo(f"Hints for {skill}:")
        else:
            all_hints = system.get_all_hints()
            hints = []
            for skill_name, skill_hints in all_hints.items():
                hints.extend(skill_hints)
            hints = hints[:max_hints]
            click.echo("All hints:")
        
        if not hints:
            click.echo("No hints available")
            return
        
        for i, hint in enumerate(hints, 1):
            metadata = hint.get("metadata", {})
            content = hint.get("content", "")
            
            click.echo(f"\n{i}. {metadata.get('title', 'Untitled')}")
            click.echo(f"   Skill: {metadata.get('skill_name', 'Unknown')}")
            click.echo(f"   Category: {metadata.get('category', 'Unknown')}")
            click.echo(f"   Usage: {metadata.get('usage_count', 0)}")
            click.echo(f"   Effectiveness: {metadata.get('effectiveness_score', 0.0):.2f}")
            click.echo(f"   Content: {content[:200]}{'...' if len(content) > 200 else ''}")
            
    except Exception as e:
        click.echo(f"Error showing hints: {e}")


@auto_hint.command()
@click.option('--max-age', default=30, help='Maximum age in days')
@click.option('--min-effectiveness', default=0.3, help='Minimum effectiveness score')
def cleanup(max_age: int, min_effectiveness: float):
    """Clean up old or ineffective hints"""
    try:
        system = get_auto_hint_system()
        deleted_count = system.cleanup_old_hints(max_age, min_effectiveness)
        click.echo(f"Cleaned up {deleted_count} hints")
    except Exception as e:
        click.echo(f"Error during cleanup: {e}")


@auto_hint.command()
@click.option('--skill', required=True, help='Skill name')
@click.option('--title', required=True, help='Hint title')
@click.option('--content', required=True, help='Hint content')
@click.option('--category', default='best_practice', help='Hint category')
def add_hint(skill: str, title: str, content: str, category: str):
    """Manually add a hint"""
    try:
        from .types import HintMetadata, HintCategory
        from datetime import datetime
        
        # Create metadata
        metadata = HintMetadata(
            title=title,
            category=HintCategory(category),
            skill_name=skill,
            version="1.0"
        )
        
        # Create hint data
        hint_data = {
            "metadata": metadata,
            "content": content
        }
        
        # Save hint
        system = get_auto_hint_system()
        if system.enable_persistence and system.persistence:
            success = system.persistence.save_hint(hint_data)
            if success:
                click.echo(f"Hint '{title}' added successfully for {skill}")
            else:
                click.echo("Failed to add hint")
        else:
            click.echo("Persistence is not enabled")
            
    except Exception as e:
        click.echo(f"Error adding hint: {e}")


@auto_hint.command()
@click.option('--path', type=click.Path(), help='Path to save statistics')
def stats(path: Optional[str]):
    """Show detailed system statistics"""
    try:
        system = get_auto_hint_system()
        stats = system.get_system_statistics()
        
        if path:
            import json
            with open(path, 'w') as f:
                json.dump(stats, f, indent=2, default=str)
            click.echo(f"Statistics saved to {path}")
        else:
            import json
            click.echo("System Statistics:")
            click.echo(json.dumps(stats, indent=2, default=str, ensure_ascii=False))
            
    except Exception as e:
        click.echo(f"Error getting statistics: {e}")


def register_auto_hint_commands(cli):
    """Register auto hint commands with the main CLI"""
    cli.add_command(auto_hint)