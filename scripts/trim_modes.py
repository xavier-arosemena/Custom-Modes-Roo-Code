#!/usr/bin/env python3
"""
Trim bloated mode fields to sizes Roo Code can actually load.
Targets:
- customInstructions: max 2000 chars
- roleDefinition: max 1200 chars
- description: max 300 chars
- whenToUse: max 400 chars
"""
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

def trim_text(text: str, max_len: int, name: str) -> str:
    if not text or len(text) <= max_len:
        return text
    # Try to break at paragraph boundary
    truncated = text[:max_len]
    # Find last paragraph break
    last_para = truncated.rfind('\n\n')
    if last_para > max_len * 0.5:
        return truncated[:last_para].strip()
    # Find last sentence
    for delim in ['. ', '! ', '? ']:
        idx = truncated.rfind(delim)
        if idx > max_len * 0.6:
            return truncated[:idx + 1].strip()
    # Find last space
    last_space = truncated.rfind(' ')
    if last_space > max_len * 0.7:
        return truncated[:last_space].strip() + '.'
    return truncated.strip()


def trim_mode(mode: dict) -> dict:
    mode['customInstructions'] = trim_text(mode.get('customInstructions', ''), 2000, 'customInstructions')
    mode['roleDefinition'] = trim_text(mode.get('roleDefinition', ''), 1200, 'roleDefinition')
    mode['description'] = trim_text(mode.get('description', ''), 300, 'description')
    mode['whenToUse'] = trim_text(mode.get('whenToUse', ''), 400, 'whenToUse')
    return mode


def main():
    d = REPO_ROOT / "custom_modes.d"
    total_files = 0
    trimmed = 0

    for f in sorted(d.rglob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(fh)

        if not isinstance(data, dict) or 'customModes' not in data:
            continue

        changed = False
        for mode in data['customModes']:
            original = {k: v for k, v in mode.items() if k in ['customInstructions', 'roleDefinition', 'description', 'whenToUse']}
            trim_mode(mode)
            for k in original:
                if original.get(k) != mode.get(k):
                    changed = True
                    break

        if changed:
            with open(f, 'w') as fh:
                yaml.dump(data, fh, default_flow_style=False, sort_keys=False, allow_unicode=True, width=10000)
            trimmed += 1
        total_files += 1

    print(f"Processed: {total_files} files")
    print(f"Trimmed: {trimmed} files")


if __name__ == "__main__":
    main()
