#!/usr/bin/env python3
"""Migrate ALL modes from .roomodes and agents/ into custom_modes.d/, then recompile.

This script:
1. Extracts preserved modes from .roomodes into custom_modes.d/
2. Converts agents/ flat YAML files to customModes format and moves them to custom_modes.d/
3. Skips modes already in custom_modes.d/ (keeps enhanced versions)
4. Runs compile_modes.py to regenerate .roomodes and custom_modes.yaml
"""

import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
CUSTOM_MODES_DIR = REPO_ROOT / "custom_modes.d"
ROOMODES_FILE = REPO_ROOT / ".roomodes"
AGENTS_DIR = REPO_ROOT / "agents"


def sanitize_dirname(name: str) -> str:
    """Convert slug to safe directory name."""
    return name.strip().lower().replace(" ", "-").replace("_", "-")[:50]


def generate_when_to_use(name: str, role_definition: str) -> str:
    """Generate whenToUse from name and roleDefinition."""
    if not role_definition:
        return f"Activate this mode when you need support from {name}."
    
    summary = role_definition.strip().split(".")[0]
    lowered = summary.lower()
    if lowered.startswith("you are "):
        rest = summary[8:].strip()
        article = "an" if rest[0:1].lower() in "aeiou" else "a"
        return f"Activate this mode when you need {article} {rest}."
    if lowered.startswith("you "):
        rest = summary[4:].strip()
        return f"Activate this mode when you need someone who can {rest}."
    return f"Activate this mode when you need {summary[0].lower() + summary[1:]}."


def convert_agent_to_mode(agent_data: dict) -> dict:
    """Convert flat agents/ YAML to Roo Code customModes format."""
    mode = {}
    
    # Required fields
    mode["slug"] = agent_data["slug"]
    mode["name"] = agent_data["name"]
    mode["roleDefinition"] = agent_data["roleDefinition"]
    mode["groups"] = agent_data.get("groups", ["read", "edit", "browser", "command", "mcp"])
    
    # Optional fields
    if "description" in agent_data and agent_data["description"]:
        mode["description"] = agent_data["description"]
    else:
        # Generate description from roleDefinition first sentence
        rd = agent_data.get("roleDefinition", "").strip()
        if rd:
            first_sentence = rd.split(".")[0] + "."
            mode["description"] = first_sentence
    
    if "whenToUse" in agent_data and agent_data["whenToUse"]:
        mode["whenToUse"] = agent_data["whenToUse"]
    else:
        mode["whenToUse"] = generate_when_to_use(
            agent_data.get("name", ""),
            agent_data.get("roleDefinition", "")
        )
    
    if "customInstructions" in agent_data and agent_data["customInstructions"]:
        mode["customInstructions"] = agent_data["customInstructions"]
    
    return mode


def write_mode_file(directory: Path, mode: dict) -> None:
    """Write a single mode to custom_modes.d/{dir}/{slug}.yaml"""
    slug = mode["slug"]
    dir_name = sanitize_dirname(slug)
    target_dir = directory / dir_name
    target_dir.mkdir(parents=True, exist_ok=True)
    
    output = {"customModes": [mode]}
    
    # Custom YAML string handling
    def str_representer(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    
    yaml.add_representer(str, str_representer)
    
    yaml_content = yaml.dump(
        output,
        default_flow_style=False,
        sort_keys=False,
        width=1000,
        allow_unicode=True,
        indent=2
    )
    
    # Fix indentation
    lines = yaml_content.split('\n')
    fixed_lines = []
    in_mode_item = False
    
    for line in lines:
        if line.startswith('customModes:'):
            fixed_lines.append(line)
            in_mode_item = False
        elif line.startswith('- slug:'):
            fixed_lines.append('  ' + line)
            in_mode_item = True
        elif in_mode_item and line and not line.startswith(' '):
            fixed_lines.append('    ' + line)
        elif in_mode_item and line.startswith('  '):
            fixed_lines.append('  ' + line)
        else:
            fixed_lines.append(line)
    
    yaml_content = '\n'.join(fixed_lines)
    
    target_file = target_dir / f"{slug}.yaml"
    target_file.write_text(yaml_content, encoding="utf-8")
    print(f"  ✓ {target_file}")


def main() -> int:
    print("=" * 60)
    print("Migrate All Agents to custom_modes.d/")
    print("=" * 60)
    
    # Load existing custom_modes.d slugs
    custom_slugs = set()
    for f in CUSTOM_MODES_DIR.rglob("*.yaml"):
        with f.open("r", encoding="utf-8") as fh:
            d = yaml.safe_load(fh)
        for mode in d.get("customModes", []):
            custom_slugs.add(mode.get("slug"))
    print(f"\nExisting modes in custom_modes.d: {len(custom_slugs)}")
    
    # Load .roomodes
    with ROOMODES_FILE.open("r", encoding="utf-8") as f:
        roomodes_data = yaml.safe_load(f)
    roomodes_by_slug = {m["slug"]: m for m in roomodes_data["customModes"]}
    print(f"Modes in .roomodes: {len(roomodes_by_slug)}")
    
    # Load agents/
    agents_by_slug = {}
    for root, dirs, files in os.walk(AGENTS_DIR):
        for filename in files:
            if filename.endswith(".yaml"):
                path = Path(root) / filename
                with path.open("r", encoding="utf-8") as fh:
                    d = yaml.safe_load(fh)
                if isinstance(d, dict) and "slug" in d:
                    agents_by_slug[d["slug"]] = d
    print(f"Modes in agents/: {len(agents_by_slug)}")
    
    # Determine what to migrate
    preserved_slugs = set(roomodes_by_slug.keys()) - custom_slugs
    agents_only_slugs = set(agents_by_slug.keys()) - custom_slugs - set(roomodes_by_slug.keys())
    
    print(f"\n→ Extracting from .roomodes: {len(preserved_slugs)} modes")
    print(f"→ Converting from agents/: {len(agents_only_slugs)} modes")
    print(f"→ Skipping (already in custom_modes.d): {len(custom_slugs & (set(roomodes_by_slug.keys()) | set(agents_by_slug.keys())))} modes")
    
    migrated = 0
    errors = []
    
    # 1. Extract preserved modes from .roomodes
    for slug in sorted(preserved_slugs):
        mode = roomodes_by_slug[slug]
        try:
            write_mode_file(CUSTOM_MODES_DIR, mode)
            migrated += 1
        except Exception as e:
            errors.append(f"{slug}: {e}")
    
    # 2. Convert agents/ modes
    for slug in sorted(agents_only_slugs):
        agent_data = agents_by_slug[slug]
        try:
            mode = convert_agent_to_mode(agent_data)
            write_mode_file(CUSTOM_MODES_DIR, mode)
            migrated += 1
        except Exception as e:
            errors.append(f"{slug}: {e}")
    
    if errors:
        print(f"\n✗ {len(errors)} error(s):")
        for err in errors:
            print(f"  {err}")
    
    print(f"\n✓ Migrated {migrated} new modes to custom_modes.d/")
    
    # 3. Recompile
    print("\n" + "=" * 60)
    print("Recompiling .roomodes and custom_modes.yaml...")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "compile_modes.py")],
        cwd=REPO_ROOT,
        capture_output=False
    )
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
