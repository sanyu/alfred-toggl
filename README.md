# tg - Toggl CLI Wrapper with Todoist Integration

A smart wrapper around [toggl-cli](https://github.com/watercooler-labs/toggl-cli) that adds:
- **Clipboard support** for quick timer starts
- **Todoist integration** for automatic project inference
- **Local caching** to avoid API rate limits
- **Alfred workflows** for one-key timer control

## Alfred Workflows

This repo includes two Alfred workflows:

### 1. Toggl Timer (Standalone)
Universal Action for starting timers from selected text.

**Download**: [Latest Release](https://github.com/sanyu/alfred-toggl/releases/latest)

**Usage:**
- Select text anywhere → Universal Actions → "Start Toggl Timer"
- Keywords: `tgstop` (stop), `tgnow` (current)

### 2. AlfreDo-Toggl (Enhanced Todoist Integration)
Modified [AlfreDo](https://github.com/giovannicoppola/AlfreDo) with built-in Toggl integration.

**Download**: [Latest AlfreDo-Toggl Release](https://github.com/sanyu/alfred-toggl/releases?q=alfredo-toggl)

**New Features:**
- **⌘↩️ (cmd-enter)**: Copy task name to clipboard 📋
- **⌥↩️ (option-enter)**: Start Toggl timer ⏱️ (with project inference!)

**How it works:**
1. Open AlfreDo (`!1` for today's tasks)
2. Select a task
3. Press **⌥↩️** → Timer starts automatically with correct project!

See [`alfredo-modifications/`](alfredo-modifications/) for technical details on how modifications are applied.

## Installation

```bash
# Add tap
brew tap sanyu/tap

# Install
brew install sanyu/tap/toggl-cli sanyu/tap/tg
```

## Setup

### 1. Authenticate with Toggl and Todoist
```bash
# Toggl authentication
toggl auth YOUR_TOGGL_TOKEN  # from https://track.toggl.com/profile

# Todoist authentication
todoist auth  # Opens browser for OAuth
```

### 2. Sync Projects
```bash
# Select which Todoist projects to sync to Toggl
tg sync-projects

# Build task→project cache
tg refresh-cache
```

## Usage

### Basic Timer Control
```bash
# Start timer from clipboard (with automatic project inference!)
tg start

# Start timer with explicit task name
tg start "Task description"

# Stop current timer
tg stop

# Show current timer
tg current
```

### Project Management
```bash
# Sync selected Todoist projects to Toggl
tg sync-projects

# Refresh task→project cache from Todoist
tg refresh-cache
```

### How Project Inference Works

1. Copy a task name from Todoist (via AlfreDo or manually)
2. Run `tg start` (reads from clipboard)
3. `tg` looks up the task in local cache → finds the project
4. Timer starts in Toggl with the correct project!

**Avoids Todoist API calls** during daily usage - project inference uses local cache at `~/.tg/config.json`.

## Requirements

- macOS
- [toggl-cli](https://github.com/watercooler-labs/toggl-cli)
- [todoist-cli](https://github.com/sachaos/todoist) (`brew install todoist-cli`)
- `jq` for JSON processing (`brew install jq`)

## License

MIT
