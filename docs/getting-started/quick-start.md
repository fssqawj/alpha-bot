# Quick Start

Get started with Ask-Shell in 5 minutes!

## 1. Configure API Key

Before using Ask-Shell, you need to configure your OpenAI API Key.

### Using .env file (Recommended)

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=your-api-key-here
```

### Using environment variable

```bash
export OPENAI_API_KEY=your-api-key-here
```

## 2. Run Your First Task

### Simple Command

Try a simple file listing task:

```bash
ask "list all Python files in current directory"
```

Ask-Shell will:

1. 💭 Analyze your request
2. 🔨 Generate the appropriate command
3. ⚠️ Ask for confirmation (showing the command)
4. ✅ Execute and show results

### Complex Multi-Step Task

This is where Ask-Shell shines:

```bash
ask "organize this project: create docs, tests, and src folders, then move files accordingly"
```

Watch as Ask-Shell:

- **Step 1**: Analyzes current directory structure
- **Step 2**: Creates necessary folders
- **Step 3**: Moves files to appropriate locations
- **Step 4**: Verifies the organization
- ✓ **Complete**: Task finished!

## 3. Try Different Modes

### Interactive Mode

Stay in a continuous session:

```bash
ask -i
```

```
Ask-Shell > list files in current directory
[... executes ...]
Ask-Shell > create a test file named hello.txt
[... executes ...]
Ask-Shell > exit
```

### Auto Mode

Skip confirmations for faster execution:

```bash
ask -a "count lines of code in current directory"
```

!!! warning
    Use auto mode carefully - it will execute commands without asking for confirmation!

### Demo Mode

Try Ask-Shell without an API Key:

```bash
ask -d "create a test folder"
```

The AI will be simulated, showing you the interface and workflow.

## 4. Working Directory

Execute tasks in a different directory:

```bash
ask -w /path/to/project "find all TODO comments"
```

## Example Workflows

### Development Tasks

```bash
# Find and organize
ask "find all .log files older than 7 days and move to archive"

# Git workflow
ask "commit all changes with a meaningful message and push to origin"

# Code analysis
ask "find all TODO comments in Python files and create a summary"
```

### System Maintenance

```bash
# Disk cleanup
ask "find and list all files larger than 100MB"

# Process management
ask "show all running Python processes with their memory usage"

# Backup
ask "create a timestamped backup of this directory"
```

### File Organization

```bash
# Sort by type
ask "organize downloads folder by file type"

# Cleanup
ask "find and remove all .pyc files in this project"

# Search
ask "find all files containing 'error' in their content"
```

## Understanding the Output

Ask-Shell provides rich visual feedback:

1. **💭 Thinking Process** - See the AI's reasoning in real-time
2. **⚙️ Command Preview** - Review the command before execution
3. **⚠️ Safety Warnings** - Get alerted about dangerous operations
4. **✨ Syntax Highlighting** - Commands are beautifully formatted
5. **📊 Results** - Clear output from command execution

## Safety Features

Ask-Shell protects you with:

- 🛡️ **AI-powered danger detection** - Understands context
- 🚫 **Command blacklist** - Blocks catastrophic commands
- ✋ **Interactive confirmation** - You always have final say
- ✏️ **Command editing** - Modify before execution

## Next Steps

- [Learn about configuration options](configuration.md)
- [Explore advanced features](../user-guide/advanced-features.md)
- [See more examples](../user-guide/examples.md)
- [Understand safety features](../user-guide/safety.md)

## Pro Tips

!!! tip "Complex Tasks"
    The more complex your task, the more Ask-Shell's advantages shine! Don't hesitate to describe multi-step workflows.

!!! tip "Natural Language"
    Write naturally! "I need to..." works just as well as "do this..."

!!! tip "Context Matters"
    Ask-Shell remembers the conversation in interactive mode - you can reference previous commands!
