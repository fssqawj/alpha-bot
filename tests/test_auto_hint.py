"""Auto Hint System Tests"""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

from ask_shell.auto_hint.types import HintPattern, HintCategory, HintMetadata
from ask_shell.auto_hint.analyzer import ExecutionResultAnalyzer
from ask_shell.auto_hint.generator import HintGenerator
from ask_shell.auto_hint.persistence import HintPersistenceManager
from ask_shell.auto_hint.system import AutoHintSystem, get_auto_hint_system
from ask_shell.models.types import ExecutionResult, SkillResponse
from ask_shell.skills.base_skill import BaseSkill


class TestHintTypes(unittest.TestCase):
    """Test hint data types"""
    
    def test_hint_pattern_creation(self):
        """Test HintPattern creation and default values"""
        pattern = HintPattern(
            category=HintCategory.SUCCESS_PATTERN,
            skill_name="TestSkill",
            pattern_description="Test pattern"
        )
        
        self.assertEqual(pattern.category, HintCategory.SUCCESS_PATTERN)
        self.assertEqual(pattern.skill_name, "TestSkill")
        self.assertEqual(pattern.pattern_description, "Test pattern")
        self.assertEqual(pattern.success_rate, 0.0)
        self.assertEqual(pattern.frequency, 1)
        self.assertIsInstance(pattern.id, str)
    
    def test_hint_metadata_creation(self):
        """Test HintMetadata creation"""
        metadata = HintMetadata(
            title="Test Hint",
            category=HintCategory.BEST_PRACTICE,
            skill_name="TestSkill"
        )
        
        self.assertEqual(metadata.title, "Test Hint")
        self.assertEqual(metadata.category, HintCategory.BEST_PRACTICE)
        self.assertEqual(metadata.skill_name, "TestSkill")
        self.assertEqual(metadata.version, "1.0")
        self.assertEqual(metadata.usage_count, 0)
        self.assertEqual(metadata.effectiveness_score, 0.0)


class TestExecutionResultAnalyzer(unittest.TestCase):
    """Test execution result analyzer"""
    
    def setUp(self):
        self.analyzer = ExecutionResultAnalyzer()
    
    def test_analyze_empty_history(self):
        """Test analyzing empty history"""
        result = self.analyzer.analyze_history([], [])
        self.assertEqual(len(result.patterns), 0)
        self.assertEqual(len(result.success_patterns), 0)
        self.assertEqual(len(result.failure_patterns), 0)
    
    def test_analyze_simple_history(self):
        """Test analyzing simple execution history"""
        # Create mock execution results
        skill_response = Mock()
        skill_response.skill_name = "CommandSkill"
        
        results = [
            ExecutionResult(
                command="ls -la",
                returncode=0,
                stdout="file1.txt",
                stderr="",
                skill_response=skill_response
            ),
            ExecutionResult(
                command="pwd",
                returncode=0,
                stdout="/home/user",
                stderr="",
                skill_response=skill_response
            )
        ]
        
        mock_skill = Mock()
        mock_skill.name = "CommandSkill"
        
        analysis_result = self.analyzer.analyze_history(results, [mock_skill])
        
        # Should have some patterns even with minimal data
        self.assertIsInstance(analysis_result.patterns, list)
        self.assertIsInstance(analysis_result.skill_insights, dict)


class TestHintPersistenceManager(unittest.TestCase):
    """Test hint persistence manager"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.persistence = HintPersistenceManager(self.temp_dir)
    
    def test_save_and_load_hint(self):
        """Test saving and loading a hint"""
        hint_data = {
            "metadata": HintMetadata(
                title="Test Hint",
                category=HintCategory.BEST_PRACTICE,
                skill_name="TestSkill"
            ),
            "content": "This is a test hint content"
        }
        
        # Save hint
        success = self.persistence.save_hint(hint_data)
        self.assertTrue(success)
        
        # Load hints for skill
        hints = self.persistence.load_hints_for_skill("TestSkill")
        self.assertEqual(len(hints), 1)
        self.assertEqual(hints[0]["content"], "This is a test hint content")
    
    def test_load_all_hints(self):
        """Test loading all hints"""
        # Save multiple hints
        hint1 = {
            "metadata": HintMetadata(title="Hint 1", skill_name="SkillA"),
            "content": "Content 1"
        }
        hint2 = {
            "metadata": HintMetadata(title="Hint 2", skill_name="SkillB"),
            "content": "Content 2"
        }
        
        self.persistence.save_hint(hint1)
        self.persistence.save_hint(hint2)
        
        # Load all hints
        all_hints = self.persistence.load_all_hints()
        self.assertIn("SkillA", all_hints)
        self.assertIn("SkillB", all_hints)
        self.assertEqual(len(all_hints["SkillA"]), 1)
        self.assertEqual(len(all_hints["SkillB"]), 1)
    
    def test_hint_statistics(self):
        """Test getting hint statistics"""
        stats = self.persistence.get_hint_statistics()
        self.assertIn("total_hints", stats)
        self.assertIn("storage_path", stats)
        self.assertEqual(stats["total_hints"], 0)
        
        # Add a hint and check stats
        hint_data = {
            "metadata": HintMetadata(title="Test", skill_name="TestSkill"),
            "content": "Test content"
        }
        self.persistence.save_hint(hint_data)
        
        stats = self.persistence.get_hint_statistics()
        self.assertEqual(stats["total_hints"], 1)
        self.assertEqual(stats["hints_by_skill"]["TestSkill"], 1)


class TestAutoHintSystem(unittest.TestCase):
    """Test auto hint system"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.system = AutoHintSystem(enable_persistence=True, hints_path=self.temp_dir)
    
    def test_system_initialization(self):
        """Test system initialization"""
        self.assertTrue(self.system.enable_persistence)
        self.assertIsNotNone(self.system.analyzer)
        self.assertIsNotNone(self.system.generator)
        self.assertIsNotNone(self.system.persistence)
    
    def test_get_hints_for_skill(self):
        """Test getting hints for a skill"""
        hints = self.system.get_hints_for_skill("TestSkill")
        self.assertIsInstance(hints, list)
        # Should be empty initially
        self.assertEqual(len(hints), 0)
    
    def test_get_all_hints(self):
        """Test getting all hints"""
        all_hints = self.system.get_all_hints()
        self.assertIsInstance(all_hints, dict)
        # Should be empty initially
        self.assertEqual(len(all_hints), 0)
    
    def test_system_statistics(self):
        """Test getting system statistics"""
        stats = self.system.get_system_statistics()
        self.assertIn("enabled", stats)
        self.assertIn("task_completion_count", stats)
        self.assertIn("analysis_interval", stats)
    
    def test_global_system_instance(self):
        """Test global system instance"""
        system1 = get_auto_hint_system()
        system2 = get_auto_hint_system()
        self.assertIs(system1, system2)  # Should be the same instance


class TestSkillIntegration(unittest.TestCase):
    """Test integration with skills"""
    
    def test_base_skill_hints(self):
        """Test BaseSkill hints functionality"""
        class TestSkill(BaseSkill):
            def get_capabilities(self):
                return ["test"]
            
            def execute(self, task, context=None, **kwargs):
                return Mock()
        
        skill = TestSkill()
        
        # Should have auto hint system
        self.assertIsNotNone(skill.auto_hint_system)
        
        # Should have hints methods
        self.assertTrue(hasattr(skill, '_build_hints_info'))
        self.assertTrue(hasattr(skill, '_load_auto_hints'))


if __name__ == '__main__':
    unittest.main()