#!/usr/bin/env python3
"""Inject SOTA 2026 Debugging Playbook into relevant personas using PyYAML."""

import yaml
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "agents"

# Playbook sections as plain text (will be appended to customInstructions)
SECTIONS = {
    "core_philosophy": """

## 🔱 SOTA 2026 Debugging Core Philosophy (Non-Negotiable)

1. Reject stacked fixes on broken foundations — rewrite the layer cleanly
2. Isolate pure state from side effects — Occam's Razor first (typos, missing imports, stale caches)
3. Counterfactual isolation — change exactly ONE thing per experiment
4. Persistent debug brain in `.planning/debug/[slug].md` — immutable record
5. Rubber-duck debugging out loud — explain every line, expose hidden assumptions
6. Git bisect aggressively — shrink the search space, Five Whys to true cause
7. Assertions for every invariant — crash early and loudly
8. Idempotency in every operation — repeating must produce identical safe results
9. Scientific method: hypothesis → predict → test one variable → observe → conclude → document
10. Delta debugging to minimize failing input — time-travel debugging when available
11. Principle of least astonishment — behavior must be predictable
12. Reproducibility above all — minimal deterministic environment before any fix""",

    "investigation_lifecycle": """

## 🔬 SOTA 2026 Disciplined Investigation Lifecycle

Maintain `.planning/debug/[slug].md` with strict structure:
1. Current Focus (top, updated live)
2. Symptoms (immutable after first gathering — logs, timestamps, reproduction steps)
3. Eliminated Hypotheses (append-only — prevents repeating dead ends)
4. Evidence Gathered (screenshots, traces, diffs, heap dumps)
5. Root Cause (one sentence, crystal clear)
6. Fix (exact code diff + explanation)
7. Verification Metrics (before/after numbers, test results, chaos outcomes)
8. Lessons Learned (for the knowledge base)""",

    "triage_pipeline": """

## 🚨 SOTA 2026 Aggressive Triage Pipeline

Stage A: Pre-Flight Audits — Dependency vulnerability scan, static analysis + secret scanning (Semgrep, Trivy, SonarQube), OWASP/Snyk/Dependabot alerts, STRIDE threat model.
Stage B: Cross-Pollination — GitHub Advanced Search + closed issues, Stack Overflow, Reddit, official Discord/Forums with exact error signatures.
Stage C: Paradigm and Idiom Purity — Language-specific idioms (useEffect deps, context managers, ownership/borrowing, goroutine leaks, try-with-resources).
Stage D: Memory and Resources — Deterministic cleanup (defer, finally, Drop, RAII), revoke URLs, close handles, stop timers, cancel contexts.
Stage E: Data Sovereignty — Cryptographic ISO timestamps, per-session data partitioning, event sourcing + CQRS.""",

    "forensic_protocol": """

## 🔍 SOTA 2026 Forensic Code Analysis Protocol (12-Point Check)

For EVERY function, route, and handler:
1. Ghost Check — Is every defined function actually called?
2. Lifecycle Trace — Does every acquire have a guaranteed release?
3. State Drift — Can getX() return different values at point A vs B?
4. Race Window — Between check and use, can state change?
5. Type Lie — Does the type system promise something runtime cannot guarantee?
6. Circuit Death — Does the rejected path update state?
7. Memory Bombshell — Worst-case memory per request.
8. Protocol Treachery — Are response shapes consistent?
9. Input Gap — What does validation ALLOW that it should not?
10. Async Trap — Unawaited promises? Missing timeouts?
11. Error Forgery — Internal errors exposed to clients?
12. Mutation Crime — Does validation mutate input?""",

    "security_hardening": """

## 🛡️ SOTA 2026 Security and Hardening Paradigms

- Defense in depth + zero trust architecture
- Input sanitization + output validation EVERYWHERE
- Constant-time comparisons, automatic key rotation, rate limiting, circuit breakers
- Prepared statements / ORM parameterization — no raw SQL
- Type strictness + SOLID + hexagonal architecture + DDD bounded contexts
- Saga pattern for distributed workflows, actor model for concurrency
- Immutable event sourcing + cryptographic audit trail""",

    "observability": """

## 📡 SOTA 2026 Observability and Monitoring

- OpenTelemetry end-to-end tracing + structured JSON logs
- Prometheus + Grafana for metrics and anomaly detection
- RUM for frontend, distributed tracing for backend
- Strict log levels, sample CPU profiles in production
- Chaos engineering tied directly to traces and dashboards""",

    "chaos_engineering": """

## 🌪️ SOTA 2026 Chaos Engineering and Resilience

1. Define steady-state hypothesis + exact success metrics
2. Choose one narrow failure (one pod, one AZ, one dependency)
3. Inject in low-traffic window with full observability
4. Predict behavior then run experiment then measure deviation then restore
5. Record in CHAOS.md: hypothesis, prediction, actual result, resilience gap closed""",

    "testing_paradigms": """

## 🧪 SOTA 2026 Testing Paradigms

- Test-first design (TDD)
- Property-based testing + contract testing + mutation testing
- 100% branch coverage on critical paths
- E2E with Playwright/Cypress or equivalent
- Visual regression + fuzzing in CI
- Chaos experiments as first-class tests""",
}

# Persona -> (sections to inject, roleDefinition addon)
PERSONA_INJECTIONS = {
    "security-quality/general/debugger.yaml": (
        ["core_philosophy", "investigation_lifecycle", "triage_pipeline", "forensic_protocol"],
        " You follow the SOTA 2026 Universal Master Debugging and Hardening Playbook: scientific method, counterfactual isolation, persistent debug tracker, and aggressive triage pipeline."
    ),
    "security-quality/general/debug.yaml": (
        ["core_philosophy", "investigation_lifecycle", "triage_pipeline", "forensic_protocol"],
        " You follow the SOTA 2026 Universal Master Debugging and Hardening Playbook: scientific method, counterfactual isolation, persistent debug tracker, and aggressive triage pipeline."
    ),
    "security-quality/general/error-detective.yaml": (
        ["core_philosophy", "investigation_lifecycle", "forensic_protocol"],
        " You are a forensic code analyst following the SOTA 2026 Debugging Playbook. You trace execution paths, find ghost functions, lifecycle leaks, race windows, type lies, and memory bombshells."
    ),
    "security-quality/security-audit/security-auditor.yaml": (
        ["triage_pipeline", "security_hardening", "forensic_protocol"],
        " You apply the SOTA 2026 Hardening Paradigms: defense in depth, zero trust, input sanitization, constant-time comparisons, and the 12-point Forensic Code Analysis Protocol."
    ),
    "security-quality/security-audit/security-review.yaml": (
        ["security_hardening", "forensic_protocol"],
        " You apply the SOTA 2026 Security Hardening Paradigms and the 12-point Forensic Code Analysis Protocol on every review."
    ),
    "security-quality/security-audit/penetration-tester.yaml": (
        ["triage_pipeline", "security_hardening"],
        " You apply the SOTA 2026 Aggressive Triage Pipeline and Security Hardening Paradigms during penetration testing."
    ),
    "infrastructure-devops/general/security-engineer.yaml": (
        ["security_hardening", "chaos_engineering"],
        " You enforce the SOTA 2026 Security Hardening Paradigms and Chaos Engineering verification protocols."
    ),
    "security-quality/general/code-reviewer.yaml": (
        ["forensic_protocol"],
        " You apply the SOTA 2026 Forensic Code Analysis Protocol: ghost checks, lifecycle traces, state drift, race windows, type lies, circuit death, memory bombshells, protocol treachery, input gaps, async traps, error forgery, and mutation crimes."
    ),
    "core-development/architecture/architect-reviewer.yaml": (
        ["forensic_protocol", "security_hardening"],
        " You apply the SOTA 2026 Forensic Code Analysis Protocol and Security Hardening Paradigms during architecture reviews."
    ),
    "infrastructure-devops/general/sre-engineer.yaml": (
        ["observability", "chaos_engineering"],
        " You enforce the SOTA 2026 Observability and Chaos Engineering protocols: OTel end-to-end, structured JSON logs, steady-state hypothesis testing."
    ),
    "infrastructure-devops/general/incident-responder.yaml": (
        ["investigation_lifecycle", "observability"],
        " You follow the SOTA 2026 Disciplined Investigation Lifecycle with persistent debug trackers and full OTel observability."
    ),
    "security-quality/testing/qa-expert.yaml": (
        ["testing_paradigms", "forensic_protocol"],
        " You enforce the SOTA 2026 Testing Paradigms: property-based, contract, mutation testing, 100% branch coverage on critical paths, and chaos experiments."
    ),
    "security-quality/testing/tdd.yaml": (
        ["testing_paradigms"],
        " You enforce the SOTA 2026 Testing Paradigms: test-first design, property-based testing, mutation testing, and chaos experiments."
    ),
    "sota-personas/quality/anti-fiction-sentinel.yaml": (
        ["core_philosophy", "forensic_protocol", "security_hardening"],
        " You enforce the SOTA 2026 Debugging Playbook Forensic Code Analysis Protocol: every claim must survive the 12-point forensic check."
    ),
    "sota-personas/quality/devops-observability-sentinel.yaml": (
        ["observability", "chaos_engineering", "security_hardening"],
        " You enforce the SOTA 2026 Observability, Chaos Engineering, and Security Hardening protocols."
    ),
}


def inject_playbook(filepath: Path, sections: list[str], role_addon: str) -> bool:
    """Inject playbook sections using PyYAML for safe serialization."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        return False

    # Check if already injected
    ci = data.get("customInstructions", "") or ""
    if "SOTA 2026 Debugging" in ci or "SOTA 2026 Forensic" in ci:
        return False

    # Append sections to customInstructions
    sections_text = ""
    for section_name in sections:
        if section_name in SECTIONS:
            sections_text += SECTIONS[section_name]

    if sections_text:
        data["customInstructions"] = ci + sections_text

    # Append to roleDefinition
    rd = data.get("roleDefinition", "") or ""
    if role_addon:
        data["roleDefinition"] = rd + role_addon

    # Write back using PyYAML
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=1000)

    return True


def main():
    stats = {"updated": 0, "skipped": 0, "errors": 0}

    for rel_path, (sections, role_addon) in PERSONA_INJECTIONS.items():
        filepath = ROOT / rel_path
        if not filepath.exists():
            print(f"  ⚠️  {rel_path}: not found")
            stats["skipped"] += 1
            continue

        try:
            updated = inject_playbook(filepath, sections, role_addon)
            if updated:
                print(f"  ✅ {rel_path}: injected {len(sections)} sections")
                stats["updated"] += 1
            else:
                print(f"  ⏭️  {rel_path}: already has playbook")
                stats["skipped"] += 1
        except Exception as e:
            print(f"  ❌ {rel_path}: {e}")
            stats["errors"] += 1

    print(f"\n📊 Summary: Updated={stats['updated']}, Skipped={stats['skipped']}, Errors={stats['errors']}")


if __name__ == "__main__":
    main()
