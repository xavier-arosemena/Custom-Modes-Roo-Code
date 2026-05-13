#!/usr/bin/env python3
"""
Split modes into smaller .roomodes files for testing batch sizes.
Finds the maximum number of modes Roo Code can load.

Usage:
  python3 scripts/batch_roomodes.py --batch-size 50    # Creates .roomodes.00, .roomodes.01, etc.
  python3 scripts/batch_roomodes.py --single debug     # Creates .roomodes.single-debug for one-mode test
"""
import argparse
import shutil
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def load_all_modes():
    d = REPO_ROOT / "custom_modes.d"
    modes = []
    for f in sorted(d.rglob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if isinstance(data, dict) and "customModes" in data:
            modes.extend(data.get("customModes", []))
    return modes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=50, help="Modes per batch file")
    parser.add_argument("--single", help="Generate a single-mode test file for this slug")
    parser.add_argument("--output-prefix", default=".roomodes", help="Output file prefix")
    args = parser.parse_args()

    modes = load_all_modes()

    if args.single:
        found = None
        for m in modes:
            if m.get("slug") == args.single:
                found = m
                break
        if not found:
            print(f"Mode '{args.single}' not found")
            return
        out = REPO_ROOT / f"{args.output_prefix}.single-{args.single}"
        with open(out, "w") as f:
            yaml.dump({"customModes": [found]}, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"Created: {out.name}")
        print(f"To test: cp {out.name} .roomodes && reload VS Code")
        return

    # Create batches
    total_batches = (len(modes) + args.batch_size - 1) // args.batch_size
    print(f"Creating {total_batches} batch files ({args.batch_size} modes each)...")

    for i in range(total_batches):
        start = i * args.batch_size
        end = min(start + args.batch_size, len(modes))
        batch = modes[start:end]
        out = REPO_ROOT / f"{args.output_prefix}.{i:02d}"
        with open(out, "w") as f:
            yaml.dump({"customModes": batch}, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        size = out.stat().st_size
        print(f"  {out.name}: {len(batch)} modes, {size:,} bytes ({size/1024:.0f} KB)")

    print(f"\nTest each batch:")
    print(f"  cp .roomodes.00 .roomodes && reload VS Code")
    print(f"  cp .roomodes.01 .roomodes && reload VS Code")
    print(f"  ...etc")
    print(f"\nWhen you find the max batch that works, you can stack them:")
    print(f"  cat .roomodes.00 .roomodes.01 > .roomodes  (if YAML merging works)")


if __name__ == "__main__":
    main()
