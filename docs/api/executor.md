# Executor

The Executor module safely executes shell commands with safety validation.

## Overview

The `ShellExecutor` class handles command execution, safety checks, and result parsing.

## Location

[`ask_shell/executor/shell.py`](https://github.com/fssqawj/ask-shell/blob/main/ask_shell/executor/shell.py)

## Class: ShellExecutor

### Initialization

```python
from ask_shell.executor import ShellExecutor

executor = ShellExecutor(workdir="/path/to/dir")  # Optional workdir
```

### Methods

#### `execute(command, timeout=30)`

Execute a shell command safely.

**Parameters:**
- `command` (str): Shell command to execute
- `timeout` (int): Maximum execution time in seconds

**Returns:**
- `dict`: Execution result with stdout, stderr, exit_code

**Example:**

```python
result = executor.execute("ls -la")
# Returns: {
#     "stdout": "...",
#     "stderr": "",
#     "exit_code": 0,
#     "success": True
# }
```

#### `is_dangerous(command)`

Check if a command is dangerous.

**Parameters:**
- `command` (str): Command to check

**Returns:**
- `bool`: True if dangerous

**Example:**

```python
if executor.is_dangerous("rm -rf /"):
    print("Blocked!")
# Returns: True
```

#### `validate_command(command)`

Validate command syntax and safety.

**Parameters:**
- `command` (str): Command to validate

**Returns:**
- `tuple`: (is_valid, error_message)

## Safety Features

### Dangerous Pattern Blacklist

```python
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/',           # Recursive deletion of root
    r'dd\s+if=/dev/zero',       # Disk wipe
    r'mkfs\.',                  # Format filesystem
    r':\(\)\{.*:\|:.*\}',      # Fork bomb
    r'wget.*\|\s*sh',          # Download and execute
    r'curl.*\|\s*bash',        # Download and execute
]
```

### Validation Flow

```
Command Input
    │
    ├─> Blacklist Check
    │       │
    │       └─> Match? → BLOCK
    │
    ├─> Syntax Validation
    │       │
    │       └─> Invalid? → ERROR
    │
    ├─> AI Safety Analysis (optional)
    │       │
    │       └─> Dangerous? → WARN
    │
    └─> Execute
```

## Usage Examples

### Basic Execution

```python
from ask_shell.executor import ShellExecutor

executor = ShellExecutor()

# Execute command
result = executor.execute("echo 'Hello World'")

if result["success"]:
    print(result["stdout"])
else:
    print(f"Error: {result['stderr']}")
```

### With Safety Check

```python
command = "rm -rf /tmp/old_files"

# Check safety first
if executor.is_dangerous(command):
    print("⚠️ Dangerous command detected!")
    # Get user confirmation
else:
    result = executor.execute(command)
```

### Custom Working Directory

```python
executor = ShellExecutor(workdir="/var/www/myapp")

# All commands execute in /var/www/myapp
executor.execute("ls -la")
```

### With Timeout

```python
# Long-running command with 60s timeout
result = executor.execute(
    "python long_script.py",
    timeout=60
)
```

## Error Handling

```python
try:
    result = executor.execute("invalid-command")
    if not result["success"]:
        print(f"Command failed: {result['stderr']}")
except TimeoutError:
    print("Command timed out")
except PermissionError:
    print("Permission denied")
```

## See Also

- [Agent API](agent.md)
- [Safety Features](../user-guide/safety.md)
- [Architecture](../development/architecture.md)
