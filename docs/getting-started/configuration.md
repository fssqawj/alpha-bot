# Configuration

Ask-Shell can be configured through environment variables and command-line arguments.

## Environment Variables

### Required Configuration

#### `OPENAI_API_KEY`

Your OpenAI API key for accessing GPT models.

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

**How to get it:**

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new secret key

### Optional Configuration

#### `OPENAI_API_BASE`

Custom API endpoint URL (useful for proxy or compatible APIs).

```bash
OPENAI_API_BASE=https://api.openai.com/v1
```

**Use cases:**

- Using a proxy service
- Azure OpenAI Service
- Compatible API providers (e.g., LocalAI, Ollama with OpenAI compatibility)

#### `MODEL_NAME`

The language model to use for generating commands.

```bash
MODEL_NAME=gpt-4
```

**Supported models:**

- `gpt-4` (default, recommended)
- `gpt-4-turbo`
- `gpt-3.5-turbo` (faster, less accurate)

!!! tip
    GPT-4 is recommended for best results, especially for complex multi-step tasks and safety analysis.

## Configuration File

### Using .env File

The recommended way to configure Ask-Shell is using a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit with your preferred editor
nano .env
```

Example `.env` file:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4
```

### Environment Variable Priority

Ask-Shell loads configuration in this order (later overrides earlier):

1. Default values
2. `.env` file in current directory
3. System environment variables
4. Command-line arguments

## Command-Line Arguments

### Task Execution

```bash
ask [OPTIONS] "task description"
```

### Available Options

#### `-i, --interactive`

Start interactive mode for continuous task execution.

```bash
ask -i
```

#### `-a, --auto`

Auto execution mode - skips confirmation prompts.

```bash
ask -a "your task"
```

!!! warning
    Use with caution! Commands will execute immediately without confirmation.

#### `-d, --demo`

Demo mode using simulated AI (no API key required).

```bash
ask -d "create a test folder"
```

#### `-w, --workdir PATH`

Specify working directory for command execution.

```bash
ask -w /path/to/project "list all files"
```

#### `--help`

Show help message and exit.

```bash
ask --help
```

## Advanced Configuration

### Using Azure OpenAI

```bash
OPENAI_API_BASE=https://YOUR-RESOURCE.openai.azure.com/
OPENAI_API_KEY=your-azure-api-key
MODEL_NAME=your-deployment-name
```

### Using Compatible APIs

Many LLM providers offer OpenAI-compatible APIs:

```bash
# Example: LocalAI
OPENAI_API_BASE=http://localhost:8080/v1
OPENAI_API_KEY=not-needed
MODEL_NAME=gpt-4

# Example: Ollama (with OpenAI compatibility)
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_API_KEY=not-needed
MODEL_NAME=llama2
```

!!! note
    Results may vary with different models. GPT-4 is tested and recommended.

### Proxy Configuration

If you need to use a proxy:

```bash
# System-level proxy
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# Then run Ask-Shell normally
ask "your task"
```

## Configuration Best Practices

### Security

!!! danger "API Key Security"
    - Never commit `.env` files to version control
    - Never share your API key publicly
    - Rotate keys regularly
    - Use environment variables in production

### Performance

- **Use GPT-4** for complex tasks and safety analysis
- **Use GPT-3.5-turbo** for simple, fast command generation
- **Enable auto mode** only for trusted, repetitive tasks

### Workflow

```bash
# Development
ask -i  # Interactive mode for exploring

# Production scripts
ask -a -w /var/app "deploy latest version"

# Testing
ask -d "test task"  # Demo mode, no API calls
```

## Troubleshooting

### API Key Issues

**Error: "Authentication failed"**

- Check your API key is correct
- Verify the key hasn't expired
- Ensure you have API credits available

**Error: "Rate limit exceeded"**

- Wait a few seconds and retry
- Upgrade your OpenAI plan for higher limits

### Connection Issues

**Error: "Connection timeout"**

- Check your internet connection
- Verify `OPENAI_API_BASE` URL is correct
- Check if you need proxy configuration

### Model Issues

**Error: "Model not found"**

- Verify `MODEL_NAME` is supported
- Check your OpenAI account has access to the model
- For Azure, ensure deployment name is correct

## Next Steps

- [Start using Ask-Shell](quick-start.md)
- [Learn about basic usage](../user-guide/basic-usage.md)
- [Explore safety features](../user-guide/safety.md)
