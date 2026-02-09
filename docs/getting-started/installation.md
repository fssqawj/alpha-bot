# Installation

Alpha-Bot can be installed in multiple ways. Choose the method that best fits your workflow.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- OpenAI API Key (or compatible API endpoint)
- For browser automation: Chrome or Chromium browser installed on your system

## Installation Methods

### Method 1: Development Mode (Recommended)

This method is ideal if you want to contribute to the project or modify the code.

```bash
# Clone the repository
git clone https://github.com/fssqawj/alpha-bot.git
cd alpha-bot

# Install in development mode
pip install -e .
```

After installation, you can use both `alpha-bot` and `ask` commands directly:

```bash
ask "list all Python files in current directory"
```

### Method 2: Install from PyPI

The simplest way to install Alpha-Bot is from PyPI:

```bash
pip install alpha-bot
```

This will install the latest stable version and make `alpha-bot` and `ask` commands available globally.

### Method 3: Install Dependencies Only

If you prefer to run the script directly without installation:

```bash
# Clone the repository
git clone https://github.com/fssqawj/alpha-bot.git
cd alpha-bot

# Install dependencies
pip install -r requirements.txt
```

Then run using:

```bash
python ask_shell/cli.py "your task here"
```

## Verifying Installation

To verify that Alpha-Bot is installed correctly:

```bash
# Check version
ask --help

# Or if installed via PyPI
alpha-bot --help
```

You should see the help message with available options.

## Next Steps

- [Configure your API Key](configuration.md)
- [Quick Start Guide](quick-start.md)
- [Learn about basic usage](../user-guide/basic-usage.md)

## Troubleshooting

### Command not found

If you get "command not found" error after installation:

1. Make sure pip's bin directory is in your PATH
2. Try using `python -m ask_shell.cli` instead
3. Reinstall with `pip install --force-reinstall alpha-bot`

### Permission denied

If you encounter permission errors during installation:

```bash
# Use user installation
pip install --user alpha-bot

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install alpha-bot
```

### Import errors

If you get import errors:

1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. For browser automation, install Playwright: `playwright install chromium`
3. Check your Python version: `python --version` (should be 3.7+)
4. Try creating a fresh virtual environment
