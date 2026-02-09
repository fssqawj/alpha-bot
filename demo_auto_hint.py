#!/usr/bin/env python3
"""Demo script for Auto Hint System"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alpha_bot.auto_hint.system import AutoHintSystem
from alpha_bot.auto_hint.types import HintPattern, HintCategory
from alpha_bot.models.types import ExecutionResult, SkillResponse
from alpha_bot.skills.base_skill import BaseSkill


def create_mock_execution_history():
    """Create mock execution history for demonstration"""
    # Create mock skill responses
    skill_response1 = SkillResponse(
        skill_name="CommandSkill",
        thinking="Need to list files in current directory",
        command="ls -la",
        explanation="List all files with details",
        next_step="Check if target file exists"
    )
    
    skill_response2 = SkillResponse(
        skill_name="CommandSkill", 
        thinking="Looking for specific file pattern",
        command="find . -name '*.py' -type f",
        explanation="Find all Python files",
        next_step="Count the files found"
    )
    
    skill_response3 = SkillResponse(
        skill_name="BrowserSkill",
        thinking="Need to navigate to website",
        command="python3 /tmp/temp_script.py",
        explanation="Open browser and navigate to target site",
        next_step="Extract required information"
    )
    
    # Create execution results
    results = [
        ExecutionResult(
            command="ls -la",
            returncode=0,
            stdout="total 24\ndrwxr-xr-x  5 user  staff  160 Dec  1 10:00 .\ndrwxr-xr-x  8 user  staff  256 Dec  1 09:30 ..\n-rw-r--r--  1 user  staff  1024 Dec  1 10:00 main.py\n-rw-r--r--  1 user  staff   512 Dec  1 09:45 utils.py",
            stderr="",
            skill_response=skill_response1
        ),
        ExecutionResult(
            command="find . -name '*.py' -type f",
            returncode=0,
            stdout="./main.py\n./utils.py\n./test.py\n./scripts/helper.py",
            stderr="",
            skill_response=skill_response2
        ),
        ExecutionResult(
            command="python3 /tmp/temp_script.py",
            returncode=0,
            stdout="Browser opened successfully\nNavigated to https://github.com\nPage title: GitHub: Where the world builds software",
            stderr="",
            skill_response=skill_response3
        )
    ]
    
    return results


def create_mock_skills():
    """Create mock skills for demonstration"""
    class MockCommandSkill(BaseSkill):
        def get_capabilities(self):
            return ["command_generation"]
        def execute(self, task, context=None, **kwargs):
            pass
    
    class MockBrowserSkill(BaseSkill):
        def get_capabilities(self):
            return ["web_interaction"]
        def execute(self, task, context=None, **kwargs):
            pass
    
    return [MockCommandSkill(), MockBrowserSkill()]


def demo_auto_hint_system():
    """Demonstrate auto hint system functionality"""
    print("=== Auto Hint System Demo ===\n")
    
    # Initialize system
    print("1. Initializing Auto Hint System...")
    try:
        system = AutoHintSystem(enable_persistence=True)
        print("✓ System initialized successfully\n")
    except Exception as e:
        print(f"⚠ Warning: Could not initialize system (likely missing API key): {e}")
        print("  System will run in persistence-only mode for demo purposes\n")
        system = AutoHintSystem(enable_persistence=False)
        system.persistence = Mock()
        system.persistence.save_hint = Mock(return_value=True)
        system.persistence.load_hints_for_skill = Mock(return_value=[])
        system.persistence.load_all_hints = Mock(return_value={})
        system.persistence.get_hint_statistics = Mock(return_value={"total_hints": 0})
        system.analyzer = Mock()
        system.generator = Mock()
        system.generator.generate_hints_from_analysis = Mock(return_value=[])
        print("✓ System initialized in demo mode\n")
    
    # Create mock data
    print("2. Creating mock execution history...")
    history = create_mock_execution_history()
    skills = create_mock_skills()
    print(f"✓ Created {len(history)} execution steps with {len(skills)} skills\n")
    
    # Show initial statistics
    print("3. Initial system statistics:")
    stats = system.get_system_statistics()
    print(f"   - Enabled: {stats['enabled']}")
    print(f"   - Task completions: {stats['task_completion_count']}")
    print(f"   - Analysis interval: {stats['analysis_interval']}")
    if 'total_hints' in stats:
        print(f"   - Total hints: {stats['total_hints']}")
    print()
    
    # Process task completion
    print("4. Processing task completion (triggering hint analysis)...")
    success = system.process_task_completion(
        history, 
        skills, 
        "Find and analyze Python files in the project"
    )
    print(f"✓ Task completion processed: {'Hints generated' if success else 'No hints generated'}\n")
    
    # Show updated statistics
    print("5. Updated system statistics:")
    stats = system.get_system_statistics()
    if 'total_hints' in stats:
        print(f"   - Total hints: {stats['total_hints']}")
        print(f"   - Hints by skill: {stats.get('hints_by_skill', {})}")
        print(f"   - Hints by category: {stats.get('hints_by_category', {})}")
    print()
    
    # Show generated hints
    print("6. Generated hints:")
    all_hints = system.get_all_hints()
    
    if not all_hints:
        print("   No hints generated yet (need more execution history)")
        print("   Try running more tasks to build up the hint database")
    else:
        for skill_name, hints in all_hints.items():
            print(f"   Hints for {skill_name}:")
            for i, hint in enumerate(hints, 1):
                metadata = hint.get("metadata", {})
                content = hint.get("content", "")
                print(f"     {i}. {metadata.get('title', 'Untitled')}")
                print(f"        Category: {metadata.get('category', 'Unknown')}")
                print(f"        Content: {content[:100]}{'...' if len(content) > 100 else ''}")
                print()
    
    # Show skill-specific hints
    print("7. Hints for CommandSkill:")
    command_hints = system.get_hints_for_skill("CommandSkill", max_hints=2)
    if command_hints:
        for i, hint in enumerate(command_hints, 1):
            metadata = hint.get("metadata", {})
            print(f"   {i}. {metadata.get('title', 'Hint')}")
    else:
        print("   No hints available for CommandSkill")
    
    print("\n=== Demo Complete ===")
    print("\nNext steps:")
    print("- Run more tasks to generate more hints")
    print("- Use 'ask auto-hint status' to check system status")
    print("- Use 'ask auto-hint show' to view generated hints")
    print("- The system will automatically improve over time!")


if __name__ == "__main__":
    demo_auto_hint_system()