#!/usr/bin/env python3
"""
Inject engineering protocols as rulesFiles into custom_modes.yaml files.

Reads protocol markdown files and adds them as rulesFiles entries on
relevant modes in the YAML configuration. Operates via string insertion
to preserve existing YAML formatting.

Usage:
    python3 scripts/inject_engineering_protocols.py
"""

import os
import re
import sys

PROTOCOLS_DIR = "/home/batman/Desktop/4TB_Desktop/LLM-Special-Instructions-Must-Have-GIT/knowledge/engineering_protocols/"

# Map: protocol filename -> list of target mode slugs
PROTOCOL_MODE_MAP = {
    "Coding_Logic_Core.md": [
        "code",
        "backend-developer",
        "full-stack-developer",
        "fullstack-developer",
    ],
    "Coding_Logic_Operations.md": [
        "devops",
        "devops-engineer",
        "build-engineer",
        "deployment-engineer",
    ],
    "Coding_Logic_Formal.md": [
        "architect",
        "code-reviewer",
    ],
    "Coding_Logic_SOTA.md": [
        "frontend-developer",
        "nextjs-developer",
        "full-stack-developer",
    ],
    "uxui-logic.md": [
        "frontend-developer",
    ],
}

TARGET_FILES = [
    "/home/batman/.config/Antigravity/User/globalStorage/rooveterinaryinc.roo-cline/settings/custom_modes.yaml",
    "/home/batman/Desktop/ROO CODE MODES/Custom-Modes-Roo-Code/custom_modes.yaml",
]


def read_protocol(filename: str) -> str:
    """Read a protocol markdown file."""
    filepath = os.path.join(PROTOCOLS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  WARNING: Protocol file not found: {filepath}")
        return ""
    with open(filepath) as f:
        return f.read()


def find_mode_blocks(content: str) -> list[tuple[str, int, int]]:
    """Find all mode blocks in the YAML. Returns list of (slug, start, end)."""
    blocks = []
    # Find all mode starts: "  - slug: <slug>"
    for match in re.finditer(r"^  - slug: (.+)$", content, re.MULTILINE):
        slug = match.group(1).strip()
        start = match.start()
        blocks.append((slug, start))
    
    # Calculate end positions
    result = []
    for i, (slug, start) in enumerate(blocks):
        if i + 1 < len(blocks):
            end = blocks[i + 1][1]
        else:
            end = len(content)
        result.append((slug, start, end))
    
    return result


def inject_into_file(yaml_path: str) -> None:
    """Inject engineering protocols into a single YAML file."""
    print(f"\n{'='*60}")
    print(f"Processing: {yaml_path}")
    print(f"{'='*60}")
    
    if not os.path.exists(yaml_path):
        print(f"  SKIP: File not found")
        return
    
    with open(yaml_path) as f:
        content = f.read()
    
    # Find all mode blocks
    mode_blocks = find_mode_blocks(content)
    slug_to_block = {slug: (start, end) for slug, start, end in mode_blocks}
    
    injections = []  # (position, text_to_insert)
    
    for protocol_file, target_slugs in PROTOCOL_MODE_MAP.items():
        protocol_content = read_protocol(protocol_file)
        if not protocol_content:
            continue
        
        rules_path = f".rules/engineering_protocols/{protocol_file}"
        
        for slug in target_slugs:
            if slug not in slug_to_block:
                print(f"  SKIP: Mode '{slug}' not found in file")
                continue
            
            start, end = slug_to_block[slug]
            mode_block = content[start:end]
            
            # Check if this protocol is already injected
            if rules_path in mode_block:
                print(f"  SKIP: {protocol_file} already in '{slug}'")
                continue
            
            # Find insertion point: before "    groups:" line
            groups_match = re.search(r"^    groups:", mode_block, re.MULTILINE)
            if groups_match:
                insert_pos = start + groups_match.start()
            else:
                # Insert at end of mode block
                insert_pos = end
            
            # Build the rulesFiles YAML block using literal scalar
            # Content must be indented MORE than the "content:" key (8 spaces)
            # So content lines need 10+ spaces
            indented_lines = []
            for line in protocol_content.split("\n"):
                if line.strip() == "":
                    indented_lines.append("")
                else:
                    indented_lines.append("          " + line)
            
            indented_content = "\n".join(indented_lines)
            
            rules_entry = (
                f"    rulesFiles:\n"
                f"      - relativePath: \"{rules_path}\"\n"
                f"        content: |\n"
                f"{indented_content}\n"
            )
            
            injections.append((insert_pos, rules_entry, slug, protocol_file))
    
    # Sort injections by position descending (insert from bottom to top)
    injections.sort(key=lambda x: x[0], reverse=True)
    
    # Apply injections
    for pos, text, slug, protocol_file in injections:
        content = content[:pos] + text + content[pos:]
        print(f"  INJECTED: {protocol_file} -> '{slug}'")
    
    if injections:
        with open(yaml_path, "w") as f:
            f.write(content)
        print(f"  WROTE: {len(injections)} injections applied")
    else:
        print(f"  NO CHANGES: Nothing to inject")


def main():
    print("Engineering Protocol Injector")
    print(f"Protocols directory: {PROTOCOLS_DIR}")
    
    # Verify protocol files exist
    for protocol_file in PROTOCOL_MODE_MAP:
        path = os.path.join(PROTOCOLS_DIR, protocol_file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  Found: {protocol_file} ({size} bytes)")
        else:
            print(f"  MISSING: {protocol_file}")
    
    for yaml_path in TARGET_FILES:
        inject_into_file(yaml_path)
    
    print("\nDone.")


if __name__ == "__main__":
    main()
