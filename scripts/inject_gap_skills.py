#!/usr/bin/env python3
"""
Fill gaps: inject TerminalSkills-sourced super powers into remaining 162 personas.

Sources:
  - TerminalSkills/skills (github.com/TerminalSkills/skills)
  - mxyhi/ok-skills (github.com/mxyhi/ok-skills)
"""

import pathlib
import yaml

REPO_ROOT = pathlib.Path("/tmp/Custom-Modes-Roo-Code")
AGENTS_DIR = REPO_ROOT / "agents"

# ── Skill Definitions (condensed from TerminalSkills) ────────────────────────

SYSTEMS_THINKING = r"""
## 🧠 Systems Thinking Framework (from TerminalSkills)

### Gall's Law
A complex system that works invariably evolved from a simple system that worked. Don't design complex solutions upfront — build the simplest version that works, then iterate.

### Theory of Constraints (5 Focusing Steps)
1. **IDENTIFY** the constraint — What single thing limits the system's output?
2. **EXPLOIT** the constraint — Get maximum output from the constraint as-is
3. **SUBORDINATE** everything else — All other processes serve the constraint
4. **ELEVATE** the constraint — Invest in expanding the constraint's capacity
5. **REPEAT** — Once this constraint is broken, find the NEW constraint

### Feedback Loops
- **Reinforcing loops** amplify change (viral growth, compound interest, skill development)
- **Balancing loops** resist change (market saturation, resource limits, regulation)
- Map both to predict system behavior and find leverage points.

### Second-Order Effects
Before making any change, ask: "And then what?" Trace at least 3 levels of consequences.
"""

CONTEXT_ENGINEERING = r"""
## 🔧 Context Engineering (from TerminalSkills)

### The Context Hierarchy
Structure context from most persistent to most transient:
1. **Rules Files** (CLAUDE.md, etc.) — Always loaded, project-wide
2. **Spec / Architecture Docs** — Loaded per feature/session
3. **Relevant Source Files** — Loaded per task
4. **Error Output / Test Results** — Loaded per iteration
5. **Conversation History** — Accumulates, compacts

### Packing Strategies
- **Front-load critical context**: Put the most important information first
- **Signal vs Noise**: Include only what the agent needs for THIS task
- **Progressive disclosure**: Start high-level, drill down on demand
- **Compact when drifting**: If output quality degrades, summarize and reset context

### Anti-Patterns
- Dumping entire codebases into context (noise drowns signal)
- Ignoring rules files (missed leverage point)
- Not refreshing stale context (agent works from outdated assumptions)
"""

PROMPT_ENGINEERING_SOTA = r"""
## ✨ SOTA Prompt Engineering Techniques (from TerminalSkills)

### Core Techniques
- **Zero-Shot**: Direct instruction, no examples. Works for clear, simple tasks.
- **Few-Shot**: 2-5 examples to guide format and style. Use diverse, representative examples.
- **Chain-of-Thought (CoT)**: "Think step by step" — forces reasoning before answer.
- **Tree-of-Thought (ToT)**: Explore multiple reasoning paths, evaluate each, pick best.
- **ReAct**: Reason + Act loop — think, use tool, observe, repeat.
- **Self-Consistency**: Sample multiple reasoning paths, take majority vote.
- **Meta-Prompting**: Ask the model to improve its own prompt.

### Structured Output
- Use JSON Schema or Pydantic models to enforce output format
- Provide explicit examples of desired output structure
- Add "Respond only with valid JSON" constraints

### Anti-Patterns
- Overly long prompts (diminishing returns after ~2000 tokens of instruction)
- Contradictory instructions (causes unpredictable behavior)
- Missing edge case handling (model fills gaps with hallucinations)
"""

FRONTEND_DESIGN = r"""
## 🎨 Frontend Design Principles (from TerminalSkills)

### Component Architecture
- Design from atomic → molecular → organism → template → page
- Components should be: Composable, Accessible, Performant, Testable
- Use compound components for complex UIs (select + option, tabs + tabpanel)

### Visual Hierarchy
- **F-pattern** for content-heavy pages, **Z-pattern** for landing pages
- Size, color, contrast, whitespace guide the eye
- One primary action per view, maximum 3 secondary actions

### Responsive Strategy
- Mobile-first: Start from smallest screen, progressively enhance
- Use container queries over media queries where supported
- Fluid typography: clamp(1rem, 2.5vw, 1.5rem)

### Performance Budget
- First Contentful Paint < 1.8s
- Largest Contentful Paint < 2.5s
- Total JavaScript < 200KB compressed
- CSS < 50KB compressed
"""

WEB_VITALS = r"""
## ⚡ Web Vitals Analysis Protocol (from TerminalSkills)

### Core Web Vitals (2026)
- **LCP** (Largest Contentful Paint) ≤ 2.5s — measures loading performance
- **INP** (Interaction to Next Paint) ≤ 200ms — measures interactivity
- **CLS** (Cumulative Layout Shift) ≤ 0.1 — measures visual stability

### Diagnostic Approach
1. Measure with Lighthouse CI + WebPageTest + Chrome UX Report
2. Identify worst-performing pages from CrUX data
3. Trace each poor metric to specific resources/code
4. Fix: preload critical resources, lazy-load below-fold, optimize images
5. Verify: re-measure after each fix, one variable at a time

### Common Fixes
- LCP: Preload hero image, eliminate render-blocking CSS, use CDN
- INP: Break long tasks, use requestIdleCallback, code-split
- CLS: Set explicit dimensions, avoid dynamic content injection, use font-display: swap
"""

ACCESSIBILITY_AUDIT = r"""
## ♿ Accessibility Audit Protocol (from TerminalSkills)

### WCAG 2.2 Compliance Checklist
- **Perceivable**: Alt text on images, captions on video, sufficient color contrast (4.5:1)
- **Operable**: Keyboard navigation, focus indicators, no time limits, skip links
- **Understandable**: Clear labels, error messages, consistent navigation
- **Robust**: Valid HTML, ARIA attributes, screen reader compatible

### Testing Approach
1. Automated: axe-core, Lighthouse accessibility audit, pa11y
2. Manual: Keyboard-only navigation test, screen reader test (NVDA/VoiceOver)
3. User testing: Include users with disabilities in testing

### Common Issues
- Missing alt text on images and icons
- Form inputs without associated labels
- Interactive elements not keyboard-accessible
- Insufficient color contrast ratios
- Missing ARIA live regions for dynamic content
"""

OBSERVABILITY_SETUP = r"""
## 📡 Observability Setup Protocol (from TerminalSkills)

### The Three Pillars
1. **Metrics**: Counter, gauge, histogram — track SLIs (latency, error rate, throughput, saturation)
2. **Logs**: Structured JSON, correlation IDs, log levels (debug/info/warn/error)
3. **Traces**: Distributed tracing with OpenTelemetry — trace request across services

### SLO Framework
- Define SLIs (Service Level Indicators): latency p99, error rate, availability
- Set SLOs (Service Level Objectives): 99.9% availability, p99 < 500ms
- Calculate error budget: (1 - SLO) × time_window = allowed downtime
- Burn rate alerts: Fast burn (14.4x), Slow burn (6x), Page vs Ticket

### Instrumentation Priority
1. Ingress/Egress boundaries (every external call)
2. Critical business transactions
3. Database queries and cache operations
4. Background jobs and async processing
"""

SECURITY_AUDIT_PROTOCOL = r"""
## 🛡️ Security Audit Protocol (from TerminalSkills)

### OWASP Top 10 (2026)
1. Broken Access Control
2. Cryptographic Failures
3. Injection (SQL, XSS, Command)
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Auth Failures
8. Data Integrity Failures
9. Logging/Monitoring Failures
10. SSRF

### Audit Checklist
- Input validation at ALL boundaries (server-side, not just client)
- Output encoding to prevent XSS
- Parameterized queries / ORM (never string concatenation for SQL)
- Authentication: MFA, secure session management, rate limiting
- Authorization: Principle of least privilege, RBAC, resource-level checks
- Secrets management: No hardcoded credentials, use vault/env injection
- HTTPS everywhere, HSTS headers, CSP headers
- Dependency scanning: npm audit, pip-audit, Snyk, Dependabot
"""

PERFORMANCE_REVIEW = r"""
## 📊 Performance Review Protocol (from TerminalSkills)

### Analysis Method
1. **Measure first**: Profile before optimizing. Use flame graphs, traces, benchmarks
2. **Identify bottleneck**: CPU, memory, I/O, network, or lock contention
3. **Quantify impact**: What percentage of total latency does this bottleneck represent?
4. **Fix the biggest win first**: 80/20 rule — one fix often solves 80% of the problem

### Common Patterns
- **N+1 queries**: Batch or eager-load instead of per-row queries
- **Unnecessary serialization**: Avoid JSON parse/stringify in hot paths
- **Missing indexes**: Add database indexes for frequent query patterns
- **Excessive allocation**: Reuse buffers, pool objects, avoid GC pressure
- **Lock contention**: Use lock-free structures, reduce critical section size

### Verification
- Benchmark before AND after with realistic data volumes
- Measure p50, p95, p99 — not just averages
- Run load tests at 2x expected peak traffic
"""

TEST_GENERATION = r"""
## 🧪 Test Generation Protocol (from TerminalSkills)

### Test Pyramid
- **Unit tests** (70%): Fast, isolated, test one function/class
- **Integration tests** (20%): Test component interactions, real dependencies
- **E2E tests** (10%): Test critical user journeys, full stack

### Generation Strategy
1. Start with happy path — does the core behavior work?
2. Add edge cases — empty input, null, boundary values, unicode
3. Add error cases — invalid input, network failures, timeouts
4. Add property-based tests — generate random inputs, verify invariants

### Quality Criteria
- Tests should be: Deterministic, Independent, Fast (< 100ms per unit test)
- Test behavior, not implementation — tests shouldn't break on refactor
- Each test has: Arrange, Act, Assert pattern
- Name tests descriptively: "should_return_404_when_user_not_found"
"""

DOCUMENTATION = r"""
## 📚 Documentation & ADR Protocol (from TerminalSkills)

### Documentation Types
- **ADR** (Architecture Decision Record): Context → Decision → Consequences
- **API docs**: Auto-generated from code (OpenAPI/Swagger for REST, GraphQL schema)
- **README**: Setup, usage, contributing guide
- **Runbooks**: Step-by-step operational procedures for incidents

### ADR Template
```markdown
# ADR-NNNN: [Title]
## Status: Proposed | Accepted | Deprecated | Superseded
## Context: What is the issue that we're seeing?
## Decision: What have we decided to do?
## Consequences: What are the results of this decision?
```

### Writing Principles
- Document WHY, not WHAT (code shows what, docs show reasoning)
- Keep docs close to code (co-locate in repo)
- Update docs when code changes (tie to PR review)
- Use examples over abstract descriptions
"""

CONTENT_STRATEGY = r"""
## 📝 Content Strategy Framework (from TerminalSkills)

### Content Pillars
Define 3-5 core topics that align with business expertise and audience needs.
Every piece of content maps to at least one pillar.

### Content Calendar
- **Frequency**: Consistency > volume. Weekly > random bursts
- **Mix**: 60% educational, 25% industry commentary, 15% promotional
- **Formats**: Blog posts, videos, infographics, case studies, whitepapers

### SEO-Driven Content
- Research keywords with commercial intent (Ahrefs, SEMrush)
- Map keywords to content funnel: Awareness → Consideration → Decision
- Create "10x content" — 10x better than the top-ranking result
- Update high-performing content quarterly

### Distribution
- Own your platform (blog + email list) before renting (social media)
- Repurpose: 1 long-form → 5 social posts + 1 video + 1 email
- Measure: Traffic, engagement, conversion rate, subscriber growth
"""

GROWTH_HACKING = r"""
## 🚀 Growth Hacking Framework (from TerminalSkills)

### AARRR Pirate Metrics
- **Acquisition**: How do users find you? (SEO, ads, referrals, social)
- **Activation**: Do they have a great first experience? (onboarding, aha moment)
- **Retention**: Do they come back? (engagement loops, notifications, value)
- **Revenue**: How do you monetize? (freemium, subscription, transaction)
- **Referral**: Do they tell others? (invites, share features, affiliate)

### Experiment Process
1. Hypothesize: "If we [change], then [metric] will [improve] because [reason]"
2. Design minimum viable experiment
3. Run for statistically significant duration (calculate sample size)
4. Measure impact on target metric AND guardrail metrics
5. Ship if positive, learn if negative, iterate either way

### Growth Levers
- **Viral coefficient**: Optimize invite flow, reduce friction to share
- **Network effects**: More users = more value (marketplaces, social)
- **Switching costs**: Data lock-in, integrations, workflow investment
"""

SPEC_DRIVEN_DEV = r"""
## 📋 Spec-Driven Development (from TerminalSkills)

### Process
1. **Write spec first**: Define WHAT before HOW. Specs describe behavior, not implementation
2. **Review spec**: Stakeholders validate requirements before code is written
3. **Implement from spec**: Code satisfies spec exactly — no more, no less
4. **Test against spec**: Tests verify spec compliance

### Spec Template
```markdown
# [Feature Name]
## Problem: What user problem does this solve?
## Solution: High-level approach
## Requirements:
  - Functional: What must it do?
  - Non-functional: Performance, security, accessibility
  - Edge cases: What could go wrong?
## API: Endpoints, request/response shapes
## Acceptance Criteria: How do we know it's done?
```

### Anti-Patterns
- Spec too vague: "Make it fast" → "p99 latency < 200ms under 1000 RPS"
- Spec too implementation-specific: "Use Redis" → "Cache with < 100ms read latency"
- No acceptance criteria: Every spec must have testable "done" conditions
"""

TECH_DEBT_ANALYZER = r"""
## 🔬 Tech Debt Analysis Protocol (from TerminalSkills)

### Classification
- **Deliberate debt**: Conscious shortcut with tracked payoff plan
- **Accidental debt**: Emerged from incomplete understanding or changing requirements
- **Bit rot**: Dependencies age, APIs deprecate, patterns become obsolete

### Measurement
- **Complexity**: Cyclomatic complexity, cognitive complexity, nesting depth
- **Coupling**: Incoming/outgoing dependencies, change impact radius
- **Coverage**: Test coverage on critical paths (aim > 80%)
- **Freshness**: Time since last meaningful update, dependency age

### Prioritization (ICE Framework)
- **Impact**: How much does fixing this improve velocity/reliability?
- **Confidence**: How certain are we about the impact estimate?
- **Ease**: How quickly can we fix it? (1 day? 1 sprint? 1 quarter?)

### Payoff Strategy
- Boy Scout Rule: Leave code better than you found it (small, continuous)
- Strangler Fig Pattern: Incrementally replace legacy with new
- Debt sprints: Allocate 20% of sprint capacity to debt reduction
"""

CODE_MIGRATION = r"""
## 🔄 Code Migration Protocol (from TerminalSkills)

### Migration Strategy
1. **Inventory**: List all files/modules that need migration
2. **Assess risk**: Critical path vs. non-critical, test coverage, blast radius
3. **Create compatibility layer**: Shim/wrapper that works with both old and new
4. **Migrate incrementally**: One module at a time, test after each
5. **Remove old code**: Only after full migration is verified

### Patterns
- **Strangler Fig**: New system wraps old, gradually takes over
- **Feature Flags**: Toggle between old and new implementation
- **Parallel Run**: Run both, compare outputs, switch when confident
- **Big Bang**: Only for small, isolated systems with full test coverage

### Verification
- Behavioral parity tests: Same inputs → same outputs (old vs new)
- Performance regression tests: New must not be slower
- Incremental rollout: Canary → 10% → 50% → 100%
"""

AI_SCIENTIST = r"""
## 🧪 AI Research Methodology (from TerminalSkills)

### Experiment Protocol
1. **Hypothesis**: "Model X will improve metric Y by Z% because..."
2. **Baseline**: Measure current performance on held-out test set
3. **Control variables**: Change exactly ONE thing per experiment
4. **Statistical significance**: Use proper sample sizes, report confidence intervals
5. **Reproducibility**: Log all hyperparameters, random seeds, data versions

### Model Development Lifecycle
1. Data collection and cleaning (garbage in, garbage out)
2. Exploratory data analysis (understand distributions, correlations, biases)
3. Feature engineering / representation learning
4. Model selection and training (start simple, add complexity as needed)
5. Evaluation (cross-validation, held-out test, ablation studies)
6. Deployment (A/B test, shadow mode, gradual rollout)
7. Monitoring (data drift, performance degradation, fairness metrics)

### Common Pitfalls
- **Data leakage**: Training data contains information from test set
- **Overfitting**: Model memorizes training data, fails to generalize
- **Selection bias**: Training data not representative of production
- **Metric gaming**: Optimizing for proxy metric instead of true objective
"""

AI_GUARDRAILS = r"""
## 🛡️ AI Guardrails & Safety (from TerminalSkills)

### Input Guardrails
- **Prompt injection detection**: Filter adversarial inputs before processing
- **Content policy enforcement**: Block harmful, illegal, or unethical requests
- **Rate limiting**: Prevent abuse and resource exhaustion
- **Input validation**: Schema validation, length limits, encoding checks

### Output Guardrails
- **Content filtering**: Block harmful, biased, or incorrect outputs
- **PII detection**: Prevent leakage of personal information
- **Hallucination mitigation**: Cross-reference outputs with source data
- **Format enforcement**: Ensure outputs match expected schema

### Monitoring
- Track: Input/output distributions, latency, error rates, user feedback
- Alert on: Distribution shift, increased hallucination rate, policy violations
- Log: All inputs/outputs for audit trail (with PII redaction)
"""

MLFLOW_OPS = r"""
## 📦 MLOps with MLflow (from TerminalSkills)

### Experiment Tracking
- Log parameters, metrics, artifacts for every training run
- Compare runs side-by-side to find best hyperparameters
- Version datasets and models with checksums

### Model Registry
- Stage models: None → Staging → Production → Archived
- Require approval gates before production deployment
- Track model lineage: which data, code, and params produced this model

### Deployment Patterns
- **Batch**: Scheduled inference on large datasets
- **Real-time**: REST API or gRPC endpoint for online inference
- **Edge**: Export to ONNX/TFLite for on-device inference
"""

# ── Persona → Skill Mapping for Gap Filling ──────────────────────────────────

GAP_SKILL_MAP = {
    "SYSTEMS_THINKING": {
        "skill": SYSTEMS_THINKING,
        "marker": "Systems Thinking Framework (from TerminalSkills)",
        "slugs": [
            "business-analyst", "product-manager", "project-manager",
            "marketing-strategist", "growth-experimentation-lead",
            "competitive-analyst", "risk-manager", "financial-analyst",
            "scrum-master", "customer-success-manager",
            "problem-solving-maestro", "core-reasoning-architect",
            "formula-cascade-oracle", "cognitive-multi-thinker",
        ],
    },
    "CONTEXT_ENGINEERING": {
        "skill": CONTEXT_ENGINEERING,
        "marker": "Context Engineering (from TerminalSkills)",
        "slugs": [
            "ai-engineer", "llm-architect", "prompt-engineer",
            "claude-code", "agent-organizer", "multi-agent-coordinator",
            "context-manager", "agentic-swarm-conductor",
            "knowledge-synthesizer", "fractal-elaborator",
        ],
    },
    "PROMPT_ENGINEERING": {
        "skill": PROMPT_ENGINEERING_SOTA,
        "marker": "SOTA Prompt Engineering Techniques (from TerminalSkills)",
        "slugs": [
            "prompt-engineer", "ai-engineer", "llm-architect",
            "nlp-specialist", "rag-evaluator", "ai-prompt-security-specialist",
        ],
    },
    "FRONTEND_DESIGN": {
        "skill": FRONTEND_DESIGN,
        "marker": "Frontend Design Principles (from TerminalSkills)",
        "slugs": [
            "ui-expert", "web-design-specialist", "uiux-vibe-master",
            "react-optimization-director", "frontend-performance-auditor",
            "frontend-architecture-engineer",
        ],
    },
    "WEB_VITALS": {
        "skill": WEB_VITALS,
        "marker": "Web Vitals Analysis Protocol (from TerminalSkills)",
        "slugs": [
            "frontend-performance-auditor", "react-optimization-director",
            "high-perf-engineer", "sota-stack-master",
        ],
    },
    "ACCESSIBILITY": {
        "skill": ACCESSIBILITY_AUDIT,
        "marker": "Accessibility Audit Protocol (from TerminalSkills)",
        "slugs": [
            "accessibility-tester", "ui-expert", "web-design-specialist",
            "uiux-vibe-master", "frontend-developer",
        ],
    },
    "OBSERVABILITY": {
        "skill": OBSERVABILITY_SETUP,
        "marker": "Observability Setup Protocol (from TerminalSkills)",
        "slugs": [
            "devops-observability-sentinel", "sre-engineer",
            "devops-engineer", "performance-monitor",
        ],
    },
    "SECURITY_AUDIT": {
        "skill": SECURITY_AUDIT_PROTOCOL,
        "marker": "Security Audit Protocol (from TerminalSkills)",
        "slugs": [
            "cloud-security-architect", "supply-chain-security-auditor",
            "policy-as-code-auditor", "secrets-hygiene-auditor",
            "compliance-automation-engineer",
        ],
    },
    "PERFORMANCE": {
        "skill": PERFORMANCE_REVIEW,
        "marker": "Performance Review Protocol (from TerminalSkills)",
        "slugs": [
            "performance-monitor", "high-perf-engineer",
            "database-optimizer", "frontend-performance-auditor",
        ],
    },
    "TEST_GENERATION": {
        "skill": TEST_GENERATION,
        "marker": "Test Generation Protocol (from TerminalSkills)",
        "slugs": [
            "test-automator", "qa-expert",
        ],
    },
    "DOCUMENTATION": {
        "skill": DOCUMENTATION,
        "marker": "Documentation & ADR Protocol (from TerminalSkills)",
        "slugs": [
            "documentation-engineer", "technical-writer",
            "api-documenter", "content-strategist",
        ],
    },
    "CONTENT_STRATEGY": {
        "skill": CONTENT_STRATEGY,
        "marker": "Content Strategy Framework (from TerminalSkills)",
        "slugs": [
            "content-marketer", "content-strategist", "creative-director",
            "copywriting", "social-content",
        ],
    },
    "GROWTH_HACKING": {
        "skill": GROWTH_HACKING,
        "marker": "Growth Hacking Framework (from TerminalSkills)",
        "slugs": [
            "growth-experimentation-lead", "marketing-strategist",
            "content-marketer", "product-analytics-scientist",
            "product-manager", "sales-engineer",
        ],
    },
    "SPEC_DRIVEN": {
        "skill": SPEC_DRIVEN_DEV,
        "marker": "Spec-Driven Development (from TerminalSkills)",
        "slugs": [
            "architect", "claude-code", "spec-pseudocode",
            "api-contract-first-developer", "api-designer",
            "graphql-architect",
        ],
    },
    "TECH_DEBT": {
        "skill": TECH_DEBT_ANALYZER,
        "marker": "Tech Debt Analysis Protocol (from TerminalSkills)",
        "slugs": [
            "architect-reviewer", "code-reviewer", "refactoring-specialist",
        ],
    },
    "CODE_MIGRATION": {
        "skill": CODE_MIGRATION,
        "marker": "Code Migration Protocol (from TerminalSkills)",
        "slugs": [
            "legacy-modernizer", "code-migration", "database-migration-engineer",
            "data-pipeline-engineer",
        ],
    },
    "AI_SCIENTIST": {
        "skill": AI_SCIENTIST,
        "marker": "AI Research Methodology (from TerminalSkills)",
        "slugs": [
            "ai-engineer", "machine-learning-engineer", "data-scientist",
            "computer-vision", "mlops-engineer", "dataset-curator",
            "model-registry-auditor", "research-scientist",
        ],
    },
    "AI_GUARDRAILS": {
        "skill": AI_GUARDRAILS,
        "marker": "AI Guardrails & Safety (from TerminalSkills)",
        "slugs": [
            "ai-prompt-security-specialist", "ai-engineer",
            "llm-architect", "rag-evaluator",
        ],
    },
    "MLFLOW": {
        "skill": MLFLOW_OPS,
        "marker": "MLOps with MLflow (from TerminalSkills)",
        "slugs": [
            "mlops-engineer", "machine-learning-engineer",
            "model-registry-auditor",
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

    modified = {}  # path → set of skill names injected

    for skill_name, config in GAP_SKILL_MAP.items():
        skill_text = config["skill"]
        marker = config["marker"]
        slugs = config["slugs"]

        for slug in slugs:
            if slug not in slug_to_path:
                continue

            path = slug_to_path[slug]
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            instructions = data.get("customInstructions", "")

            # Check if already injected
            if marker in instructions:
                continue

            data["customInstructions"] = instructions + skill_text

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

    print(f"\nDone. {len(modified)} files updated with gap-filling skills.")


if __name__ == "__main__":
    main()
