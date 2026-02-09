# LLM Client

The LLM Client module handles communication with language models.

## Overview

The LLM client provides an abstraction layer for different AI providers, currently supporting OpenAI's GPT models.

## Module Structure

Located in: [`alpha_bot/llm/`](https://github.com/fssqawj/alpha-bot/tree/main/alpha_bot/llm)

- `base.py` - Abstract base class
- `openai_client.py` - OpenAI implementation
- `mock.py` - Demo mode simulation

## Base Interface

```python
from abc import ABC, abstractmethod

class LLMClient(ABC):
    """Abstract interface for LLM providers"""
    
    @abstractmethod
    def generate_command(self, task: str, context: dict) -> str:
        """Generate shell command from task description"""
        pass
    
    @abstractmethod
    def analyze_safety(self, command: str) -> dict:
        """Analyze command for safety concerns"""
        pass
    
    @abstractmethod
    def is_task_complete(self, task: str, results: list) -> bool:
        """Determine if task is complete"""
        pass
```

## OpenAI Client

### Initialization

```python
from alpha_bot.llm import OpenAIClient

client = OpenAIClient(
    api_key="your-api-key",
    model="gpt-4",
    base_url="https://api.openai.com/v1"  # Optional
)
```

### Methods

#### `generate_command(task, context)`

Generate a shell command from natural language task.

**Parameters:**
- `task` (str): Natural language task description
- `context` (dict): Execution context including history

**Returns:**
- `str`: Shell command to execute

**Example:**

```python
command = client.generate_command(
    task="list all Python files",
    context={"cwd": "/home/user/project"}
)
# Returns: "find . -name '*.py'"
```

#### `analyze_safety(command)`

Analyze a command for potential dangers.

**Parameters:**
- `command` (str): Shell command to analyze

**Returns:**
- `dict`: Safety analysis with risk level and explanation

**Example:**

```python
analysis = client.analyze_safety("rm -rf /tmp/*")
# Returns: {
#     "is_dangerous": True,
#     "risk_level": "high",
#     "explanation": "Recursive deletion without confirmation",
#     "alternatives": ["rm -ri /tmp/*", "mv /tmp/* ~/.Trash/"]
# }
```

## Mock Client (Demo Mode)

For testing without API calls:

```python
from alpha_bot.llm import MockClient

client = MockClient()
command = client.generate_command("list files", {})
# Returns simulated responses
```

## Configuration

### Environment Variables

```bash
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1  # Optional
MODEL_NAME=gpt-4  # Optional, defaults to gpt-4
```

### Custom Provider

To add a new provider:

```python
from alpha_bot.llm.base import LLMClient

class CustomProvider(LLMClient):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def generate_command(self, task: str, context: dict) -> str:
        # Your implementation
        pass
    
    def analyze_safety(self, command: str) -> dict:
        # Your implementation
        pass
```

## See Also

- [Agent API](agent.md)
- [Executor API](executor.md)
- [Architecture](../development/architecture.md)
