#!/usr/bin/env python3
"""
Inject GitHub-sourced super powers into persona YAML files.

Sources:
  - ciembor/agent-rules-books (1,331⭐): Clean Code, Clean Architecture, Refactoring,
    Release It!, Pragmatic Programmer, Legacy Code, Data-Intensive Applications
  - mxyhi/ok-skills (332⭐): Systematic Debugging, TDD, Karpathy Guidelines
  - gadievron/raptor (2,520⭐): RAPTOR Security Research Framework
"""

import pathlib
import yaml

REPO_ROOT = pathlib.Path("/tmp/Custom-Modes-Roo-Code")
AGENTS_DIR = REPO_ROOT / "agents"

# ── Super Power Definitions ──────────────────────────────────────────────────

KARPATHY_GUIDELINES = r"""
## 🧠 Karpathy Guidelines (SOTA Coding Behavior Layer)

Behavioral guidelines derived from Andrej Karpathy's observations on LLM coding pitfalls. Apply to ALL coding tasks.

### 1. Think Before Coding
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
- No features beyond what was asked. No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- If you write 200 lines and it could be 50, rewrite it.
- Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken. Match existing style.
- Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution
- Transform tasks into verifiable goals with success criteria.
- For multi-step tasks, state a brief plan with verify checkpoints.
- Strong success criteria let you loop independently.
"""

SYSTEMATIC_DEBUGGING = r"""
## 🔍 Systematic Debugging Protocol (from ok-skills)

### The Iron Law
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

### Phase 1: Root Cause Investigation
1. Read error messages carefully — they often contain the exact solution.
2. Reproduce consistently — can you trigger it reliably?
3. Check recent changes — git diff, recent commits, new dependencies.
4. Gather evidence at EACH component boundary in multi-component systems.
5. Trace data flow backward from the error to find the source.

### Phase 2: Pattern Analysis
1. Find working examples in the same codebase.
2. Compare against reference implementations COMPLETELY — don't skim.
3. List every difference between working and broken, however small.

### Phase 3: Hypothesis and Testing
1. Form a SINGLE hypothesis: "I think X is the root cause because Y."
2. Make the SMALLEST possible change to test it. One variable at a time.
3. If it didn't work → form NEW hypothesis. DON'T stack fixes.

### Phase 4: Implementation
1. Create a failing test case first (simplest possible reproduction).
2. Implement single fix addressing the root cause.
3. Verify: test passes, no other tests broken, issue actually resolved.
4. If 3+ fixes failed → STOP and question the architecture.

### Red Flags — STOP and Follow Process
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- Proposing solutions before tracing data flow
- "One more fix attempt" when already tried 2+
"""

CLEAN_CODE_RULES = r"""
## 📖 Clean Code Rules (from agent-rules-books/Clean Code)

### Decision Rules
- Treat cleanliness as part of delivery. Leave touched code cleaner within scope.
- Write for local reasoning. A reader should understand the path without reconstructing hidden state.
- Use precise names and one term per concept. Rename when vocabulary hides intent.
- Keep functions small, focused, and at one level of abstraction. Tell the story top-down.
- Keep parameters few and meaningful. Avoid boolean flags and output parameters.
- Separate commands from queries. A function that answers should not also mutate.
- Keep the happy path readable. Isolate error handling and invalid-state handling.
- Expose behavior rather than raw representation. Avoid train-wreck access.
- Make public APIs small, explicit, and hard to misuse.
- Use comments only for rationale, constraints, warnings, or external contracts.
- Treat tests as production code: readable, deterministic, aligned with the behavior they protect.

### Trigger Rules
- When a function mixes setup, validation, computation, and side effects → split the phases.
- When a comment explains control flow → simplify names or structure before keeping the comment.
- When a function both mutates and answers → separate the responsibilities.
- When duplication, repeated switches, or primitive clusters appear → name the concept.
- When a boundary leaks framework quirks inward → add or strengthen a local adapter.
- When fixing a bug → add or update the test that protects the intended contract.
"""

CLEAN_ARCHITECTURE_RULES = r"""
## 🏛️ Clean Architecture Rules (from agent-rules-books/Clean Architecture)

### Decision Rules
- Source dependencies must point inward toward higher-level policy. Domain must not import frameworks, databases, or external services.
- Put enterprise rules in entities; put application-specific orchestration in focused use cases.
- Pass plain request/response models across use-case boundaries. No web requests, ORM rows, or framework objects in core policy.
- Treat frameworks, databases, web delivery, messaging, and external services as outer-layer details behind adapters.
- Inner layers own the interfaces they need; outer layers implement them.
- Keep adapters humble — they translate external formats, they do not own business decisions.
- Organize by use case, feature, or business capability before generic technical buckets.
- Do not merge unrelated use cases or eliminate duplication when sharing would couple actors.
- Test entities, use cases, and boundary contracts first without real infrastructure.

### Trigger Rules
- When framework annotations enter core policy → move translation outward.
- When controllers contain business branching → move the rule inward.
- When a use case depends on a concrete implementation → introduce a policy-owned port.
- When a shared module becomes an escape hatch → split by use case or ownership.
"""

RELEASE_IT_RULES = r"""
## 🚀 Release It! Production Stability Rules (from agent-rules-books/Release It!)

### Decision Rules
- Treat every external call, shared resource, network hop, and integration point as a potential failure source.
- Use timeouts on all external calls. Default to fail-fast; use longer timeouts only when the caller can usefully wait.
- Use circuit breakers around external dependencies. Open the breaker after repeated failures; give the dependency time to recover.
- Use bulkheads to isolate critical paths from non-critical failures. One slow downstream service must not exhaust threads or connections.
- Limit retries with exponential backoff and jitter. Unlimited retries amplify load during outages.
- Validate input at system boundaries. Reject malformed data before it enters processing.
- Design for graceful degradation. Shed load, return cached data, or disable features rather than cascading failure.
- Make every state transition explicit and recoverable. Avoid implicit state machines in flags, nulls, or status strings.
- Use health checks that verify real dependency availability, not just process liveness.
- Ensure logging, tracing, and metrics cover every external call, state transition, and error path.

### Trigger Rules
- When adding an external call → add timeout, circuit breaker, and error logging.
- When a shared resource has no limit → add a pool, semaphore, or queue with backpressure.
- When a failure path has no recovery → add fallback, cache, or graceful degradation.
- When a slow operation blocks critical work → move it to a bulkhead or async path.
"""

PRAGMATIC_PROGRAMMER_RULES = r"""
## 🔨 Pragmatic Programmer Rules (from agent-rules-books/The Pragmatic Programmer)

### Decision Rules
- Take responsibility for every line you touch. "That's how I found it" is not acceptable.
- Don't repeat yourself at the knowledge level. When one fact changes, update it in one place.
- Keep orthogonal designs: changes in one area should not cascade into unrelated areas.
- Eliminate effects between unrelated things. Reduce coupling to essential interactions.
- Prototype to learn; tracer bullets to build. State what the prototype proves and which shortcuts must be discarded.
- Dig for real requirements. Separate durable needs from current implementation details.
- Automate repetitive, error-prone, or ritualized work. Builds, tests, deployment should be reproducible.
- Shorten feedback loops with relevant tests and automated checks before late expensive surprises.
- Make contracts, assumptions, and invariants explicit and close to the abstraction they protect.
- Distinguish programmer errors, contract violations, expected failures, retryable failures, and permanent failures.
- Debug from reproduced facts: observe, isolate, explain, fix, verify — before guessing.
- Break work into small deliverable increments with honest uncertainty and visible risk.
- Apply the broken windows rule: fix or visibly contain small quality decay before it becomes normal.

### Trigger Rules
- When one change requires edits in many unrelated places → repair the missing boundary.
- When volatile details are hard-coded → move them into validated configuration.
- When uncertainty is high → reduce risk with tracer feedback or a prototype.
- When repeated manual steps appear → automate and version them.
- When a human finds a bug → add an automatic regression test.
"""

LEGACY_CODE_RULES = r"""
## 🏚️ Working Effectively with Legacy Code Rules (from agent-rules-books)

### Decision Rules
- Treat untested or weakly tested code as legacy code. Do not start with rewrite unless explicitly required.
- Before editing, state the requested behavior change and the current behavior that must remain.
- Follow the legacy loop: identify change point → check existing protection → add characterization → find/create seam → break dependency → change behavior → refactor locally.
- Prefer fast, focused tests around the slice being changed.
- Choose test points by tracing effects outward from the change point.
- Use the smallest seam that allows substitution, observation, or interception.
- Keep behavior changes, structural refactorings, and cleanup separate.
- For hard-to-test methods: split construction from use, extract side effects, carve pure computation first.
- Leave the touched area easier to understand, test, or change.

### Trigger Rules
- When behavior is uncertain → add characterization before changing semantics.
- When tests require too much setup → break the first real barrier (constructor work, hidden allocation, global state).
- When a large method defeats local reasoning → sketch effects, find pinch points, extract pure computation first.
- When changing database-heavy or framework-bound code → separate policy from persistence.
- When rewrite feels tempting → choose the smallest sprout, wrap, or seam step instead.
"""

DATA_INTENSIVE_RULES = r"""
## 📊 Designing Data-Intensive Applications Rules (from agent-rules-books)

### Decision Rules
- Make core trade-offs explicit: source of truth, consistency, retry behavior, duplicate work, partial failure.
- Treat crashes, partial writes, duplicate work, timeouts, and stale reads as normal inputs.
- Describe load and performance with concrete request rates, data volume, access patterns, and percentiles.
- Choose data models from relationships, access patterns, consistency needs, and update locality.
- Treat caches, indexes, and materialized views as derived data with explicit propagation and repair paths.
- Make commands, jobs, events, and stream processors safe under retry and replay with deduplication or idempotent transitions.
- Preserve only the ordering the business logic actually needs. Scope it per key, stream, or partition.
- Design schemas, APIs, and messages as evolving contracts across old and new readers/writers.
- Align service boundaries with data ownership. Don't split one consistent concept across services.

### Trigger Rules
- When changing a write path → state source of truth, durability point, and rollback path.
- When adding a cache or index → define ownership, propagation, staleness, and rebuild.
- When changing a schema → plan compatibility for old readers, old writers, and rolling upgrades.
- When adding retries or queues → prove duplicate, replay, and ordering safety.
"""

TDD_RULES = r"""
## ✅ TDD Best Practices (from ok-skills)

### Philosophy
- Tests should verify behavior through public interfaces, not implementation details.
- Good tests are integration-style: they exercise real code paths through public APIs.
- Bad tests are coupled to implementation — they break when you refactor but behavior hasn't changed.

### Anti-Pattern: Horizontal Slices
- DO NOT write all tests first, then all implementation. This produces crap tests.
- Correct approach: Vertical slices via tracer bullets. One test → one implementation → repeat.
- Each test responds to what you learned from the previous cycle.

### Process
1. Write ONE failing test for the next behavior.
2. Write the MINIMUM implementation to make it pass.
3. Refactor while tests stay green.
4. Repeat.
"""

RAPTOR_SECURITY = r"""
## 🦅 RAPTOR Security Research Methodology (from gadievron/raptor)

### Pipeline Stages
1. **Understand** — Map attack surface: entry points, trust boundaries, sinks before scanning.
2. **Scan** — Static analysis (Semgrep, CodeQL) with deduplication.
3. **Validate** — Multi-stage exploitation validation:
   - Stage A: Is the pattern actually a vulnerability, or tool noise?
   - Stage B: What does an attacker need to reach it? What gets in the way?
   - Stage C: Does the code path actually exist? Can it be reached from outside?
   - Stage D: Final call — is this test code? Does it need unrealistic preconditions?
4. **Exploit** — Generate proof-of-concept for confirmed vulnerabilities.
5. **Patch** — Generate secure patches. Cross-finding analysis for shared root causes.

### Key Principles
- Z3 SMT integration for constraint checking: drop provably unreachable paths before LLM analysis.
- Evidence-backed findings only. No speculation.
- Findings that clear validation get exploit PoCs AND patches.
- Cross-finding analysis at the end to find shared root causes and attack chains.
"""

# ── Persona → Skill Mapping ──────────────────────────────────────────────────

SKILL_MAP = {
    # Karpathy Guidelines → ALL development personas
    "KARPATHY": {
        "skills": [KARPATHY_GUIDELINES],
        "slugs": [
            "code-reviewer", "code-skeptic", "refactoring-specialist",
            "backend-developer", "frontend-developer", "fullstack-developer",
            "full-stack-developer", "python-pro", "typescript-pro", "javascript-pro",
            "golang-pro", "rust-engineer", "cpp-pro", "csharp-developer",
            "java-architect", "kotlin-specialist", "swift-expert",
            "react-specialist", "nextjs-developer", "vue-expert",
            "django-developer", "rails-expert", "laravel-specialist",
            "spring-boot-engineer", "dotnet-core-expert", "flutter-expert",
            "silent-coder", "tdd",
        ],
    },
    # Systematic Debugging → debug/error personas
    "DEBUGGING": {
        "skills": [SYSTEMATIC_DEBUGGING],
        "slugs": [
            "debugger", "debugging-expert", "error-detective",
            "error-coordinator", "performance-engineer",
        ],
    },
    # Clean Code → code quality personas
    "CLEAN_CODE": {
        "skills": [CLEAN_CODE_RULES],
        "slugs": [
            "code-reviewer", "code-skeptic", "refactoring-specialist",
            "qa-expert", "tdd",
        ],
    },
    # Clean Architecture → architect/backend personas
    "CLEAN_ARCH": {
        "skills": [CLEAN_ARCHITECTURE_RULES],
        "slugs": [
            "architect-reviewer", "backend-developer", "fullstack-developer",
            "full-stack-developer", "microservices-architect",
            "platform-engineer", "refactoring-specialist",
        ],
    },
    # Release It! → SRE/DevOps personas
    "RELEASE_IT": {
        "skills": [RELEASE_IT_RULES],
        "slugs": [
            "sre-engineer", "devops-engineer", "devops",
            "performance-engineer", "performance-monitor",
            "incident-responder", "incident-command-director",
            "chaos-engineer", "observability-architect",
        ],
    },
    # Pragmatic Programmer → broad dev personas
    "PRAGMATIC": {
        "skills": [PRAGMATIC_PROGRAMMER_RULES],
        "slugs": [
            "code-reviewer", "code-skeptic", "fullstack-developer",
            "full-stack-developer", "backend-developer",
            "tooling-engineer", "dx-optimizer",
        ],
    },
    # Legacy Code → legacy modernizer
    "LEGACY": {
        "skills": [LEGACY_CODE_RULES],
        "slugs": [
            "legacy-modernizer", "refactoring-specialist",
        ],
    },
    # Data-Intensive → data/backend personas
    "DATA_INTENSIVE": {
        "skills": [DATA_INTENSIVE_RULES],
        "slugs": [
            "data-engineer", "database-administrator", "database-optimizer",
            "sql-pro", "postgres-pro", "backend-developer",
        ],
    },
    # TDD → TDD/QA personas
    "TDD": {
        "skills": [TDD_RULES],
        "slugs": [
            "tdd", "qa-expert",
        ],
    },
    # RAPTOR Security → security personas
    "RAPTOR": {
        "skills": [RAPTOR_SECURITY],
        "slugs": [
            "cybersecurity-expert", "penetration-tester", "security-auditor",
            "security-engineer", "security-review",
        ],
    },
}


def find_yaml_files():
    """Find all YAML files and build slug → path mapping."""
    slug_to_path = {}
    for yaml_file in AGENTS_DIR.rglob("*.yaml"):
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data and "slug" in data:
            slug_to_path[data["slug"]] = yaml_file
    return slug_to_path


def main():
    slug_to_path = find_yaml_files()
    print(f"Found {len(slug_to_path)} agent YAML files\n")

    # Track which files were modified
    modified = {}  # path → set of skill names injected

    for skill_name, config in SKILL_MAP.items():
        for slug in config["slugs"]:
            if slug not in slug_to_path:
                continue

            path = slug_to_path[slug]
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            instructions = data.get("customInstructions", "")

            # Check if already injected using a unique marker per skill
            markers = {
                "KARPATHY": "Karpathy Guidelines (SOTA Coding Behavior Layer)",
                "DEBUGGING": "Systematic Debugging Protocol (from ok-skills)",
                "CLEAN_CODE": "Clean Code Rules (from agent-rules-books",
                "CLEAN_ARCH": "Clean Architecture Rules (from agent-rules-books",
                "RELEASE_IT": "Release It! Production Stability Rules",
                "PRAGMATIC": "Pragmatic Programmer Rules (from agent-rules-books",
                "LEGACY": "Working Effectively with Legacy Code Rules",
                "DATA_INTENSIVE": "Data-Intensive Applications Rules",
                "TDD": "TDD Best Practices (from ok-skills)",
                "RAPTOR": "RAPTOR Security Research Methodology",
            }
            marker = markers.get(skill_name, "")
            if marker and marker in instructions:
                continue

            # Append all skills for this mapping
            for skill_text in config["skills"]:
                instructions += skill_text

            data["customInstructions"] = instructions

            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                         sort_keys=False, width=10000)

            if path not in modified:
                modified[path] = set()
            modified[path].add(skill_name)

    # Report
    print(f"Modified {len(modified)} files:\n")
    for path, skills in sorted(modified.items()):
        name = path.stem
        skill_list = ", ".join(sorted(skills))
        print(f"  ✅ {name}: {skill_list}")

    print(f"\nDone. {len(modified)} files updated with GitHub-sourced super powers.")


if __name__ == "__main__":
    main()
