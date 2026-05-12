#!/usr/bin/env python3
"""Bulk update jtgsystems agent YAML files from 2025 to 2026 standards."""

import os
import re
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "agents"

# Skip SOTA personas (already 2026)
SKIP_DIRS = {"sota-personas"}

REPLACEMENTS = [
    # Header: 2025 → 2026
    (r"## 2025 Standards Compliance", "## 2026 Standards Compliance"),
    (r"This agent follows 2025 best practices", "This agent follows 2026 best practices"),
    # Handle YAML escaped newlines in double-quoted strings
    (r"follows 2025 best", "follows 2026 best"),
    
    # Stack versions
    (r"React 18\+", "React 19+"),
    (r"React 19\+", "React 19+"),  # idempotent
    (r"Node 20\+", "Node 22+"),
    (r"Node 22\+", "Node 22+"),  # idempotent
    (r"Python 3\.12\+", "Python 3.13+"),
    (r"Python 3\.13\+", "Python 3.13+"),  # idempotent
    
    # Performance targets
    (r"Sub-200ms targets", "Sub-100ms targets"),
    (r"Sub-100ms targets", "Sub-100ms targets"),  # idempotent
    
    # Coverage targets
    (r">90% coverage", ">95% coverage"),
    (r">95% coverage", ">95% coverage"),  # idempotent
    
    # Node.js versions in body text
    (r"Node\.js 18\+", "Node.js 22+"),
    (r"Node\.js 20\+", "Node.js 22+"),
    (r"Node\.js 22\+", "Node.js 22+"),  # idempotent
    
    # Python versions in body text
    (r"Python 3\.11\+", "Python 3.13+"),
    
    # Go versions
    (r"Go 1\.21\+", "Go 1.24+"),
    (r"Go 1\.22\+", "Go 1.24+"),
    (r"Go 1\.23\+", "Go 1.24+"),
    (r"Go 1\.24\+", "Go 1.24+"),  # idempotent
    
    # TypeScript versions
    (r"TypeScript 5\.3", "TypeScript 5.7"),
    (r"TypeScript 5\.4", "TypeScript 5.7"),
    (r"TypeScript 5\.5", "TypeScript 5.7"),
    (r"TypeScript 5\.6", "TypeScript 5.7"),
    (r"TypeScript 5\.7", "TypeScript 5.7"),  # idempotent
    
    # Java versions
    (r"Java 21", "Java 24"),
    (r"Java 22", "Java 24"),
    (r"Java 23", "Java 24"),
    (r"Java 24", "Java 24"),  # idempotent
    
    # Spring Boot
    (r"Spring Boot 3\.2", "Spring Boot 3.4"),
    (r"Spring Boot 3\.3", "Spring Boot 3.4"),
    (r"Spring Boot 3\.4", "Spring Boot 3.4"),  # idempotent
    
    # Next.js
    (r"Next\.js 14", "Next.js 16"),
    (r"Next\.js 15", "Next.js 16"),
    (r"Next\.js 16", "Next.js 16"),  # idempotent
    
    # .NET
    (r"\.NET 8", ".NET 9"),
    (r"\.NET 9", ".NET 9"),  # idempotent
    
    # Laravel
    (r"Laravel 11", "Laravel 12"),
    (r"Laravel 12", "Laravel 12"),  # idempotent
    
    # Django
    (r"Django 4\.2", "Django 5.2"),
    (r"Django 5\.0", "Django 5.2"),
    (r"Django 5\.1", "Django 5.2"),
    (r"Django 5\.2", "Django 5.2"),  # idempotent
    
    # Rails
    (r"Rails 7", "Rails 8"),
    (r"Rails 8", "Rails 8"),  # idempotent
    
    # Flutter
    (r"Flutter 3\.", "Flutter 4."),
    
    # Swift
    (r"Swift 5\.9", "Swift 6.1"),
    (r"Swift 6\.0", "Swift 6.1"),
    (r"Swift 6\.1", "Swift 6.1"),  # idempotent
    
    # Kubernetes
    (r"Kubernetes 1\.28", "Kubernetes 1.32"),
    (r"Kubernetes 1\.29", "Kubernetes 1.32"),
    (r"Kubernetes 1\.30", "Kubernetes 1.32"),
    (r"Kubernetes 1\.31", "Kubernetes 1.32"),
    (r"Kubernetes 1\.32", "Kubernetes 1.32"),  # idempotent
    
    # Terraform
    (r"Terraform 1\.6", "Terraform 1.11"),
    (r"Terraform 1\.7", "Terraform 1.11"),
    (r"Terraform 1\.8", "Terraform 1.11"),
    (r"Terraform 1\.9", "Terraform 1.11"),
    (r"Terraform 1\.10", "Terraform 1.11"),
    (r"Terraform 1\.11", "Terraform 1.11"),  # idempotent
]


def update_yaml_file(filepath: Path) -> dict:
    """Update a single YAML file. Returns stats about changes."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    
    original = raw
    changes = 0
    
    for pattern, replacement in REPLACEMENTS:
        new_raw, count = re.subn(pattern, replacement, raw)
        if count > 0:
            changes += count
            raw = new_raw
    
    # Update version and lastUpdated fields via YAML parsing
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return {"file": str(filepath), "error": "YAML parse error", "changes": 0}
    
    field_changes = 0
    if data.get("version") == "2025.1":
        data["version"] = "2026.1"
        field_changes += 1
    if data.get("lastUpdated", "").startswith("2025"):
        data["lastUpdated"] = "2026-05-12"
        field_changes += 1
    
    if changes > 0 or field_changes > 0:
        # Re-dump with proper formatting
        # Use the text replacements for customInstructions/roleDefinition 
        # but update the structured fields
        updated = raw
        if "version: '2025.1'" in updated:
            updated = updated.replace("version: '2025.1'", "version: '2026.1'")
        elif 'version: "2025.1"' in updated:
            updated = updated.replace('version: "2025.1"', 'version: "2026.1"')
        elif "version: " in updated and field_changes > 0:
            # Fallback: use yaml dump for the whole file
            pass  # handled below
        
        # Update lastUpdated
        last_updated_pattern = r"lastUpdated: ['\"]2025-\d{2}-\d{2}['\"]"
        updated = re.sub(last_updated_pattern, "lastUpdated: '2026-05-12'", updated)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        
        return {"file": str(filepath.relative_to(ROOT)), "text_changes": changes, "field_changes": field_changes}
    
    return {"file": str(filepath.relative_to(ROOT)), "changes": 0}


def main():
    stats = {"updated": 0, "unchanged": 0, "errors": 0, "total_changes": 0}
    
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Skip SOTA personas directory
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        
        for filename in filenames:
            if not filename.endswith(".yaml"):
                continue
            
            filepath = Path(dirpath) / filename
            result = update_yaml_file(filepath)
            
            if "error" in result:
                stats["errors"] += 1
                print(f"  ❌ {result['file']}: {result['error']}")
            elif result.get("changes", 0) == 0 and result.get("text_changes", 0) == 0:
                stats["unchanged"] += 1
            else:
                total = result.get("text_changes", 0) + result.get("field_changes", 0)
                stats["updated"] += 1
                stats["total_changes"] += total
                print(f"  ✅ {result['file']} ({total} changes)")
    
    print(f"\n📊 Summary:")
    print(f"  Updated:   {stats['updated']} files")
    print(f"  Unchanged: {stats['unchanged']} files")
    print(f"  Errors:    {stats['errors']} files")
    print(f"  Total changes: {stats['total_changes']}")


if __name__ == "__main__":
    main()
