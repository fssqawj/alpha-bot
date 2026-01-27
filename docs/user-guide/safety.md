# Safety Features

Ask-Shell prioritizes your system's safety with multiple protection layers.

## Safety Philosophy

> **"Trust, but verify"** - Give AI autonomy, but keep humans in control of critical decisions.

Ask-Shell is designed to be:

- **Proactive**: Detect dangers before execution
- **Transparent**: Explain why something is dangerous
- **Controllable**: Let you make the final decision
- **Educational**: Help you learn safer alternatives

## Protection Layers

### Layer 1: AI-Powered Danger Detection

The most intelligent layer - GPT-4 analyzes each command for potential risks.

#### How It Works

Before executing any command, the AI evaluates:

1. **Intent**: What is the command trying to do?
2. **Scope**: What files/systems will be affected?
3. **Reversibility**: Can the action be undone?
4. **Risk Level**: Low, Medium, High, Critical

#### Example Analysis

**Command**: `rm -rf logs/`

**AI Analysis**:

```
⚠️ DANGER: HIGH RISK DETECTED

Command: rm -rf logs/
Risk Level: HIGH

Why dangerous:
- Recursive deletion (-rf) cannot be undone
- Operates on entire directory
- No confirmation for individual files
- Could delete important log files needed for debugging

Safer alternatives:
1. Use -i flag: rm -ri logs/
2. Move to trash: mv logs/ ~/.Trash/
3. Archive first: tar -czf logs-backup.tar.gz logs/ && rm -rf logs/

Proceed anyway? [y/N]:
```

#### Detection Capabilities

The AI understands context and can detect:

**Direct dangers:**

- File deletion (`rm`, `dd`)
- System modification (`chmod 777`, `chown`)
- Disk operations (`mkfs`, `fdisk`)
- Network risks (`wget | sh`, `curl | bash`)

**Subtle risks:**

- Recursive operations without limits
- Commands with wildcards in dangerous locations
- Piping to shell interpreters
- Operations on system directories

**Context-aware evaluation:**

```bash
# Same command, different context
rm temp.txt        # ✓ Low risk - single temp file
rm *.txt           # ⚠️ Medium risk - multiple files
rm -rf /var/*      # 🚨 Critical - system directory
```

### Layer 2: Command Blacklist

Hardcoded protection against catastrophic operations that should **never** be executed.

#### Blacklisted Patterns

```python
DANGEROUS_PATTERNS = [
    # Filesystem destruction
    r'rm\s+-rf\s+/',
    r'rm\s+-fr\s+/',
    r'rm\s+.*\s+/',
    
    # Disk operations
    r'dd\s+if=/dev/zero',
    r'dd\s+.*of=/dev/sd',
    r'mkfs\.',
    
    # Fork bombs
    r':\(\)\{.*:\|:.*\}',
    r'\.\/\.\/.*',
    
    # Download and execute
    r'wget.*\|\s*sh',
    r'curl.*\|\s*bash',
    r'curl.*\|\s*python',
    
    # System file modification
    r'chmod\s+777\s+/',
    r'chown.*:\s+/',
]
```

#### Behavior

When blacklisted command detected:

```
🚨 BLOCKED: CATASTROPHIC COMMAND DETECTED

Command: rm -rf /
Status: EXECUTION DENIED

This command is in the hardcoded blacklist and cannot be executed
through Ask-Shell under any circumstances.

Why: Could destroy your entire system
Alternative: Please specify the exact directory to delete
```

### Layer 3: Interactive Confirmation

You always have the final say before any command executes.

#### Confirmation Prompt

```
⚙️ Proposed command:
   find /home/user -name "*.tmp" -delete

   [Y]es / [N]o / [E]dit / [Q]uit:
```

#### Options Explained

**Y (Yes)** - Execute as proposed

```
✅ Executing command...
```

**N (No)** - Skip this command

```
⏭️ Skipping command, continuing with task...
💭 Looking for alternative approach...
```

**E (Edit)** - Modify before execution

```
Edit command: find /home/user -name "*.tmp" -print
                                               ^^^^^ Changed to print instead

✅ Executing modified command...
```

**Q (Quit)** - Exit Ask-Shell

```
👋 Exiting Ask-Shell. No commands executed.
```

### Layer 4: Transparency

See exactly what the AI is thinking and why.

#### Reasoning Display

```
💭 AI Thinking Process:

Task Analysis:
  "delete old temporary files"
  
Approach:
  1. Find all .tmp files
  2. Check modification time (older than 7 days)
  3. Delete found files
  
Safety Considerations:
  - Using -mtime +7 to limit scope
  - Starting in /tmp not home directory
  - Could affect running processes
  - Recommending -print first to preview
  
Risk Assessment: MEDIUM
  Reason: Deletion is permanent, but limited scope
```

## Safety Best Practices

### 1. Always Review Commands

Even for "safe" operations, quick review helps you:

- Understand what's happening
- Learn new command patterns
- Catch potential issues

### 2. Use Edit Option Liberally

When in doubt, choose **E** to:

- Add safety flags (`-i` for interactive)
- Change scope (`rm file.txt` instead of `rm *.txt`)
- Preview first (`ls` before `rm`)

### 3. Test with Demo Mode

Try risky-sounding tasks in demo mode first:

```bash
ask -d "delete all large files"
```

See what commands would be generated without actual execution.

### 4. Start Small in Auto Mode

Only use auto mode (`-a`) when:

- ✅ You trust the operation completely
- ✅ The task is read-only (listing, searching)
- ✅ You've tested it before
- ✅ The scope is well-defined

**Never** in auto mode:

- ❌ First time trying a complex task
- ❌ Operations on important data
- ❌ System-level modifications
- ❌ When you're unsure of the outcome

### 5. Leverage Interactive Mode for Risky Tasks

```bash
ask -i

Ask-Shell > first, show me what files would be deleted
[... previews files ...]

Ask-Shell > now delete only the .log files, not .txt
[... executes with confirmation ...]
```

## Understanding Risk Levels

### Low Risk ✅

Operations that are:

- Read-only (listing, viewing, searching)
- Easily reversible
- Limited scope
- Well-defined targets

**Examples:**

```bash
ls -la
cat README.md
grep "error" logfile.txt
find . -name "*.py"
```

### Medium Risk ⚠️

Operations that are:

- Modify files (but not delete)
- Affect multiple files with pattern
- Create/move files
- Change metadata

**Examples:**

```bash
mv *.log archive/
chmod +x script.sh
touch newfile.txt
cp -r src/ backup/
```

### High Risk 🚨

Operations that are:

- Delete files permanently
- Recursive operations
- System configuration changes
- Network-based execution

**Examples:**

```bash
rm -rf old_data/
chmod 777 /var/www/
curl http://example.com/script.sh | bash
sudo systemctl stop important-service
```

### Critical Risk 💀

Operations that are:

- System-destroying
- Data loss at scale
- Irreversible harm
- Security vulnerabilities

**Examples:**

```bash
rm -rf /
dd if=/dev/zero of=/dev/sda
chmod -R 777 /
:(){ :|:& };:
```

These are **BLOCKED** by blacklist.

## Advanced Safety Features

### Scope Limitation

AI tries to limit command scope:

**Your request**: "delete log files"

**Without context**: Might affect entire system

**AI strategy**:

```bash
# Starts conservative
find /var/log -name "*.log" -mtime +30 -print

# Shows you what would be affected
# Then asks if you want to proceed with deletion
```

### Incremental Execution

For multi-step tasks, each step confirmed separately:

```bash
ask "clean up project: remove node_modules, clear cache, delete logs"
```

**Step 1** (Low risk):

```
rm -rf node_modules/  # Confirmed ✓
```

**Step 2** (Medium risk):

```
rm -rf .cache/  # Confirmed ✓
```

**Step 3** (High risk):

```
find . -name "*.log" -delete
⚠️ This will permanently delete log files. Proceed? [y/N]
```

### Backup Suggestions

For risky operations, AI suggests backups:

```
💭 Recommendation: Create backup first

Proposed sequence:
  1. tar -czf backup-$(date +%Y%m%d).tar.gz data/
  2. rm -rf data/

Execute with backup? [Y/n]
```

## Handling False Positives

Sometimes safe commands are flagged. Here's how to handle it:

### Understanding the Warning

```
⚠️ Potential risk detected
   Command: find . -name "*.pyc" -delete
   Concern: Deletion operation without preview
```

### Evaluating the Risk

Ask yourself:

1. Is the scope correct? (current directory)
2. Is the pattern specific enough? (*.pyc only)
3. Can I recover if needed? (regenerated by Python)
4. Do I understand the command? (yes)

### Proceeding Safely

```
[E]dit to add preview first:

find . -name "*.pyc" -print
# Review the list

# Then if ok:
find . -name "*.pyc" -delete
```

## Safety Configuration

### Strictness Levels (Future Feature)

```bash
# Paranoid mode - confirm everything
export ASK_SHELL_SAFETY=strict

# Balanced mode (default) - AI-powered detection
export ASK_SHELL_SAFETY=balanced

# Relaxed mode - only blacklist
export ASK_SHELL_SAFETY=relaxed
```

### Custom Blacklist

Add project-specific dangerous patterns:

```bash
# In your .env
ASK_SHELL_CUSTOM_BLACKLIST="drop table,truncate database,rm -rf src/"
```

## Emergency Stop

### During Execution

Press `Ctrl+C` to stop:

```
^C
⏸️ Execution interrupted by user
   Cleaning up...
   Safe to exit.
```

### In Interactive Mode

Type `quit`, `exit`, or press `Ctrl+D`:

```
Ask-Shell > quit
👋 Goodbye! No pending operations.
```

## What Safety Doesn't Cover

### System-Level Risks

- Commands run with **your** user permissions
- If you have sudo access, AI might generate sudo commands
- External scripts downloaded and executed are not analyzed

### Logical Errors

- AI-generated commands should be correct, but always verify
- Edge cases in complex regex or find expressions
- Race conditions in scripted operations

### Best Practice

> **Never run Ask-Shell with root privileges unless absolutely necessary**

## Learning from Safety Warnings

Each warning is an opportunity to learn:

```
⚠️ Command: rm *.log

Why risky: Wildcards expand unpredictably

What you learn: 
- Always preview with ls *.log first
- Use find for more control
- Consider moving to trash instead

Better approach:
  ls *.log  # Preview
  # Then if OK:
  rm *.log
```

## Next Steps

- [See safety in action with examples](examples.md)
- [Learn about the Agent architecture](../api/agent.md)
- [Explore the Executor safety implementation](../api/executor.md)
