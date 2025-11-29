# AlfreDo Toggl Integration Modifications

This directory contains **decoupled modifications** that add Toggl time tracking integration to the [AlfreDo workflow](https://github.com/giovannicoppola/AlfreDo).

## What It Does

Adds two new modifier key actions to AlfreDo task lists:

- **⌘↩️ (cmd-enter)**: Copy task name to clipboard 📋
- **⌥↩️ (option-enter)**: Start Toggl timer with automatic project inference ⏱️

## How It Works

### Architecture

The modifications are **completely decoupled** from AlfreDo's code and version-independent:

```
toggl-actions.json       → Declarative action definitions
alfredo-query.patch      → Single-line patch for visual hint
apply-modifications.py   → Automation script
```

### What Gets Modified

1. **`info.plist`** (via `toggl-actions.json`):
   - Adds 2 new script actions (copy-task, start-timer)
   - Connects them to 3 task list script filters with modifier keys

2. **`alfredo-query.py`** (via `alfredo-query.patch`):
   - Changes alt modifier subtitle from `""` to `"Start Toggl timer ⏱️"`
   - This provides visual feedback when holding Option key

### Files

#### `toggl-actions.json`

Declarative definition of our additions:

```json
{
  "actions": [
    { "name": "copy-task", "config": { ... } },
    { "name": "start-timer", "config": { ... } }
  ],
  "connections": [ ... ]
}
```

**Easy to modify**: Just edit the JSON to change scripts, modifiers, or text.

#### `alfredo-query.patch`

Unified diff patch for the Python script:

```diff
-                        "subtitle": ""
+                        "subtitle": "Start Toggl timer ⏱️"
```

**Fallback**: If `patch` command fails, script uses direct string replacement.

#### `apply-modifications.py`

Python script that:
1. Reads `toggl-actions.json`
2. Generates unique UIDs for new actions
3. Adds actions and connections to `info.plist`
4. Applies patch to `alfredo-query.py`

**Version independent**: Works with any AlfreDo release structure.

## Usage

### Manual Application

```bash
# Download AlfreDo workflow
curl -L -o alfredo.alfredworkflow \
  https://github.com/giovannicoppola/AlfreDo/releases/download/v0.4.1/AlfreDo_0.4.1.alfredworkflow

# Extract
unzip alfredo.alfredworkflow -d alfredo-extracted

# Apply modifications
python3 apply-modifications.py alfredo-extracted alfredo-modifications

# Repackage
cd alfredo-extracted
zip -r ../AlfreDo-Toggl.alfredworkflow . -x "*.DS_Store"
cd ..

# Install
open AlfreDo-Toggl.alfredworkflow
```

### Automated via GitHub Actions

The workflow `.github/workflows/build-alfredo-toggl.yml` automates this:

- **Manual trigger**: Build any AlfreDo version on-demand
- **Scheduled**: Checks weekly for new AlfreDo releases
- **Publishes**: Creates releases with tag `alfredo-toggl-v{version}`

## Maintenance

### Updating Modifier Keys

Edit `toggl-actions.json`:

```json
{
  "modifiers": 524288,           // 524288 = Option, 1048576 = Cmd
  "modifiersubtext": "Your text",
  "vitoclose": true
}
```

### Changing Scripts

Edit the `script` field in `toggl-actions.json`:

```json
{
  "name": "start-timer",
  "config": {
    "script": "/opt/homebrew/bin/tg start \"$myTaskContent\""
  }
}
```

### Updating for New AlfreDo Versions

If AlfreDo changes structure:

1. **Actions broken?** → Check UIDs in `toggl-actions.json` `source_filters`
2. **Patch fails?** → Update line numbers in `alfredo-query.patch`
3. **Script errors?** → Check `alfredo-query.py` variable names

The automation includes fallbacks and will warn about issues.

## Modifier Key Codes

For reference:

| Modifier | Code |
|----------|------|
| None     | 0 |
| Shift    | 131072 |
| Control  | 262144 |
| Option   | 524288 |
| Command  | 1048576 |

## Dependencies

- Python 3.7+
- `tg` wrapper script (from this repo)
- Alfred with Powerpack

## Why This Approach?

**Pros:**
- ✅ Version independent
- ✅ Easy to update
- ✅ Transparent modifications
- ✅ Automated builds
- ✅ No forking required

**Cons:**
- ⚠️ Can break if AlfreDo radically changes structure
- ⚠️ Requires automation to stay updated

## License

Same as AlfreDo (MIT) and alfred-toggl (MIT).
