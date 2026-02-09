# UI Components

The UI module provides a beautiful, interactive terminal interface.

## Overview

Ask-Shell uses the [Rich](https://github.com/Textualize/rich) library to create a modern, colorful terminal experience.

## Location

[`alpha_bot/ui/console.py`](https://github.com/fssqawj/alpha-bot/blob/main/alpha_bot/ui/console.py)

## Components

### Console Manager

The main console interface for user interaction.

```python
from alpha_bot.ui import Console

console = Console()
```

### Display Methods

#### Show Thinking Process

```python
console.show_thinking("Analyzing your request...")
```

Displays AI's reasoning in real-time with animated spinner.

#### Display Command

```python
console.display_command("find . -name '*.py'")
```

Shows generated command with syntax highlighting.

#### Show Results

```python
console.show_result(
    stdout="file1.py\nfile2.py",
    stderr="",
    exit_code=0
)
```

Displays command execution results in formatted panels.

#### Confirmation Prompt

```python
response = console.confirm_execution("rm old_file.txt")
# Returns: 'y', 'n', 'e', or 'q'
```

Interactive prompt with options to execute, skip, edit, or quit.

#### Show Warning

```python
console.show_warning(
    command="rm -rf logs/",
    reason="Recursive deletion cannot be undone",
    alternatives=["rm -i logs/*", "mv logs/ ~/.Trash/"]
)
```

Displays safety warnings with explanations and alternatives.

## Styling

### Colors

```python
# Info (blue)
console.print("[blue]ℹ️ Information[/blue]")

# Success (green)
console.print("[green]✅ Success![/green]")

# Warning (yellow)
console.print("[yellow]⚠️ Warning[/yellow]")

# Error (red)
console.print("[red]❌ Error[/red]")
```

### Panels

```python
from rich.panel import Panel

panel = Panel(
    "Content here",
    title="Panel Title",
    border_style="blue"
)
console.print(panel)
```

### Progress Animation

```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("Processing...", total=100)
    for i in range(100):
        # Do work
        progress.update(task, advance=1)
```

## Example Usage

### Complete Interaction Flow

```python
from alpha_bot.ui import Console

console = Console()

# 1. Show thinking
console.show_thinking("Analyzing task...")

# 2. Display generated command
command = "find . -name '*.log'"
console.display_command(command)

# 3. Get user confirmation
response = console.confirm_execution(command)

if response == 'y':
    # 4. Show execution
    with console.status("Executing..."):
        result = execute_command(command)
    
    # 5. Display results
    console.show_result(
        stdout=result.stdout,
        stderr=result.stderr,
        exit_code=result.exit_code
    )
elif response == 'e':
    # Edit command
    edited = console.edit_command(command)
    # ...
```

### Custom Formatting

```python
from rich.syntax import Syntax

# Syntax highlighted code
code = Syntax(
    "def hello():\n    print('world')",
    "python",
    theme="monokai",
    line_numbers=True
)
console.print(code)
```

### Tables

```python
from rich.table import Table

table = Table(title="Command History")
table.add_column("Command", style="cyan")
table.add_column("Status", style="green")

table.add_row("ls -la", "✓")
table.add_row("git status", "✓")

console.print(table)
```

## Visual Elements

### Icons

- 💭 Thinking/Analysis
- ⚙️ Command/Execution
- ✅ Success
- ❌ Error
- ⚠️ Warning
- 📊 Results
- 🔒 Security/Safety

### Spinners

```python
from rich.spinner import Spinner

spinner = Spinner("dots", text="Processing...")
```

## See Also

- [Rich Documentation](https://rich.readthedocs.io/)
- [Agent API](agent.md)
- [User Guide](../user-guide/basic-usage.md)
