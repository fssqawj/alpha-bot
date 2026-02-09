# Auto Hint System Documentation

## Overview

The Auto Hint System automatically extracts and generates helpful hints from execution history, enabling the system to learn from both successful and failed executions. This allows Ask-Shell to become more efficient and effective over time by avoiding unnecessary trial and error.

## System Architecture

The system consists of several key components:

1. **ExecutionResultAnalyzer** - Analyzes execution history to discover patterns
2. **HintGenerator** - Generates human-readable hints from discovered patterns using LLM
3. **HintPersistenceManager** - Manages storage and retrieval of generated hints
4. **AutoHintSystem** - Main orchestrator that integrates all components

## Key Features

### Pattern Discovery
- Analyzes command execution patterns and their success rates
- Identifies common error patterns and failure modes
- Extracts successful execution sequences
- Categorizes patterns by skill usage

### Automatic Hint Generation
- Generates contextual hints using LLM
- Creates different types of hints:
  - Success patterns (what works well)
  - Failure patterns (common pitfalls)
  - Best practices (recommended approaches)
  - Troubleshooting guides (how to fix issues)

### Persistent Storage
- Stores hints in organized directory structure
- Maintains metadata for tracking effectiveness
- Provides cache mechanism for performance
- Supports cleanup of old/ineffective hints

### Skill Integration
- Automatically integrates with all existing skills
- Provides hints context to LLM during execution
- Tracks hint usage and effectiveness
- Supports both static and auto-generated hints

## Configuration

The system can be configured through environment variables:

```bash
# Enable/disable the system
export AUTO_HINT_ENABLED=true

# Persistence settings
export AUTO_HINT_PERSISTENCE=true
export AUTO_HINT_STORAGE_PATH=/custom/path/to/hints

# Analysis parameters
export AUTO_HINT_MIN_HISTORY=3
export AUTO_HINT_ANALYSIS_INTERVAL=5
export AUTO_HINT_MIN_CONFIDENCE=0.7
export AUTO_HINT_SUCCESS_RATE=0.8

# Generation limits
export AUTO_HINT_MAX_PER_CATEGORY=5
export AUTO_HINT_MAX_PER_SKILL=3

# Cleanup settings
export AUTO_HINT_AUTO_CLEANUP=true
export AUTO_HINT_CLEANUP_AGE=30
export AUTO_HINT_CLEANUP_EFFECTIVENESS=0.3
```

## Usage

### Automatic Usage
The system works automatically in the background:

1. **Task Completion**: When tasks complete (successfully or unsuccessfully), the system analyzes the execution history
2. **Pattern Analysis**: Identifies patterns in the execution steps
3. **Hint Generation**: Automatically generates relevant hints
4. **Storage**: Saves hints for future use
5. **Integration**: Skills automatically load relevant hints during execution

### CLI Commands
The system provides CLI commands for management:

```bash
# Show system status
python -m ask_shell auto-hint status

# Show generated hints
python -m ask_shell auto-hint show --skill BrowserSkill

# Configure system
python -m ask_shell auto-hint configure --enable --min-history 5

# Clean up old hints
python -m ask_shell auto-hint cleanup --max-age 60 --min-effectiveness 0.5

# Add manual hint
python -m ask_shell auto-hint add-hint --skill BrowserSkill --title "Login Pattern" --content "Always check for login forms first" --category best_practice
```

## Directory Structure

Generated hints are stored in organized directories:

```
ask_shell/skills/hints_generated/
├── browser/          # Browser skill hints
├── command/          # Command skill hints
├── general/          # General hints
├── wechat/           # WeChat skill hints
├── feishu/           # Feishu skill hints
├── ppt/              # PPT skill hints
├── image/            # Image skill hints
└── direct_llm/       # Direct LLM skill hints
```

Each hint is stored as a markdown file with metadata.

## Integration with Skills

### BaseSkill Integration
All skills automatically inherit hint support through the BaseSkill class:

```python
class MySkill(BaseSkill):
    def execute(self, task, context, **kwargs):
        # Hints are automatically loaded and provided to LLM
        hints_info = self._build_hints_info()
        # Use hints_info in your LLM prompts
        # ...
```

### Manual Integration
Skills can also manually access hints:

```python
from ask_shell.auto_hint import get_auto_hint_system

# Get hints for specific skill
auto_hint_system = get_auto_hint_system()
hints = auto_hint_system.get_hints_for_skill("BrowserSkill", max_hints=3)

# Record hint usage
for hint in hints:
    hint_id = hint["metadata"]["id"]
    auto_hint_system.record_hint_usage(hint_id)
```

## Effectiveness Tracking

The system tracks hint effectiveness:

- **Usage Count**: How many times a hint was used
- **Effectiveness Score**: 0.0-1.0 rating based on user feedback
- **Automatic Cleanup**: Removes old or ineffective hints periodically

## Best Practices

### For Users
- Allow the system to run for several tasks to build up hints
- The system works best with 3+ execution steps per task
- Review generated hints periodically to ensure quality
- Provide feedback through effectiveness scoring

### For Developers
- Use consistent skill naming conventions
- Provide clear task descriptions for better analysis
- Implement proper error handling in skills
- Consider the hint system when designing new skills

## Example Workflow

1. **User runs a task**: "Browse to GitHub and find the latest Python releases"
2. **BrowserSkill executes**: Multiple steps to navigate and extract information
3. **Task completes**: System analyzes the execution history
4. **Pattern discovered**: Successful sequence of navigation and data extraction
5. **Hint generated**: "For GitHub browsing tasks, first navigate to the target page, then look for release sections"
6. **Future tasks**: When similar tasks are encountered, the hint is automatically provided to the LLM
7. **Improved performance**: The system executes more efficiently with fewer trial and error steps

## Troubleshooting

### Common Issues

**No hints generated**: 
- Ensure sufficient execution history (minimum 3 steps)
- Check that persistence is enabled
- Verify LLM API is working

**Hints not loading in skills**:
- Check that skills inherit from BaseSkill
- Verify hint system is properly initialized
- Ensure hint files are readable

**Performance issues**:
- Adjust analysis interval to reduce frequency
- Enable caching for better performance
- Clean up old hints regularly

### Debugging

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

Planned improvements:
- Multi-task pattern recognition
- Cross-skill hint sharing
- Advanced effectiveness metrics
- User feedback integration
- Hint versioning and updates