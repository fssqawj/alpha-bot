# Basic Usage

Learn the fundamentals of using Alpha-Bot for everyday tasks.

## Command Structure

### Standard Format

```bash
ask [OPTIONS] "task description"
```

### Components

- **Options**: Flags that modify behavior (optional)
- **Task Description**: Natural language description of what you want to do

## Simple Tasks

### File Operations

List files with specific criteria:

```bash
ask "show all files modified in the last 24 hours"
ask "find files larger than 10MB"
ask "list all PDF files recursively"
```

### Search Operations

```bash
ask "find all files containing the word 'error'"
ask "search for TODO comments in Python files"
ask "locate all shell scripts in this directory"
```

### System Information

```bash
ask "show current disk usage"
ask "display running processes sorted by memory"
ask "check system uptime and load average"
```

## Multi-Step Tasks

This is where Alpha-Bot excels - handling complex workflows automatically.

### File Organization

```bash
ask "organize project files: create folders for docs, tests, and source code, then move files accordingly"
```

Ask-Shell will:

1. Analyze current file structure
2. Create necessary directories
3. Move files to appropriate locations
4. Verify the organization

### Development Workflows

```bash
ask "find all Python files, count their lines, and create a summary report"
```

The agent will:

1. Find all .py files
2. Count lines in each file
3. Generate a summary
4. Save to a report file

### Git Operations

```bash
ask "stage all changes, commit with a descriptive message, and push to origin"
```

## Understanding AI Responses

### Thinking Process

When you give Alpha-Bot a task, you'll see:

```
💭 Analyzing task...
   Understanding: Need to list all Python files in current directory
   Approach: Use find command with .py extension filter
   Safety: Low risk operation, no destructive actions
```

### Command Preview

Before execution, you'll see the proposed command:

```
⚙️ Proposed command:
   find . -name "*.py" -type f

   Execute this command? [Y/n/e/q]:
```

Options:

- `Y` (Yes): Execute the command
- `n` (No): Skip this command and continue
- `e` (Edit): Modify the command before execution
- `q` (Quit): Exit Ask-Shell

### Execution Results

After running, you'll see structured output:

```
✅ Command executed successfully

📊 Results:
./alpha_bot/cli.py
./alpha_bot/agent.py
./setup.py

💭 Next step: Task completed
```

## Interactive Mode

### Starting Interactive Mode

```bash
ask -i
```

### Benefits

- **Context retention**: AI remembers previous commands and results
- **Faster iteration**: No need to restart for each task
- **Natural conversation**: Reference previous steps naturally

### Example Session

```
Alpha-Bot > list all log files
[... shows log files ...]

Alpha-Bot > count the lines in each of them
[... analyzes the files from previous command ...]

Alpha-Bot > archive the ones older than 7 days
[... uses context from both previous commands ...]

Alpha-Bot > exit
```

## Working with Different Directories

### Specify Directory

```bash
ask -w /var/log "find error messages in syslog"
```

### Multiple Directories

In interactive mode:

```
Alpha-Bot > cd /var/log
Alpha-Bot > analyze error logs
Alpha-Bot > cd /home/user
Alpha-Bot > backup configuration files
```

## Best Practices

### Writing Good Task Descriptions

**Good Examples:**

```bash
✅ "find all JavaScript files and check for console.log statements"
✅ "create a backup of database files with timestamp"
✅ "organize downloads folder by file extension"
```

**Less Effective:**

```bash
❌ "do something with files"  # Too vague
❌ "ls *.js"  # Just write the command directly if you know it
❌ "files"  # Not enough context
```

### Task Description Tips

1. **Be specific**: Include file types, criteria, and desired outcome
2. **Use natural language**: No need to think in command syntax
3. **Describe the goal**: What you want to achieve, not how
4. **Provide context**: Mention relevant details (timeframes, sizes, etc.)

### Safety Considerations

Always review commands before execution:

- Check the proposed command makes sense
- Verify it operates on the right files/directories
- Be cautious with destructive operations (delete, modify, etc.)

### Efficiency Tips

**Use auto mode for safe, repetitive tasks:**

```bash
ask -a "count lines of code"  # Read-only operation
```

**Use interactive mode for exploratory work:**

```bash
ask -i
# Then explore step by step with AI assistance
```

**Use working directory for focused tasks:**

```bash
ask -w ~/projects/myapp "run tests"
```

## Common Patterns

### Find and Process

```bash
ask "find all markdown files and convert them to PDF"
ask "locate all images and resize them to 800px width"
```

### Analyze and Report

```bash
ask "analyze log files and count error occurrences by type"
ask "check all scripts for potential security issues"
```

### Batch Operations

```bash
ask "rename all .jpeg files to .jpg"
ask "compress all log files older than 30 days"
```

### System Maintenance

```bash
ask "clean up temporary files and clear cache"
ask "find and remove duplicate files in downloads"
```

## Troubleshooting Common Issues

### AI Misunderstands Task

**Problem**: AI generates wrong command

**Solution**: 

1. Be more specific in your description
2. Use the edit option to correct the command
3. In interactive mode, clarify with follow-up

### Command Needs Modification

**Problem**: Command is almost right but needs tweaking

**Solution**: Choose 'e' (edit) when prompted and modify before execution

### Task Too Complex

**Problem**: AI struggles with very complex multi-part tasks

**Solution**:

1. Break into smaller sub-tasks
2. Use interactive mode to guide step-by-step
3. Provide more context and examples

## Next Steps

- [Explore advanced features](advanced-features.md)
- [Learn about safety mechanisms](safety.md)
- [See real-world examples](examples.md)
