# Agent Brief for gemma4:e2b — Sequential Mode Improvement

## Goal
Improve the quality of 305 Roo Code custom modes stored in `custom_modes.d/*/`.
Process **one mode at a time**, sequentially. Do **not** trim or remove content.

## Why Sequential?
If you process all modes at once, you may:
- Run out of context window
- Apply generic templates that hurt quality
- Miss mode-specific nuances

Processing one mode at a time ensures each gets proper attention.

## Directory Structure
```
custom_modes.d/
  {slug}/
    {slug}.yaml
```

Each YAML file contains:
```yaml
customModes:
  - slug: mode-slug
    name: Mode Name
    roleDefinition: >-      # Detailed persona
    description: >-         # 1-2 sentence summary
    whenToUse: >-           # When to activate
    customInstructions: >-  # Detailed behavioral guidance
    groups:
      - read
      - edit
      - command
      - mcp
```

## Schema Rules (HARD CONSTRAINTS)
- `slug`: kebab-case, `^[a-zA-Z0-9-]+$`, NO double dashes
- `name`: display name (can contain emoji in name, but NO `emoji` field)
- `roleDefinition`: REQUIRED, detailed persona
- `description`: OPTIONAL but should differ from `roleDefinition`
- `whenToUse`: OPTIONAL, specific activation guidance
- `groups`: REQUIRED, from `{read, edit, command, mcp}` (`browser` tolerated)
- `customInstructions`: OPTIONAL, detailed workflows
- **NO** `emoji`, `category`, `subcategory`, `version`, `lastUpdated` fields

## What to Fix (per mode)

### 1. Identical `description` and `roleDefinition`
If they are identical, split them:
- `description`: Concise 1-2 sentence summary (80-150 chars)
- `roleDefinition`: Detailed persona with domain expertise (300-800 chars)

### 2. Short `roleDefinition` (< 150 chars)
Expand with genuine domain expertise. Include:
- Specific methodologies and tools
- Quality standards and practices
- Concrete responsibilities (not generic fluff)

### 3. Placeholder `whenToUse`
Replace "Use when you need X expertise" with:
- Specific scenarios where this mode adds value
- What problems it solves
- When NOT to use it

### 4. Weak `customInstructions`
If present but generic, enhance with:
- Step-by-step workflows
- Decision trees
- Quality checkpoints
- Tool-specific guidance

## Sequential Process

For EACH mode file in `custom_modes.d/` (alphabetical order):

1. **READ** the file
2. **ANALYZE**: Check for the 4 issues above
3. **REWRITE**: Fix issues, preserve all valuable content
4. **VERIFY**: Run `python3 scripts/verify_modes.py` — must pass
5. **COMMIT** (optional): `git add {file} && git commit -m "improve: {slug}"`
6. **NEXT**: Move to the next mode file

## Verification
After each mode, run:
```bash
python3 scripts/verify_modes.py
```
Must output: `✅ ALL CHECKS PASSED`

After every ~10 modes, run:
```bash
python3 scripts/compile_modes.py
```
To regenerate `.roomodes` and `custom_modes.yaml`.

## Quality Examples

### BAD — Identical and short:
```yaml
description: You debug code.
roleDefinition: You debug code.
whenToUse: Use when you need debug expertise.
```

### GOOD — Differentiated and detailed:
```yaml
description: Systematically isolates root causes of runtime failures through
  tracing, reproduction, and evidence-based analysis.
roleDefinition: >-
  You are an expert debugging specialist who eliminates unknowns to find root
  causes. You combine static analysis, dynamic tracing, and environmental
  inspection. You produce minimal reproduction cases, write regression tests,
  and document failure modes. You understand memory corruption, race
  conditions, deadlocks, and Heisenbugs.
whenToUse: >-
  Activate when investigating crashes, flaky tests, memory leaks, or any
  behavior that deviates from expected output. Also use when logs or stack
  traces need expert interpretation.
```

## Commands
```bash
# List all mode files to process
find custom_modes.d -name "*.yaml" | sort

# Test one mode individually
cp custom_modes.d/debug/debug.yaml /tmp/test-mode.yaml

# Verify all modes
python3 scripts/verify_modes.py

# Compile to .roomodes
python3 scripts/compile_modes.py

# Test a single mode in Roo Code
python3 scripts/batch_roomodes.py --single debug
cp .roomodes.single-debug .roomodes
# Then reload VS Code window
```

## Critical Rules
1. **ONE mode at a time** — finish it completely before starting the next
2. **DO NOT trim** — preserve all valuable content, just restructure and enhance
3. **DO NOT add unsupported fields** — no emoji, category, version, lastUpdated
4. **Verify after EACH mode** — never batch-verify, always check immediately
5. **If unsure, ask** — stop and ask the user rather than guessing
