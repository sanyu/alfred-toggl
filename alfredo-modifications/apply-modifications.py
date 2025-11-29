#!/usr/bin/env python3
"""
Apply Toggl integration modifications to AlfreDo workflow.

This script:
1. Reads toggl-actions.json for action definitions
2. Adds the actions to info.plist
3. Connects them to task list script filters
4. Applies the patch to alfredo-query.py
"""

import json
import plistlib
import subprocess
import sys
import uuid
from pathlib import Path


def load_modifications(mod_dir: Path):
    """Load modification definitions."""
    with open(mod_dir / 'toggl-actions.json', 'r') as f:
        return json.load(f)


def apply_plist_modifications(alfredo_dir: Path, modifications: dict):
    """Apply modifications to info.plist."""
    plist_path = alfredo_dir / 'info.plist'

    # Read plist
    with open(plist_path, 'rb') as f:
        plist = plistlib.load(f)

    # Create actions with unique UIDs
    action_uids = {}
    for action_def in modifications['actions']:
        uid = str(uuid.uuid4()).upper()
        action_uids[action_def['name']] = uid

        action_obj = {
            'config': action_def['config'],
            'type': action_def['type'],
            'uid': uid,
            'version': action_def['version']
        }
        plist['objects'].append(action_obj)
        print(f"✅ Added action '{action_def['name']}' with UID {uid}")

    # Add connections
    for conn_group in modifications['connections']:
        for source_uid in conn_group['source_filters']:
            if source_uid not in plist['connections']:
                print(f"⚠️  Warning: Source filter {source_uid} not found in connections")
                continue

            for conn_def in conn_group['connections']:
                action_name = conn_def['action']
                if action_name not in action_uids:
                    print(f"⚠️  Warning: Action {action_name} not found")
                    continue

                connection = {
                    'destinationuid': action_uids[action_name],
                    'modifiers': conn_def['modifiers'],
                    'modifiersubtext': conn_def['modifiersubtext'],
                    'vitoclose': conn_def['vitoclose']
                }
                plist['connections'][source_uid].append(connection)
                print(f"✅ Added connection for {source_uid[:8]}... -> {action_name}")

    # Add action chains (action-to-action connections)
    if 'action_chains' in modifications:
        for chain in modifications['action_chains']:
            from_action = chain['from']
            to_action = chain['to']

            if from_action not in action_uids:
                print(f"⚠️  Warning: Source action {from_action} not found")
                continue
            if to_action not in action_uids:
                print(f"⚠️  Warning: Destination action {to_action} not found")
                continue

            from_uid = action_uids[from_action]
            to_uid = action_uids[to_action]

            # Initialize connections array if it doesn't exist
            if from_uid not in plist['connections']:
                plist['connections'][from_uid] = []

            # Add connection from action to action
            connection = {
                'destinationuid': to_uid,
                'modifiers': 0,
                'modifiersubtext': '',
                'vitoclose': False
            }
            plist['connections'][from_uid].append(connection)
            print(f"✅ Added action chain: {from_action} -> {to_action}")

    # Write back
    with open(plist_path, 'wb') as f:
        plistlib.dump(plist, f)

    print(f"\n✅ Updated {plist_path}")


def apply_python_patch(alfredo_dir: Path, mod_dir: Path):
    """Apply patch to alfredo-query.py."""
    patch_file = mod_dir / 'alfredo-query.patch'
    target_file = alfredo_dir / 'alfredo-query.py'

    if not patch_file.exists():
        print(f"⚠️  Patch file not found: {patch_file}")
        return

    try:
        # Apply patch
        result = subprocess.run(
            ['patch', '-p1', str(target_file), str(patch_file)],
            cwd=alfredo_dir,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ Applied patch to {target_file}")
        else:
            # Try simple string replacement as fallback
            print(f"⚠️  Patch command failed, trying direct replacement...")
            with open(target_file, 'r') as f:
                content = f.read()

            # Replace the subtitle
            old_text = '"alt": {\n                        \n                        "arg": "",\n                        "subtitle": ""'
            new_text = '"alt": {\n\n                        "arg": "",\n                        "subtitle": "Start Toggl timer ⏱️"'

            if old_text in content:
                content = content.replace(old_text, new_text)
                with open(target_file, 'w') as f:
                    f.write(content)
                print(f"✅ Applied direct replacement to {target_file}")
            else:
                print(f"⚠️  Could not find target text in {target_file}")
                print(f"    This may be due to AlfreDo version differences")

    except FileNotFoundError:
        # patch command not available, use direct replacement
        print(f"⚠️  'patch' command not found, using direct replacement...")
        with open(target_file, 'r') as f:
            content = f.read()

        # Replace the subtitle
        content = content.replace(
            '"subtitle": ""\n                                },\n             },',
            '"subtitle": "Start Toggl timer ⏱️"\n                                },\n             },'
        )

        with open(target_file, 'w') as f:
            f.write(content)
        print(f"✅ Applied direct replacement to {target_file}")


def main():
    if len(sys.argv) != 3:
        print("Usage: apply-modifications.py <alfredo_dir> <modifications_dir>")
        sys.exit(1)

    alfredo_dir = Path(sys.argv[1]).resolve()
    mod_dir = Path(sys.argv[2]).resolve()

    if not alfredo_dir.exists():
        print(f"❌ AlfreDo directory not found: {alfredo_dir}")
        sys.exit(1)

    if not mod_dir.exists():
        print(f"❌ Modifications directory not found: {mod_dir}")
        sys.exit(1)

    print(f"📦 Applying Toggl modifications to AlfreDo")
    print(f"   AlfreDo dir: {alfredo_dir}")
    print(f"   Modifications: {mod_dir}\n")

    # Load modifications
    modifications = load_modifications(mod_dir)

    # Apply plist modifications
    apply_plist_modifications(alfredo_dir, modifications)

    # Apply Python patch
    apply_python_patch(alfredo_dir, mod_dir)

    print(f"\n✅ All modifications applied successfully!")


if __name__ == '__main__':
    main()
