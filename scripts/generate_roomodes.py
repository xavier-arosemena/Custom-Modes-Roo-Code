#!/usr/bin/env python3
"""
Generate .roomodes from individual custom_modes.d/ files.
Supports filtering by slug list, batch sizes, and exclusion lists.

Usage:
  python3 scripts/generate_roomodes.py                    # All 305 modes
  python3 scripts/generate_roomodes.py --batch 50 --index 0   # First 50 modes
  python3 scripts/generate_roomodes.py --exclude-slugs debug,ask  # Exclude specific modes
  python3 scripts/generate_roomodes.py --include-file passing_slugs.txt  # Only include listed slugs
  python3 scripts/generate_roomodes.py --max-size 500000  # Include modes up to ~500KB total
"""
import argparse
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
    parser.add_argument("--batch", type=int, help="Batch size (modes per file)")
    parser.add_argument("--index", type=int, default=0, help="Batch index (0-based)")
    parser.add_argument("--exclude-slugs", help="Comma-separated slugs to exclude")
    parser.add_argument("--include-file", help="File with one slug per line to include")
    parser.add_argument("--max-size", type=int, help="Max total size in bytes")
    parser.add_argument("--output", default=".roomodes", help="Output file name")
    args = parser.parse_args()

    modes = load_all_modes()
    print(f"Loaded {len(modes)} modes from custom_modes.d/")

    # Filter by include file
    if args.include_file:
        include_path = Path(args.include_file)
        if include_path.exists():
            include_slugs = set()
            with open(include_path) as f:
                for line in f:
                    s = line.strip()
                    if s:
                        include_slugs.add(s)
            modes = [m for m in modes if m.get("slug") in include_slugs]
            print(f"Filtered to {len(modes)} modes from {args.include_file}")

    # Filter by exclude list
    if args.exclude_slugs:
        exclude = set(s.strip() for s in args.exclude_slugs.split(","))
        modes = [m for m in modes if m.get("slug") not in exclude]
        print(f"Excluded {len(exclude)} slugs, {len(modes)} remain")

    # Filter by max size
    if args.max_size:
        selected = []
        total = 0
        for m in modes:
            size = len(yaml.dump({"customModes": [m]}, default_flow_style=False, allow_unicode=True))
            if total + size <= args.max_size:
                selected.append(m)
                total += size
            else:
                break
        modes = selected
        print(f"Size-limited to {len(modes)} modes (~{total:,} bytes)")

    # Batch
    if args.batch:
        start = args.index * args.batch
        end = start + args.batch
        modes = modes[start:end]
        print(f"Batch {args.index}: modes {start}-{end-1} ({len(modes)} modes)")

    # Write output
    output_path = REPO_ROOT / args.output
    with open(output_path, "w") as f:
        yaml.dump({"customModes": modes}, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=10000)

    size = output_path.stat().st_size
    print(f"\nWrote {len(modes)} modes to {args.output} ({size:,} bytes = {size/1024:.1f} KB)")
    print(f"To test: rename to .roomodes and reload VS Code")


if __name__ == "__main__":
    main()
