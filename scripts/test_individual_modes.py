#!/usr/bin/env python3
"""
Test each mode individually by creating a single-mode .roomodes file.
This isolates broken modes so they don't kill the entire set.

Usage:
  python3 scripts/test_individual_modes.py          # Test all modes, report failures
  python3 scripts/test_individual_modes.py --slug debug   # Test one specific mode
  python3 scripts/test_individual_modes.py --create-passing  # Build .roomodes from only passing modes
"""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
ROOMODES_PATH = REPO_ROOT / ".roomodes"


def test_single_mode(mode: dict) -> tuple[bool, str]:
    """Test one mode by writing it to a temp .roomodes and parsing it back."""
    slug = mode.get("slug", "UNKNOWN")

    # Check 1: Required fields
    required = {"slug", "name", "roleDefinition", "groups"}
    missing = required - set(mode.keys())
    if missing:
        return False, f"Missing required fields: {missing}"

    # Check 2: Slug format
    import re
    if not re.match(r'^[a-zA-Z0-9-]+$', mode["slug"]):
        return False, f"Invalid slug: '{mode['slug']}'"
    if "--" in mode["slug"]:
        return False, f"Double dash in slug: '{mode['slug']}'"

    # Check 3: Groups
    allowed = {"read", "edit", "browser", "command", "mcp"}
    groups = mode.get("groups", [])
    invalid = set(groups) - allowed
    if invalid:
        return False, f"Invalid groups: {invalid}"
    if not groups:
        return False, "Empty groups list"

    # Check 4: Unsupported fields
    allowed_keys = {"slug", "name", "roleDefinition", "description", "whenToUse", "customInstructions", "groups", "source"}
    extra = set(mode.keys()) - allowed_keys
    if extra:
        return False, f"Unsupported fields: {extra}"

    # Check 5: YAML roundtrip
    try:
        single_file = {"customModes": [mode]}
        yaml_str = yaml.dump(single_file, default_flow_style=False, sort_keys=False, allow_unicode=True)

        # Check size
        if len(yaml_str) > 50000:
            return False, f"Mode YAML too large: {len(yaml_str)} bytes (max ~50KB)"

        # Parse back
        parsed = yaml.safe_load(yaml_str)
        if not parsed or "customModes" not in parsed:
            return False, "YAML roundtrip failed"

        return True, "OK"
    except Exception as e:
        return False, f"YAML error: {e}"


def test_all_modes():
    """Test each mode from custom_modes.d/ individually."""
    d = REPO_ROOT / "custom_modes.d"
    files = sorted(d.rglob("*.yaml"))

    passing = []
    failing = []

    print(f"Testing {len(files)} modes individually...\n")

    for f in files:
        rel = f.relative_to(REPO_ROOT)
        try:
            with open(f) as fh:
                data = yaml.safe_load(fh)
            if not isinstance(data, dict) or "customModes" not in data:
                failing.append((str(rel), "Missing customModes wrapper"))
                print(f"  ❌ {rel}: Missing customModes wrapper")
                continue

            modes = data.get("customModes", [])
            if not modes:
                failing.append((str(rel), "Empty customModes"))
                print(f"  ❌ {rel}: Empty customModes")
                continue

            mode = modes[0]
            slug = mode.get("slug", "UNKNOWN")
            ok, msg = test_single_mode(mode)

            if ok:
                passing.append(slug)
                print(f"  ✅ {slug}")
            else:
                failing.append((slug, msg))
                print(f"  ❌ {slug}: {msg}")

        except Exception as e:
            failing.append((str(rel), f"Parse error: {e}"))
            print(f"  ❌ {rel}: Parse error: {e}")

    print(f"\n{'='*60}")
    print(f"Results: {len(passing)} passing, {len(failing)} failing")

    if failing:
        print(f"\n❌ FAILING MODES ({len(failing)}):")
        for slug, msg in failing:
            print(f"  {slug}: {msg}")

    # Write passing slugs to file
    passing_file = REPO_ROOT / "passing_slugs.txt"
    with open(passing_file, "w") as f:
        for slug in sorted(passing):
            f.write(f"{slug}\n")
    print(f"\nPassing slugs written to: {passing_file}")

    return passing, failing


def create_passing_roomodes():
    """Build .roomodes from only passing modes."""
    passing_file = REPO_ROOT / "passing_slugs.txt"
    if not passing_file.exists():
        print("No passing_slugs.txt found. Run without --create-passing first.")
        return

    passing_slugs = set()
    with open(passing_file) as f:
        for line in f:
            s = line.strip()
            if s:
                passing_slugs.add(s)

    print(f"Building .roomodes from {len(passing_slugs)} passing modes...")

    all_modes = []
    d = REPO_ROOT / "custom_modes.d"
    for f in sorted(d.rglob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if not isinstance(data, dict) or "customModes" not in data:
            continue
        for mode in data.get("customModes", []):
            if mode.get("slug") in passing_slugs:
                all_modes.append(mode)

    # Write
    output = {"customModes": all_modes}
    with open(ROOMODES_PATH, "w") as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=10000)

    size = ROOMODES_PATH.stat().st_size
    print(f"✅ Wrote {len(all_modes)} modes to .roomodes ({size:,} bytes)")


def test_specific_mode(slug: str):
    """Test one specific mode and create a temp .roomodes for manual testing."""
    d = REPO_ROOT / "custom_modes.d"
    found = None

    for f in sorted(d.rglob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if not isinstance(data, dict) or "customModes" not in data:
            continue
        for mode in data.get("customModes", []):
            if mode.get("slug") == slug:
                found = mode
                break
        if found:
            break

    if not found:
        print(f"Mode '{slug}' not found in custom_modes.d/")
        return

    ok, msg = test_single_mode(found)
    print(f"{slug}: {'✅' if ok else '❌'} {msg}")

    if ok:
        # Create temp file for manual testing
        tmp = REPO_ROOT / f".roomodes.test-{slug}"
        with open(tmp, "w") as f:
            yaml.dump({"customModes": [found]}, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"Temp file created: {tmp}")
        print(f"To test in Roo Code: cp {tmp.name} .roomodes && reload VS Code")


def main():
    parser = argparse.ArgumentParser(description="Test individual modes")
    parser.add_argument("--slug", help="Test a specific mode by slug")
    parser.add_argument("--create-passing", action="store_true", help="Build .roomodes from passing modes only")
    args = parser.parse_args()

    if args.slug:
        test_specific_mode(args.slug)
    elif args.create_passing:
        create_passing_roomodes()
    else:
        passing, failing = test_all_modes()
        if failing:
            print(f"\nRun with --create-passing to build .roomodes excluding broken modes")
            sys.exit(1)


if __name__ == "__main__":
    main()
