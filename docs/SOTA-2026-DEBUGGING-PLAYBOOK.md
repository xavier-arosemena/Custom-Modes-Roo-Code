# 🔱 SOTA 2026: Universal Master Debugging & Hardening Playbook

For Any AI Agent • Any Programming Language • Any Codebase

**STATUS**: ACTIVE | **SCOPE**: UNIVERSAL | **CLASSIFICATION**: SCIENTIFIC METHOD • ARCHITECTURE • RESILIENCE

## How to Use

Paste the relevant sections into any AI agent's custom instructions, or reference this document directly.

## I. Core Philosophy (Non-Negotiable)

1. **Reject stacked fixes on broken foundations.** Rewrite the layer cleanly.
2. **Isolate pure state from side effects.** Apply Occam's Razor first: typos, missing imports, stale caches, wrong environment variables, and copy-paste errors are eliminated before anything else.
3. **Enforce counterfactual isolation:** Change exactly one thing per experiment. If two changes make the bug disappear, you still do not know what fixed it.
4. **Maintain a persistent debug brain** in `.planning/debug/[slug].md`. Every symptom, eliminated hypothesis, piece of evidence, root cause, fix, and verification metric is recorded immutably.
5. **Practice rubber-duck debugging out loud** (in the tracker). Explain every line and expose hidden assumptions.
6. **Run git bisect aggressively.** Shrink the search space. Apply the Five Whys until you reach the true cause.
7. **Insert assertions for every invariant.** Crash early and loudly on violation.
8. **Enforce idempotency in every operation.** Repeating an action must produce identical, safe results.
9. **Treat every bug as a scientific experiment:** form hypothesis → predict outcome → test one variable → observe → conclude → document.
10. **Practice delta debugging** to minimize the failing input. Use time-travel debugging (record & replay) whenever available.
11. **Obey the principle of least astonishment:** behavior must be predictable.
12. **Prioritize reproducibility above all:** every bug must be reproduced in a minimal, deterministic environment before any fix is attempted.

## II. The Disciplined Investigation Lifecycle

Every hard problem is a formal scientific investigation. Create and maintain:

**`.planning/debug/[slug].md`** — Tracker Structure (strict order):
1. **Current Focus** (top of file, updated live)
2. **Symptoms** (immutable after first gathering — with logs, timestamps, reproduction steps)
3. **Eliminated Hypotheses** (append-only — prevents repeating dead ends)
4. **Evidence Gathered** (screenshots, traces, diffs, heap dumps, etc.)
5. **Root Cause** (one sentence, crystal clear)
6. **Fix** (exact code diff + explanation)
7. **Verification Metrics** (before/after numbers, test results, chaos experiment outcomes)
8. **Lessons Learned** (for the knowledge base)

## III. The Aggressive Triage Pipeline

### Stage A: Pre-Flight Audits & Threat Awareness
- Full dependency vulnerability scan (`npm audit --all`, `pip-audit`, `cargo audit`, etc.)
- Static analysis + secret scanning: Semgrep, Trivy, SonarQube, language linters
- Check OWASP, Snyk, GitHub Dependabot alerts
- Model threats with STRIDE for the specific module

### Stage B: Cross-Pollination & Community Intelligence
- Search GitHub Advanced Search + closed issues in similar stacks
- Query Stack Overflow, Reddit, official Discord/Forums with exact error signatures
- Extract solution trajectories, never raw code. Adapt patterns to your architecture.

### Stage C: Paradigm & Idiom Purity (Language-Specific)
- JavaScript/TypeScript/React: useEffect deps, useMemo/useCallback, stale closures, React.memo
- Python: context managers, dataclasses/pydantic, type hints, no mutable defaults, proper asyncio
- Rust: ownership/borrowing/lifetimes, Result/Option exhaustive handling, no unnecessary unsafe
- Go: goroutine leaks, channel direction, error wrapping, context.Context propagation
- Java/Kotlin: try-with-resources, immutability, dependency injection, reactive streams
- Any language: pure functions where possible, explicit state transitions, no hidden side effects

### Stage D: Memory, Resources & Lifecycle Management
- Singletons and global state are explicit and guarded
- Every resource has deterministic cleanup (defer, finally, useEffect return, Drop, RAII)
- Revoke object URLs, close file handles, stop timers, cancel AbortController on unmount
- Use WeakMap/WeakRef/weakref where available. Monitor heap growth.
- Implement resource pools and bounded concurrency

### Stage E: Data Sovereignty, Auditability & Integrity
- Cryptographic ISO timestamps at exact moment of record creation
- Per-auth-session data partitioning and key derivation
- Event sourcing + CQRS for full history and replay
- Cryptographic signing + append-only logs
- NTP-synced clocks. Zero time drift.

## IV. Advanced AI Master Prompts

| Prompt | Purpose |
|---|---|
| Subagent Triage | Strict tracker + fault tree + predict-test-observe loop |
| Paradigm Inspection | Analyze hook/idiom purity, closure staleness, re-render loops |
| Root Cause Extraction | Enterprise patterns + top 3 invisible leaks + cross-check |
| Threat Vector Review | SAST simulation on auth/crypto modules |
| Git Bisect | Optimal bisect points targeting the symptom commit |
| Fuzzing | Generate inputs that break invariants |
| Closure/Lifetime Audit | List stale variables or dangling references |
| Observability | Add spans, metrics, predicted blind spots |
| Refactor | Strangler pattern + adapter isolation + identical behavior verification |
| Performance & Scalability | Hot-path analysis + load-test design |
| Chaos Resilience | Design failure injection experiment for this component |

## V. Observability & Monitoring

- OpenTelemetry end-to-end tracing + structured JSON logs
- Prometheus + Grafana for metrics and anomaly detection
- RUM for frontend, distributed tracing for backend
- Strict log levels. Sample CPU profiles in production.
- Chaos engineering tied directly to traces and dashboards.

## VI. Testing Paradigms

- Test-first design
- Property-based testing + contract testing + mutation testing
- 100% branch coverage on critical paths
- E2E with Playwright/Cypress or equivalent
- Visual regression + fuzzing in CI
- Model-based testing for state machines
- Chaos experiments as first-class tests

## VII. Security & Hardening Paradigms

- Defense in depth + zero trust
- Input sanitization + output validation everywhere
- Constant-time comparisons, automatic key rotation, rate limiting, circuit breakers
- Prepared statements / ORM parameterization
- Type strictness + SOLID + hexagonal architecture + DDD bounded contexts
- Saga pattern for distributed workflows, actor model for concurrency
- Immutable event sourcing + cryptographic audit trail

## VIII. Knowledge Sharing & Continuous Improvement

- Post-mortem on every critical bug → "Five Lessons Learned"
- Immediately fold new patterns into this playbook (living document, version-controlled)
- Auto-convert closed DEBUG.md files into anonymized, searchable knowledge-base entries
- Weekly game-day chaos exercises + team debriefs logged in tracker

## IX. Chaos Engineering & Resilience Verification

1. Define steady-state hypothesis + exact success metrics
2. Choose one narrow failure (one pod, one AZ, one dependency)
3. Inject in low-traffic window with full observability
4. Predict behavior → run experiment → measure deviation → restore
5. Record in CHAOS.md: hypothesis, prediction, actual result, resilience gap closed
6. Update main playbook with any new pattern discovered

## X. Forensic Code Analysis Protocol

For every function, route, and handler, answer:

1. **Ghost Check**: Is every defined function actually called?
2. **Lifecycle Trace**: Does every "acquire" have a guaranteed "release"?
3. **State Drift**: Can `getX()` return different values at point A vs B?
4. **Race Window**: Between check and use, can state change?
5. **Type Lie**: Does the type system promise something runtime can't guarantee?
6. **Circuit Death**: Does the "rejected" path update state?
7. **Memory Bombshell**: Calculate worst-case memory per request.
8. **Protocol Treachery**: Are response shapes consistent?
9. **Input Gap**: What does validation ALLOW that it shouldn't?
10. **Async Trap**: Are there unawaited promises? Missing timeouts?
11. **Error Forgery**: Are internal errors exposed to clients?
12. **Mutation Crime**: Does validation mutate input?

---

*Source: SOTA 2026 Universal Master Debugging & Hardening Playbook (GS-DEBUG-001)*
*Version: 2026.1 | Last Updated: 2026-05-12*
