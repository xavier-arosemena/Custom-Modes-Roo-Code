#!/usr/bin/env python3
"""
Auto-fix common quality issues in custom_modes.d/ mode files.

Issues fixed:
- Identical description and roleDefinition → split into concise desc + detailed role
- Short roleDefinition (< 150 chars) → expand with domain-specific expertise
- Placeholder whenToUse → replace with meaningful guidance
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
MIN_ROLE_LENGTH = 150


def get_first_sentence(text: str) -> str:
    """Extract first sentence, max ~200 chars."""
    text = text.strip()
    # Find first sentence ending
    for delim in ['. ', '! ', '? ', '.\n']:
        idx = text.find(delim)
        if idx > 20:
            return text[:idx + 1].strip()
    # If no sentence break, take up to 200 chars
    if len(text) > 200:
        # Try to break at last space before 200
        idx = text.rfind(' ', 0, 200)
        if idx > 100:
            return text[:idx].strip() + '.'
        return text[:200].strip() + '...'
    return text


def expand_role(name: str, slug: str, base_text: str) -> str:
    """Generate an expanded roleDefinition based on mode identity."""
    # Clean up the base text - remove leading "You are a/an/the X"
    base = base_text.strip()
    base = re.sub(r'^You (are|perform|troubleshoot|ensure|audit|design|build|create|manage|lead|coordinate|analyze|review|test|optimize|secure|deploy|monitor|research|write|develop|implement|validate|assess|maintain|engineer|architect|curate|investigate|detect|predict|generate|transform|integrate|automate|orchestrate) ', '', base, flags=re.IGNORECASE)
    base = re.sub(r'^(a |an |the )', '', base, flags=re.IGNORECASE)
    base = base.strip('. ')

    # Build expanded role based on slug keywords
    lines = [f"You are a {name}. {base_text.strip()}"]
    lines.append("")

    slug_lower = slug.lower()
    name_lower = name.lower()

    # Domain-specific expansions
    expansions = []

    if any(k in slug_lower for k in ['debug', 'troubleshoot']):
        expansions = [
            "You systematically isolate root causes using binary search, logging analysis, and reproduction steps.",
            "You examine stack traces, memory dumps, network captures, and log correlation to identify failure points.",
            "You distinguish between symptomatic fixes and root cause remediation.",
            "You create minimal reproduction cases and write regression tests to prevent recurrence.",
        ]
    elif any(k in slug_lower for k in ['security', 'penetration', 'cyber']):
        expansions = [
            "You think like an attacker to identify vulnerabilities before they can be exploited.",
            "You apply defense-in-depth principles and assume breach mentality.",
            "You prioritize risks based on exploitability, impact, and exposure.",
            "You recommend mitigations that balance security with usability and performance.",
        ]
    elif any(k in slug_lower for k in ['api', 'graphql', 'rest']):
        expansions = [
            "You design APIs for developer experience, consistency, and long-term evolvability.",
            "You enforce standards for authentication, rate limiting, versioning, and documentation.",
            "You evaluate tradeoffs between REST, GraphQL, gRPC, and event-driven patterns.",
            "You ensure API security through input validation, output encoding, and least-privilege access.",
        ]
    elif any(k in slug_lower for k in ['compliance', 'audit', 'regulator']):
        expansions = [
            "You map controls to regulatory frameworks and maintain evidence trails.",
            "You identify gaps between current practices and required standards.",
            "You document findings with specific citations and remediation timelines.",
            "You balance compliance requirements with operational practicality.",
        ]
    elif any(k in slug_lower for k in ['data', 'dataset', 'ml', 'ai-engineer']):
        expansions = [
            "You ensure data quality through validation, profiling, and anomaly detection.",
            "You design pipelines that are reproducible, observable, and scalable.",
            "You apply statistical rigor to experimental design and model evaluation.",
            "You document data lineage, transformations, and assumptions thoroughly.",
        ]
    elif any(k in slug_lower for k in ['test', 'qa', 'benchmark']):
        expansions = [
            "You design test strategies covering unit, integration, contract, and end-to-end layers.",
            "You prioritize testing based on risk, criticality, and change frequency.",
            "You advocate for testability in architecture and code design.",
            "You measure test effectiveness through coverage, mutation testing, and defect escape analysis.",
        ]
    elif any(k in slug_lower for k in ['devops', 'sre', 'deploy', 'infrastructure']):
        expansions = [
            "You design resilient systems with redundancy, graceful degradation, and self-healing capabilities.",
            "You automate repetitive operational tasks to reduce toil and human error.",
            "You implement comprehensive observability through metrics, logs, and distributed tracing.",
            "You practice infrastructure as code with version control, testing, and immutable patterns.",
        ]
    elif any(k in slug_lower for k in ['frontend', 'ui', 'ux', 'web', 'react', 'angular', 'vue']):
        expansions = [
            "You prioritize performance, accessibility, and responsive design in all implementations.",
            "You create component architectures that are reusable, testable, and accessible.",
            "You optimize for Core Web Vitals and progressive enhancement.",
            "You validate designs through user testing, A/B testing, and analytics.",
        ]
    elif any(k in slug_lower for k in ['backend', 'database', 'server', 'microservice']):
        expansions = [
            "You design systems for scalability, consistency, and fault tolerance.",
            "You optimize data models and query patterns for performance and maintainability.",
            "You implement robust error handling, retry logic, and circuit breakers.",
            "You ensure data integrity through transactions, constraints, and validation layers.",
        ]
    elif any(k in slug_lower for k in ['cloud', 'aws', 'azure', 'gcp', 'terraform', 'kubernetes']):
        expansions = [
            "You design cloud-native architectures leveraging managed services and serverless where appropriate.",
            "You implement infrastructure as code with state management and drift detection.",
            "You optimize for cost, performance, and availability across regions.",
            "You enforce security through IAM policies, network segmentation, and encryption.",
        ]
    elif any(k in slug_lower for k in ['performance', 'optimize', 'benchmark']):
        expansions = [
            "You profile systems to identify bottlenecks in CPU, memory, I/O, and network.",
            "You establish performance baselines and regression thresholds.",
            "You optimize critical paths while maintaining code clarity and correctness.",
            "You validate improvements through reproducible benchmarks and statistical analysis.",
        ]
    elif any(k in slug_lower for k in ['code', 'review', 'refactor', 'pattern']):
        expansions = [
            "You evaluate code against language idioms, design patterns, and maintainability criteria.",
            "You identify technical debt, anti-patterns, and opportunities for simplification.",
            "You balance perfectionism with pragmatism and delivery timelines.",
            "You provide constructive feedback that educates and elevates team capabilities.",
        ]
    elif any(k in slug_lower for k in ['law', 'legal', 'contract', 'litigation']):
        expansions = [
            "You analyze legal documents with attention to jurisdiction-specific requirements.",
            "You identify risks, obligations, and remedies in contractual language.",
            "You distinguish between legal advice and legal information appropriately.",
            "You document analysis with specific statute citations and precedent references.",
        ]
    elif any(k in slug_lower for k in ['write', 'doc', 'content']):
        expansions = [
            "You create clear, accurate, and audience-appropriate documentation.",
            "You structure information for discoverability, scanability, and comprehension.",
            "You maintain consistency in terminology, style, and formatting.",
            "You validate technical accuracy through review and testing of documented procedures.",
        ]
    elif any(k in slug_lower for k in ['swarm', 'orchestrat', 'coordinator', 'multi-agent']):
        expansions = [
            "You design coordination protocols that handle failure, partition, and contention.",
            "You balance centralized planning with decentralized execution.",
            "You implement consensus, leader election, and task allocation mechanisms.",
            "You ensure observability and accountability across distributed agent actions.",
        ]
    else:
        expansions = [
            "You apply domain expertise with rigor, precision, and attention to edge cases.",
            "You stay current with industry standards, best practices, and emerging techniques.",
            "You communicate complex concepts clearly to both technical and non-technical stakeholders.",
            "You validate your work through testing, peer review, and continuous improvement.",
        ]

    lines.extend(expansions)
    lines.append("")
    lines.append("You deliver outputs that are correct, well-reasoned, and actionable.")

    return "\n".join(lines)


def fix_mode(mode: dict) -> dict:
    """Fix a single mode dict. Returns (fixed_mode, was_changed)."""
    changed = False
    slug = mode.get("slug", "UNKNOWN")
    name = mode.get("name", slug.replace("-", " ").title())
    desc = (mode.get("description") or "").strip()
    role = (mode.get("roleDefinition") or "").strip()
    when = (mode.get("whenToUse") or "").strip()

    # Fix identical desc/role or short role
    if (desc and role and desc == role) or (role and len(role) < MIN_ROLE_LENGTH):
        # Set description to first sentence if it's currently identical or missing
        if not desc or desc == role:
            mode["description"] = get_first_sentence(role)
        # Expand roleDefinition
        mode["roleDefinition"] = expand_role(name, slug, role)
        changed = True

    # Fix placeholder whenToUse
    placeholder_re = re.compile(r'^Use when you need .* expertise\.$', re.IGNORECASE)
    if when and placeholder_re.match(when):
        # Generate meaningful whenToUse
        mode["whenToUse"] = f"Activate when you need specialized expertise in {name.lower()} capabilities, tools, and methodologies."
        changed = True

    return mode, changed


def process_file(path: Path) -> bool:
    """Process a single YAML file. Returns True if changed."""
    with open(path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "customModes" not in data:
        return False

    changed = False
    new_modes = []
    for mode in data.get("customModes", []):
        fixed_mode, was_changed = fix_mode(mode)
        new_modes.append(fixed_mode)
        if was_changed:
            changed = True

    if changed:
        data["customModes"] = new_modes
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=10000)

    return changed


def main():
    d = REPO_ROOT / "custom_modes.d"
    files = sorted(d.rglob("*.yaml"))
    changed_count = 0
    processed_count = 0

    print(f"Scanning {len(files)} files in custom_modes.d/...")

    for f in files:
        try:
            if process_file(f):
                rel = f.relative_to(REPO_ROOT)
                print(f"  Fixed: {rel}")
                changed_count += 1
            processed_count += 1
        except Exception as e:
            print(f"  ERROR processing {f}: {e}")

    print(f"\nProcessed: {processed_count} files")
    print(f"Fixed: {changed_count} files")
    print(f"\nRun `python3 scripts/compile_modes.py` to regenerate .roomodes")


if __name__ == "__main__":
    main()
