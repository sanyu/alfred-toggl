# tg - Toggl CLI Wrapper

A thin wrapper around [toggl-cli](https://github.com/watercooler-labs/toggl-cli) that adds clipboard support for macOS.

## Installation

```bash
# Add tap
brew tap sanyu/tap

# Install
brew install sanyu/tap/toggl sanyu/tap/tg
```

## Usage

```bash
# Start timer from clipboard (copy task name first)
tg start

# Start timer with task name
tg start "Task description"

# Other commands pass through to toggl
tg stop
tg current
```

## Requirements

- macOS
- [toggl-cli](https://github.com/watercooler-labs/toggl-cli)

## License

MIT
