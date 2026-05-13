# Agent Brief: Rewrite 72 Custom Modes for Roo Code

## Context
Repository: `jtgsystems/Custom-Modes-Roo-Code`
- `custom_modes.d/*/` — 305 individual mode YAML files (source of truth)
- `scripts/compile_modes.py` — compiles individual files into `.roomodes`
- `scripts/verify_modes.py` — validates schema and quality

## Problem
72 modes were auto-fixed by a script. They pass schema validation but have **generic, templated content**. The `roleDefinition` fields read like cookie-cutter expansions rather than genuine domain expertise. These need human-quality rewriting.

## Target Files
The 72 modes listed below. Each lives at `custom_modes.d/{slug}/{slug}.yaml`.

```
ai-prompt-security-specialist, api-contract-first-developer, api-governance-lead,
ask, bff-engineer, bullshit-detection-analyst, chaos-resilience-lead,
cli-tool-developer, cloud-security-architect, compiler-engineer,
compliance-auditor-canada, compliance-auditor-usa, compliance-automation-engineer,
compliance-specialist-canada, compliance-specialist-usa, concurrency-specialist,
corporate-law-canada, corporate-law-usa, criminal-law-canada, criminal-law-usa,
data-pipeline-engineer, database-migration-engineer, dataset-curator, debug,
docs-writer, edge-computing-architect, employment-law-canada, employment-law-usa,
experience-polish-director, feature-flag-orchestrator, finops-optimizer,
framework-currency, frontend-architecture-engineer, frontend-performance-auditor,
graphql-resolver-writer, growth-experimentation-lead, hardware-acceleration-engineer,
i18n-l10n-reviewer, incident-command-director, integration,
intellectual-property-canada, intellectual-property-usa, litigation-support-canada,
litigation-support-usa, mode-orchestrator, model-registry-auditor,
observability-architect, oss-license-auditor, performance-benchmark,
policy-as-code-auditor, post-deployment-monitoring-mode, product-analytics-scientist,
rag-evaluator, react-optimization-director, realtime-collaboration-engineer,
refinement-optimization-mode, release-governance-lead, sdk-developer,
secrets-hygiene-auditor, security-review, serverless-platform-architect,
silent-coder, site-readiness-engineer, spec-pseudocode,
streaming-systems-engineer, supply-chain-security-auditor, tdd,
tech-research-strategist, terraform-module-author, wasm-systems-developer,
website-foundation-planner, zero-trust-strategist
```

## Schema (Roo Code Official)
```yaml
customModes:
  - slug: kebab-case-id          # REQUIRED, ^[a-zA-Z0-9-]+$
    name: Display Name           # REQUIRED
    roleDefinition: >-           # REQUIRED, detailed persona (300-800 chars)
      You are a [Role]. [What you do]. [How you approach problems].
      [Domain-specific methodologies]. [Quality standards].
    description: >-              # OPTIONAL, 1-2 sentence summary (80-150 chars)
      Concise summary of what this mode does and when it's useful.
    whenToUse: >-                # OPTIONAL, activation guidance (80-200 chars)
      Specific scenarios where this mode should be activated.
    groups:                      # REQUIRED
      - read
      - edit
      - command
      - mcp
    customInstructions: >-       # OPTIONAL, detailed behavioral instructions
      Specific workflows, patterns, tools, and constraints.
```

**CRITICAL RULES:**
- NO `emoji` field (causes silent failure in Roo Code)
- NO `category`, `subcategory`, `version`, `lastUpdated` fields
- `description` MUST differ from `roleDefinition`
- `roleDefinition` MUST be ≥150 chars and contain genuine expertise
- `description` MUST be 80-150 chars, concise summary only
- `groups` allowed: `read`, `edit`, `command`, `mcp` (`browser` deprecated but tolerated)

## Quality Standard

### BAD (current auto-fixed state):
```yaml
roleDefinition: >-
  You are a Debugger. You troubleshoot runtime bugs...

  You systematically isolate root causes using binary search...
  You examine stack traces, memory dumps...
  You distinguish between symptomatic fixes...
  You deliver outputs that are correct...
```
Generic bullet points that could apply to any technical role.

### GOOD (reference: existing high-quality modes):
```yaml
roleDefinition: >-
  You are an expert debugging specialist who systematically eliminates unknowns
  to find root causes of software failures. You combine static analysis, dynamic
  tracing, and environmental inspection to reproduce and isolate bugs. You think
  in terms of hypotheses, experiments, and evidence — never guessing. You produce
  minimal reproduction cases, write regression tests, and document failure modes
  so they never recur. You understand memory corruption, race conditions,
  deadlocks, performance regressions, and Heisenbugs. You instrument code when
  necessary and read core dumps, stack traces, and logs with precision.
```
Specific domain knowledge, concrete techniques, recognizable expertise.

## Instructions for gemma4:e2b

1. **Read** each of the 72 YAML files in `custom_modes.d/`
2. **Analyze** the `slug` and `name` to understand the actual domain
3. **Rewrite** the following fields with genuine expertise:
   - `roleDefinition` → 300-600 chars of specific domain persona
   - `description` → 1-2 sentence summary (different from roleDefinition)
   - `whenToUse` → specific activation scenarios
   - `customInstructions` → detailed behavioral guidance with domain-specific workflows
4. **Preserve** existing `slug`, `name`, `groups`
5. **Do NOT add** unsupported fields (emoji, category, version, lastUpdated)
6. **Run** `python3 scripts/verify_modes.py` after each batch to confirm clean
7. **Run** `python3 scripts/compile_modes.py` when done to regenerate `.roomodes`

## Verification Checklist
- [ ] All 72 files rewritten with non-generic content
- [ ] `python3 scripts/verify_modes.py` returns ✅ ALL CHECKS PASSED
- [ ] `python3 scripts/compile_modes.py` completes without errors
- [ ] `.roomodes` and `custom_modes.yaml` contain 305 modes
- [ ] No duplicate slugs, no double dashes, no missing required fields
- [ ] `description` != `roleDefinition` for all 72 modes
- [ ] Each roleDefinition reads like actual domain expertise, not a template

## Example: Before → After

### Before (auto-fixed):
```yaml
customModes:
  - slug: debug
    name: 🪲 Debugger
    description: You troubleshoot runtime bugs, logic errors, or integration failures...
    roleDefinition: >-
      You are a 🪲 Debugger. You troubleshoot runtime bugs...

      You systematically isolate root causes using binary search...
      You examine stack traces, memory dumps...
      You distinguish between symptomatic fixes...
      You deliver outputs that are correct...
    whenToUse: Use when you need 🪲 Debugger expertise.
```

### After (target quality):
```yaml
customModes:
  - slug: debug
    name: Debugger
    description: Systematically isolates root causes of runtime failures through
      tracing, reproduction, and evidence-based analysis.
    roleDefinition: >-
      You are an expert debugging specialist who systematically eliminates unknowns
      to find root causes of software failures. You combine static analysis,
      dynamic tracing, and environmental inspection to reproduce and isolate bugs.
      You think in terms of hypotheses, experiments, and evidence — never guessing.
      You produce minimal reproduction cases, write regression tests, and document
      failure modes so they never recur. You understand memory corruption, race
      conditions, deadlocks, performance regressions, and Heisenbugs. You instrument
      code when necessary and read core dumps, stack traces, and logs with precision.
    whenToUse: >-
      Activate when investigating runtime crashes, flaky tests, memory leaks,
      performance regressions, or any behavior that deviates from expected output.
    groups:
      - read
      - edit
      - browser
      - command
      - mcp
    customInstructions: >-
      Start by reproducing the issue reliably. If you cannot reproduce it, you
      cannot fix it. Use binary search on commits, configuration, or inputs to
      narrow the failure window. Check environment differences (OS, versions,
      dependencies, timing). Produce a minimal reproduction case before proposing
      fixes. Write regression tests that fail before the fix and pass after.
      Document the root cause, not just the symptom. Distinguish between fixes
      that mask problems and fixes that eliminate them.
```
