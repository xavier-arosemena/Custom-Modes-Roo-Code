#!/usr/bin/env python3
"""Compile individual custom_modes.d/ YAML files into consolidated .roomodes and custom_modes.yaml.

This script:
1. Reads all custom_modes.d/*/*.yaml files
2. Validates them against Roo Code schema
3. Merges with existing .roomodes (custom_modes.d takes precedence)
4. Outputs .roomodes (YAML format, preferred by Roo Code)
5. Outputs custom_modes.yaml (for convert_modes.py compatibility)

Usage:
    python3 scripts/compile_modes.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set

import yaml

# Paths
REPO_ROOT = Path(__file__).parent.parent
CUSTOM_MODES_DIR = REPO_ROOT / "custom_modes.d"
ROOMODES_FILE = REPO_ROOT / ".roomodes"
CUSTOM_MODES_YAML = REPO_ROOT / "custom_modes.yaml"

# Validation
ALLOWED_PERMISSIONS = {"read", "edit", "browser", "command", "mcp"}
SLUG_PATTERN = re.compile(r"^[a-zA-Z0-9-]+$")


class ValidationError(Exception):
    """Raised when validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def _ensure(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_mode(mode: Dict[str, Any], seen_slugs: Set[str]) -> None:
    _ensure(isinstance(mode, dict), "Each custom mode must be a mapping")
    slug = mode.get("slug")
    _ensure(isinstance(slug, str) and slug.strip(), "Mode is missing a non-empty 'slug'")
    _ensure(SLUG_PATTERN.fullmatch(slug), f"{slug}: slug must match {SLUG_PATTERN.pattern}")
    _ensure(slug not in seen_slugs, f"{slug}: duplicate slug detected")
    seen_slugs.add(slug)

    allowed_keys = {
        "slug",
        "name",
        "description",
        "roleDefinition",
        "whenToUse",
        "customInstructions",
        "groups",
        "rulesFiles",
    }
    extra = set(mode) - allowed_keys
    _ensure(not extra, f"{slug}: contains unsupported keys: {sorted(extra)}")

    missing = {"name", "roleDefinition", "groups"} - set(mode)
    _ensure(not missing, f"{slug}: missing required keys: {sorted(missing)}")

    name = mode["name"]
    _ensure(isinstance(name, str) and 1 <= len(name) <= 100,
            f"{slug}: name must be a non-empty string up to 100 characters")

    role_definition = mode["roleDefinition"]
    _ensure(isinstance(role_definition, str) and len(role_definition.strip()) >= 10,
            f"{slug}: roleDefinition must be at least 10 characters")

    if "description" in mode:
        _ensure(isinstance(mode["description"], str) and mode["description"].strip(),
                f"{slug}: description must be a non-empty string when provided")

    if "whenToUse" in mode:
        _ensure(isinstance(mode["whenToUse"], str) and mode["whenToUse"].strip(),
                f"{slug}: whenToUse must be a non-empty string when provided")

    if "customInstructions" in mode:
        _ensure(isinstance(mode["customInstructions"], str) and mode["customInstructions"].strip(),
                f"{slug}: customInstructions must be a non-empty string when provided")

    # Validate groups
    groups = mode["groups"]
    _ensure(isinstance(groups, Sequence) and not isinstance(groups, (str, bytes)),
            f"{slug}: groups must be a list")
    _ensure(groups, f"{slug}: groups must not be empty")

    for idx, entry in enumerate(groups, start=1):
        prefix = f"{slug}: groups[{idx}]"
        if isinstance(entry, str):
            _ensure(entry in ALLOWED_PERMISSIONS,
                    f"{prefix} must be one of {sorted(ALLOWED_PERMISSIONS)}; got {entry!r}")
            continue
        if isinstance(entry, Sequence) and not isinstance(entry, (str, bytes)):
            _ensure(len(entry) == 2,
                    f"{prefix} tuple must contain exactly two items")
            _ensure(entry[0] == "edit",
                    f"{prefix}[0] must be 'edit' when using tuple syntax")
            options = entry[1]
            _ensure(isinstance(options, dict),
                    f"{prefix}[1] must be a mapping of options")
            allowed_opt_keys = {"fileRegex", "description"}
            extra_opt = set(options) - allowed_opt_keys
            _ensure(not extra_opt,
                    f"{prefix}[1] contains unsupported keys: {sorted(extra_opt)}")
            _ensure("fileRegex" in options,
                    f"{prefix}[1] must include 'fileRegex'")
            _ensure(isinstance(options["fileRegex"], str) and options["fileRegex"].strip(),
                    f"{prefix}[1].fileRegex must be a non-empty string")
            continue
        raise ValidationError(f"{prefix} must be a permission string or ['edit', {{options}}]")

    if "rulesFiles" in mode:
        rf = mode["rulesFiles"]
        _ensure(isinstance(rf, Sequence) and not isinstance(rf, (str, bytes)),
                f"{slug}: rulesFiles must be a list")
        for idx, entry in enumerate(rf, start=1):
            prefix = f"{slug}: rulesFiles[{idx}]"
            _ensure(isinstance(entry, dict), f"{prefix} must be a mapping")
            for key in ("relativePath", "content"):
                _ensure(key in entry, f"{prefix} missing required key '{key}'")
                _ensure(isinstance(entry[key], str) and entry[key].strip(),
                        f"{prefix}.{key} must be a non-empty string")


def load_individual_modes() -> List[Dict[str, Any]]:
    """Load and validate all individual YAML files from custom_modes.d/."""
    modes: List[Dict[str, Any]] = []
    seen_slugs: Set[str] = set()
    errors: List[str] = []

    yaml_files = sorted(CUSTOM_MODES_DIR.rglob("*.yaml"))
    print(f"Found {len(yaml_files)} YAML files in {CUSTOM_MODES_DIR}")

    for file_path in yaml_files:
        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append(f"{file_path}: YAML parse error: {e}")
            continue
        except IOError as e:
            errors.append(f"{file_path}: read error: {e}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{file_path}: top-level must be a mapping")
            continue

        if "customModes" not in data:
            errors.append(f"{file_path}: missing 'customModes' key")
            continue

        file_modes = data["customModes"]
        if not isinstance(file_modes, Sequence) or isinstance(file_modes, (str, bytes)):
            errors.append(f"{file_path}: customModes must be a list")
            continue

        for mode in file_modes:
            try:
                validate_mode(mode, seen_slugs)
                modes.append(mode)
            except ValidationError as e:
                errors.append(f"{file_path}: {e.message}")

    if errors:
        print("\nVALIDATION ERRORS:", file=sys.stderr)
        for err in errors:
            print(f"  ✗ {err}", file=sys.stderr)
        print(f"\n{len(errors)} error(s) found. Fix them before compiling.", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Loaded and validated {len(modes)} modes from individual files")
    return modes


def load_existing_roomodes() -> List[Dict[str, Any]]:
    """Load existing .roomodes if present."""
    if not ROOMODES_FILE.exists():
        return []

    try:
        with ROOMODES_FILE.open("r", encoding="utf-8") as f:
            content = f.read()
    except IOError:
        return []

    # Try YAML first, then JSON
    for parser in (yaml.safe_load,):
        try:
            data = parser(content)
            if isinstance(data, dict) and "customModes" in data:
                modes = data["customModes"]
                if isinstance(modes, Sequence) and not isinstance(modes, (str, bytes)):
                    print(f"✓ Loaded {len(modes)} modes from existing {ROOMODES_FILE}")
                    return list(modes)
        except Exception:
            pass

    # Try JSON
    import json
    try:
        data = json.loads(content)
        if isinstance(data, dict) and "customModes" in data:
            modes = data["customModes"]
            if isinstance(modes, Sequence) and not isinstance(modes, (str, bytes)):
                print(f"✓ Loaded {len(modes)} modes from existing {ROOMODES_FILE} (JSON)")
                return list(modes)
    except json.JSONDecodeError:
        pass

    print(f"⚠ Could not parse existing {ROOMODES_FILE}, starting fresh")
    return []


def merge_modes(new_modes: List[Dict[str, Any]], existing_modes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge modes: new_modes take precedence, but preserve modes only in existing."""
    new_by_slug: Dict[str, Dict[str, Any]] = {}
    for mode in new_modes:
        slug = mode.get("slug")
        if slug:
            new_by_slug[slug] = mode

    existing_by_slug: Dict[str, Dict[str, Any]] = {}
    for mode in existing_modes:
        slug = mode.get("slug")
        if slug:
            existing_by_slug[slug] = mode

    merged: List[Dict[str, Any]] = []
    preserved: List[str] = []
    updated: List[str] = []
    added: List[str] = []

    # Process in order: existing first (preserving order), then new additions
    for slug in existing_by_slug:
        if slug in new_by_slug:
            merged.append(new_by_slug[slug])
            updated.append(slug)
        else:
            merged.append(existing_by_slug[slug])
            preserved.append(slug)

    # Add completely new modes
    for slug, mode in new_by_slug.items():
        if slug not in existing_by_slug:
            merged.append(mode)
            added.append(slug)

    print(f"\nMerge results:")
    print(f"  Updated: {len(updated)} mode(s)")
    print(f"  Added: {len(added)} mode(s)")
    print(f"  Preserved (only in .roomodes): {len(preserved)} mode(s)")
    if preserved:
        print(f"    Preserved slugs: {', '.join(sorted(preserved))}")

    return merged


def write_yaml_output(path: Path, modes: List[Dict[str, Any]]) -> None:
    """Write modes as YAML in Roo Code compatible format."""
    output = {"customModes": modes}

    # Custom YAML string handling to preserve multi-line strings nicely
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

    # Fix indentation: PyYAML doesn't indent list items at the root level properly
    lines = yaml_content.split('\n')
    fixed_lines: List[str] = []
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

    try:
        path.write_text(yaml_content, encoding="utf-8")
        print(f"✓ Wrote {len(modes)} modes to {path}")
    except IOError as e:
        print(f"✗ Error writing {path}: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    print("=" * 60)
    print("Custom Modes Compiler")
    print("=" * 60)

    # Load individual files
    individual_modes = load_individual_modes()

    # Load existing .roomodes
    existing_modes = load_existing_roomodes()

    # Merge
    merged_modes = merge_modes(individual_modes, existing_modes)

    # Remove old double-dash slugs that have been superseded by new single-dash versions
    superseded_old_slugs = set()
    slug_set = {m["slug"] for m in merged_modes}
    for slug in slug_set:
        if "--" in slug:
            # Check if a cleaned version exists (replace -- with -)
            cleaned = slug.replace("--", "-")
            while "--" in cleaned:
                cleaned = cleaned.replace("--", "-")
            if cleaned in slug_set and cleaned != slug:
                superseded_old_slugs.add(slug)

    if superseded_old_slugs:
        print(f"\n🗑 Removing {len(superseded_old_slugs)} superseded old slug(s):")
        for slug in sorted(superseded_old_slugs):
            print(f"    - {slug}")
        merged_modes = [m for m in merged_modes if m["slug"] not in superseded_old_slugs]

    # Check for remaining problematic slugs
    problematic = [m["slug"] for m in merged_modes if "--" in m["slug"]]
    if problematic:
        print(f"\n⚠ Warning: {len(problematic)} mode(s) have double dashes in slugs:")
        for slug in sorted(problematic):
            print(f"    - {slug}")
        print("  These are valid but ugly. Consider renaming for consistency.")

    # Write outputs
    print()
    write_yaml_output(ROOMODES_FILE, merged_modes)
    write_yaml_output(CUSTOM_MODES_YAML, merged_modes)

    print(f"\n{'=' * 60}")
    print(f"Done! Total modes: {len(merged_modes)}")
    print(f"{'=' * 60}")
    print(f"\nRoo Code will read modes from:")
    print(f"  Project-specific: {ROOMODES_FILE}")
    print(f"  Conversion source: {CUSTOM_MODES_YAML}")
    print(f"\nReload VS Code window for changes to take effect.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
