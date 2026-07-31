#!/usr/bin/env python3
"""
Fix mode descriptions: replace clone-of-roleDefinition descriptions with
genuinely user-friendly, action-oriented descriptions.

Transformation rules:
- roleDefinition = internal AI prompt (what the AI is)
- description = user-facing summary (what the mode does for you)

Usage:
    python3 scripts/fix_descriptions.py                    # Fix all three sets
    python3 scripts/fix_descriptions.py --dir agents       # Fix only agents/
    python3 scripts/fix_descriptions.py --dir custom_modes.d  # Fix only custom_modes.d/
    python3 scripts/fix_descriptions.py --dir vs-code/converted_modes.d  # Fix only vs-code/
"""

import yaml
import re
import glob
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


# Mapping of slug -> user-friendly description
# Keyed by slug so the same description applies consistently across all three file sets
USER_FRIENDLY_DESCRIPTIONS = {
    # === Core Development ===
    "architect": "Designs scalable, modular system architectures with clear component boundaries and integration patterns.",
    "architect-reviewer": "Reviews system architectures for scalability, security, and adherence to design patterns.",
    "backend-developer": "Builds secure, scalable server-side applications, APIs, and microservices with robust data handling.",
    "frontend-developer": "Crafts performant, accessible, and maintainable user interfaces using modern frontend frameworks.",
    "fullstack-developer": "Develops end-to-end features across the entire stack — from database to user interface.",
    "api-designer": "Creates well-structured REST and GraphQL APIs with comprehensive documentation and great developer experience.",
    "microservices-architect": "Designs and coordinates distributed microservice ecosystems with service boundaries and inter-service communication.",
    "mobile-developer": "Builds cross-platform mobile applications with native performance and platform-optimized experiences.",
    "sdk-developer": "Designs developer-friendly SDKs with ergonomic APIs, strong typing, and clear documentation.",
    "ui-expert": "Creates intuitive, visually appealing user interfaces following design system principles and accessibility standards.",
    "web-design-specialist": "Designs and builds modern websites with responsive layouts, accessibility, and performance optimization.",
    "algorithmic-problem-solver": "Designs and implements optimal algorithms with rigorous correctness and complexity analysis.",
    "compiler-engineer": "Designs compiler toolchains including lexing, parsing, IR design, optimization passes, and code generation.",
    "functional-programming-expert": "Designs purely functional, composable systems with strong type systems and algebraic reasoning.",
    "performance-engineer": "Identifies bottlenecks and optimizes system performance across application, database, and infrastructure layers.",
    "blockchain-developer": "Develops Web3 applications including smart contracts, DeFi protocols, and cross-chain solutions.",
    "deep-research-protocol": "Conducts systematic, multi-source research and produces publication-ready analytical reports.",
    "integration": "Merges outputs from multiple development modes into a working, tested, production-ready system.",
    "mcp": "Connects to and manages external services through MCP (Management Control Panel) interfaces.",
    "post-deployment-monitoring-mode": "Monitors system health, performance, and errors after deployment to detect and report issues.",
    "refinement-optimization-mode": "Refactors, modularizes, and optimizes existing code for better performance and maintainability.",
    "ask": "Guides users in navigating, scoping, and delegating tasks to the appropriate specialized modes.",
    "code": "Writes clean, modular, production-ready code following architecture specifications and best practices.",
    "silent-coder": "Executes coding tasks autonomously with minimal interaction, following pre-defined specifications.",
    "spec-pseudocode": "Translates high-level requirements into detailed pseudocode and implementation specifications.",
    "sparc": "Guides users through the SPARC methodology: Specification, Implementation, Architecture, Refinement, Completion.",
    "website-foundation-planner": "Creates comprehensive planning dossiers, folder structures, and best-practice blueprints for new websites.",
    "content-strategist": "Develops content strategies, editorial calendars, and content architectures aligned with business goals.",
    "tutorial": "Creates educational content and tutorials to onboard users and teach development workflows.",
    "frontend-architecture-engineer": "Designs scalable frontend architectures including state management, routing, component boundaries, and build pipelines.",
    "frontend-performance-auditor": "Audits frontend applications for performance bottlenecks, Core Web Vitals, and optimization opportunities.",
    "react-optimization-director": "Analyzes and optimizes React applications for rendering performance, bundle size, and用户体验.",
    "electron-pro": "Builds cross-platform desktop applications using Electron with native-feeling experiences.",
    "cli-tool-developer": "Designs and builds command-line interfaces with intuitive argument parsing, output formatting, and error handling.",
    "bff-engineer": "Designs Backend-for-Frontend (BFF) API layers optimized for specific client application needs.",
    "concurrency-specialist": "Designs and implements concurrent and parallel systems with thread-safe, deadlock-free execution.",
    "database-migration-engineer": "Plans and executes safe database schema migrations with rollback strategies and zero-downtime deployment.",
    "data-pipeline-engineer": "Builds data processing pipelines for ETL/ELT workflows, stream processing, and batch analytics.",
    "streaming-systems-engineer": "Designs real-time data streaming systems using Kafka, Flink, or similar technologies.",
    "wasm-systems-developer": "Develops WebAssembly modules for high-performance browser and server-side applications.",
    "realtime-collaboration-engineer": "Builds real-time collaborative features including WebSockets, CRDTs, and operational transforms.",
    "embedded-firmware-developer": "Develops embedded firmware and IoT device software with resource-constrained optimization.",
    "game-engine-developer": "Builds game engines and game development tools with rendering, physics, and asset pipelines.",
    "api-contract-first-developer": "Designs APIs using a contract-first approach with OpenAPI specs and automated validation.",
    "graphql-resolver-writer": "Implements efficient GraphQL resolvers with data loading optimization and schema stitching.",
    "product-owner": "Manages product backlogs, prioritizes features, and bridges business requirements with technical implementation.",
    
    # === Language Specialists ===
    "typescript-pro": "Writes type-safe TypeScript code with advanced type system features and strict mode compliance.",
    "python-developer": "Builds Python applications using modern frameworks like FastAPI, Django, and async patterns.",
    "python-pro": "Writes production-grade Python with performance optimization, type hints, and testing best practices.",
    "rust-developer": "Develops safe, high-performance Rust applications leveraging ownership, borrowing, and zero-cost abstractions.",
    "golang-developer": "Builds concurrent, performant Go services with strong typing and idiomatic Go patterns.",
    "java-developer": "Develops enterprise Java applications with Spring Boot, microservices, and JVM optimization.",
    "java-architect": "Designs Java enterprise architectures with Spring ecosystem, microservices decomposition, and JVM tuning.",
    "kotlin-specialist": "Builds Kotlin applications for Android, backend, and multiplatform projects with coroutines and flows.",
    "swift-expert": "Develops Swift applications for Apple platforms with modern SwiftUI, concurrency, and performance patterns.",
    "csharp-developer": "Builds .NET applications with C# following modern language features and framework best practices.",
    "dotnet-core-expert": "Develops cross-platform .NET Core applications with ASP.NET, Entity Framework, and cloud-native patterns.",
    "cpp-pro": "Writes high-performance C++ code with modern standards, template metaprogramming, and zero-overhead abstractions.",
    "flutter-expert": "Builds cross-platform Flutter applications with Dart, widget-based UIs, and native platform integrations.",
    "react-specialist": "Develops React applications with hooks, context, Suspense, and modern rendering patterns.",
    "vue-expert": "Builds Vue.js applications with Composition API, Pinia state management, and component architecture.",
    "angular-architect": "Develops Angular applications with RxJS, NgRx, modular architecture, and enterprise patterns.",
    "nextjs-developer": "Builds Next.js applications with SSR, ISR, App Router, and full-stack React capabilities.",
    "rails-expert": "Develops Ruby on Rails applications following convention-over-configuration and MVC patterns.",
    "django-developer": "Builds Django web applications with ORM, admin interface, REST framework, and async views.",
    "spring-boot-engineer": "Develops Spring Boot microservices with auto-configuration, Actuator, and cloud-native patterns.",
    "laravel-specialist": "Builds Laravel PHP applications with Eloquent ORM, artisan CLI, and modern PHP patterns.",
    "php-pro": "Writes modern PHP with strict types, PSR standards, and framework-agnostic clean architecture.",
    "sql-pro": "Optimizes complex database queries, designs schemas, and tunes performance across major SQL databases.",
    "javascript-pro": "Writes modern JavaScript with ES2024+ features, async patterns, and cross-platform compatibility.",
    "javascript-developer": "Builds JavaScript applications with modern tooling, Node.js, and frontend/backend integration.",
    
    # === AI & ML ===
    "ai-engineer": "Designs and implements AI systems including model selection, agentic workflows, and production deployment.",
    "machine-learning-engineer": "Deploys and serves ML models in production with scalable inference pipelines and monitoring.",
    "llm-architect": "Architects large language model systems including deployment, fine-tuning, RAG, and prompt optimization.",
    "prompt-engineer": "Designs and optimizes prompts for large language models to achieve reliable, high-quality outputs.",
    "rag-evaluator": "Builds evaluation suites for RAG/LLM systems measuring retrieval quality, faithfulness, and hallucination rates.",
    "nlp-specialist": "Applies natural language processing techniques including transformers, embeddings, and text analytics.",
    "data-scientist": "Analyzes data, builds predictive models, and extracts actionable insights using statistical methods and ML.",
    "dataset-curator": "Creates, validates, and maintains high-quality datasets for ML training with balance and coverage checks.",
    "computer-vision": "Develops computer vision solutions using deep learning for image and video analysis.",
    "mlops-engineer": "Operationalizes ML pipelines with CI/CD for models, feature stores, experiment tracking, and monitoring.",
    "model-registry-auditor": "Audits ML model registries for versioning, lineage, governance, and compliance with ML lifecycle policies.",
    
    # === DevOps & Infrastructure ===
    "devops-architect": "Designs cloud-native CI/CD pipelines, container orchestration, and infrastructure automation.",
    "devops-engineer": "Implements CI/CD pipelines, containerization, monitoring, and infrastructure-as-code solutions.",
    "deployment-engineer": "Automates release processes, manages deployment strategies, and ensures reliable rollouts.",
    "cloud-architect": "Designs multi-cloud architectures with cost optimization, scalability, and security best practices.",
    "network-engineer": "Designs and manages cloud and hybrid network architectures with security and performance optimization.",
    "kubernetes-specialist": "Orchestrates containerized workloads on Kubernetes with service mesh, scaling, and operational excellence.",
    "terraform-engineer": "Manages infrastructure as code using Terraform with modular, reusable, and state-managed configurations.",
    "terraform-module-author": "Creates reusable, versioned Terraform modules following composition patterns and best practices.",
    "platform-engineer": "Builds internal developer platforms with self-service infrastructure, golden paths, and paved roads.",
    "serverless-platform-architect": "Designs serverless architectures with function compute, event-driven patterns, and managed services.",
    "site-readiness-engineer": "Ensures production readiness through load testing, chaos engineering, and reliability validation.",
    "observability-architect": "Designs monitoring, logging, and tracing systems with SLI/SLO definition and actionable alerting.",
    "finops-optimizer": "Analyzes and optimizes cloud spending through rightsizing, commitments, and cost-aware architecture decisions.",
    "chaos-engineer": "Proactively tests system resilience through controlled failure injection and chaos experiments.",
    "chaos-resilience-lead": "Leads chaos engineering programs to build fault-tolerant, self-healing distributed systems.",
    "incident-responder": "Responds to production incidents with systematic triage, mitigation, and post-mortem analysis.",
    "hardware-acceleration-engineer": "Optimizes workloads using GPUs, FPGAs, and specialized hardware accelerators.",
    
    # === Security ===
    "cybersecurity-expert": "Identifies and mitigates security vulnerabilities across applications, networks, and infrastructure.",
    "penetration-tester": "Conducts ethical penetration testing to identify security weaknesses and validate defenses.",
    "security-auditor": "Performs comprehensive security assessments, compliance validation, and risk management reviews.",
    "security-engineer": "Implements security controls, threat modeling, and secure architecture patterns.",
    "zero-trust-strategist": "Designs zero-trust security architectures with adaptive access controls and continuous verification.",
    "cloud-security-architect": "Designs secure cloud architectures with identity management, encryption, and compliance controls.",
    "secrets-hygiene-auditor": "Scans repositories for hardcoded secrets, migrates to secret stores, and enforces rotation policies.",
    "code-reviewer": "Reviews code for quality, security vulnerabilities, and adherence to best practices.",
    "code-skeptic": "Critically examines code for assumptions, edge cases, and potential issues with a questioning mindset.",
    "security-review": "Conducts security-focused code reviews identifying vulnerabilities and recommending fixes.",
    "compliance-specialist": "Ensures regulatory compliance across GDPR, HIPAA, SOX, and other frameworks with cross-jurisdiction expertise.",
    "compliance-specialist-canada": "Ensures regulatory compliance with Canadian standards and privacy legislation.",
    "compliance-specialist-usa": "Ensures regulatory compliance with US federal and state regulations.",
    "compliance-auditor-canada": "Audits systems and processes for compliance with Canadian regulatory requirements.",
    "compliance-auditor-usa": "Audits systems and processes for compliance with US regulatory requirements.",
    "compliance-automation-engineer": "Automates compliance enforcement through policy-as-code and continuous compliance monitoring.",
    "oss-license-auditor": "Validates third-party dependencies, generates SBOMs, and ensures open source license compliance.",
    "ai-prompt-security-specialist": "Secures AI systems against prompt injection, data leakage, and other LLM-specific threats.",
    
    # === Quality & Testing ===
    "tdd": "Implements Test-Driven Development with tests written first, followed by minimal implementation and refactoring.",
    "qa-expert": "Designs comprehensive test strategies and ensures quality across unit, integration, and E2E testing.",
    "test-automator": "Builds automated test frameworks with CI/CD integration for reliable, repeatable testing.",
    "accessibility-tester": "Audits digital products for WCAG compliance, screen reader compatibility, and inclusive design.",
    "error-detective": "Investigates and diagnoses errors across logs, traces, and metrics to identify root causes.",
    "debugger": "Systematically troubleshoots code issues using breakpoints, logging, and root-cause analysis.",
    "refactoring-specialist": "Safely restructures and improves existing code without changing external behavior.",
    "bullshit-detection-analyst": "Critically evaluates claims and information sources for credibility, accuracy, and logical consistency.",
    "framework-currency": "Audits project dependencies and updates them to latest stable versions with migration guidance.",
    "dx-optimizer": "Improves developer experience through tooling, automation, and streamlined development workflows.",
    "legacy-modernizer": "Modernizes legacy codebases by incrementally upgrading architecture, dependencies, and practices.",
    
    # === Business & Product ===
    "product-manager": "Defines product strategy, prioritizes features, and bridges user needs with business goals.",
    "business-analyst": "Gathers requirements, analyzes processes, and recommends data-driven business improvements.",
    "project-manager": "Orchestrates project timelines, resources, and deliverables to ensure on-time, on-scope completion.",
    "scrum-master": "Facilitates Agile ceremonies, removes impediments, and coaches teams on Scrum practices.",
    "sales-engineer": "Provides technical pre-sales support, designs solution architectures, and builds proof-of-concepts.",
    "customer-success-manager": "Drives customer retention, adoption, and growth through proactive engagement and success planning.",
    "marketing-strategist": "Develops data-driven marketing strategies across digital channels, brand development, and campaign optimization.",
    "growth-experimentation-lead": "Designs and manages experimentation programs with A/B testing and metric-driven optimization.",
    "content-marketer": "Creates and distributes valuable content to attract, engage, and convert target audiences.",
    "technical-writer": "Produces clear, accurate technical documentation, guides, and reference materials.",
    "ux-researcher": "Conducts user research, usability testing, and data analysis to inform product design decisions.",
    "i18n-l10n-reviewer": "Validates internationalization and localization quality including ICU messages, RTL support, and cultural adaptation.",
    "product-analytics-scientist": "Analyzes product usage data to uncover insights, measure feature adoption, and drive product decisions.",
    "creative-director": "Leads brand identity, visual design, and creative strategy across digital and traditional media.",
    "financial-analyst": "Builds financial models, conducts investment analysis, and provides strategic financial planning.",
    "market-researcher": "Conducts market analysis, consumer research, and competitive intelligence to inform strategy.",
    "competitive-analyst": "Analyzes competitor strategies, market positioning, and industry trends to identify opportunities.",
    "research-analyst": "Gathers and synthesizes information from multiple sources to produce actionable research findings.",
    "data-analyst": "Transforms raw data into actionable business insights through analysis, visualization, and reporting.",
    "data-engineer": "Builds scalable data pipelines, ETL/ELT processes, and data infrastructure for analytics and ML.",
    "database-administrator": "Manages database systems for high availability, performance, backup/recovery, and security.",
    "database-optimizer": "Tunes database queries, indexes, and schemas for maximum performance and scalability.",
    "dependency-manager": "Manages package dependencies, audits for security vulnerabilities, and resolves version conflicts.",
    "digital-marketing-specialist": "Executes multi-channel digital marketing campaigns with measurement and optimization.",
    "performance-copywriter": "Creates persuasive, conversion-optimized copy for marketing, advertising, and brand communications.",
    "seo-strategist": "Develops comprehensive SEO strategies including keyword research, on-page optimization, and link building.",
    "technical-seo-optimizer": "Optimizes technical SEO factors including crawlability, indexation, structured data, and site architecture.",
    "core-web-vitals-seo": "Optimizes Core Web Vitals metrics including LCP, FID/INP, and CLS for search ranking improvement.",
    "local-seo-specialist": "Optimizes local search presence including Google Business Profile, local citations, and review management.",
    "ecommerce-seo-specialist": "Optimizes ecommerce sites for search including product pages, category structure, and technical SEO.",
    "ai-content-seo": "Creates and optimizes AI-generated content for search engines while maintaining quality and relevance.",
    "instagram-content-creator": "Creates engaging Instagram content with visual storytelling, caption psychology, and platform trends.",
    "ai-art-director": "Directs AI-powered visual art creation across photography, illustration, game art, and design disciplines.",
    "investigative-reporter": "Thoroughly researches topics, uncovers connections, and produces comprehensive investigative reports.",
    "excel-power-user": "Creates advanced Excel spreadsheets with formulas, pivot tables, macros, and data visualization.",
    "powerpoint-presenter": "Designs professional PowerPoint presentations with compelling visuals and clear narrative structure.",
    
    # === Legal ===
    "corporate-law": "Provides legal guidance on corporate governance, mergers & acquisitions, and business transactions.",
    "corporate-law-usa": "Provides legal guidance on US corporate law including governance, M&A, and securities compliance.",
    "corporate-law-canada": "Provides legal guidance on Canadian corporate law including governance, M&A, and securities compliance.",
    "criminal-law": "Provides legal analysis and guidance on criminal law matters.",
    "criminal-law-usa": "Provides legal analysis on US criminal law including federal and state jurisdiction matters.",
    "criminal-law-canada": "Provides legal analysis on Canadian criminal law including Criminal Code and provincial matters.",
    "employment-law": "Provides legal guidance on employment law including hiring, termination, discrimination, and workplace policies.",
    "employment-law-usa": "Provides legal guidance on US employment law including federal and state labor regulations.",
    "employment-law-canada": "Provides legal guidance on Canadian employment law including provincial and federal standards.",
    "intellectual-property": "Provides legal guidance on patents, trademarks, copyrights, and trade secret protection.",
    "intellectual-property-usa": "Provides legal guidance on US intellectual property law including USPTO procedures and enforcement.",
    "litigation-support": "Provides litigation support including case analysis, document review, and legal research.",
    "litigation-support-usa": "Provides litigation support for US legal proceedings including federal and state court procedures.",
    "litigation-support-canada": "Provides litigation support for Canadian legal proceedings including court procedures and rules.",
    "legal-advisor": "Provides comprehensive legal advice across multiple practice areas and jurisdictions.",
    "legal-advisor-usa": "Provides legal advice on US law across multiple practice areas and federal/state jurisdictions.",
    "legal-advisor-canada": "Provides legal advice on Canadian law across multiple practice areas and provincial/federal jurisdictions.",
    
    # === Meta-Orchestration ===
    "workflow-orchestrator": "Designs and coordinates complex multi-step workflows and business process automation.",
    "multi-agent-coordinator": "Manages inter-agent communication, task delegation, and distributed coordination across agents.",
    "task-distributor": "Intelligently allocates work across available resources with load balancing and queue management.",
    "agent-organizer": "Organizes multi-agent teams, assigns roles, and orchestrates collaborative problem-solving.",
    "knowledge-synthesizer": "Extracts insights, identifies patterns, and builds collective intelligence from multi-source information.",
    "build-engineer": "Optimizes build systems, compilation strategies, and developer productivity toolchains.",
    "git-workflow-manager": "Manages Git branching strategies, automation hooks, and team Git workflows.",
    "release-governance-lead": "Orchestrates release readiness reviews, coordinates stakeholders, and enforces release policies.",
    "feature-flag-orchestrator": "Manages feature flag lifecycles including safe rollouts, kill-switches, and flag cleanup.",
    "error-coordinator": "Coordinates error handling across distributed systems with failure recovery and resilience patterns.",
    "performance-monitor": "Tracks and analyzes system performance metrics to identify regressions and optimization opportunities.",
    "performance-benchmark": "Designs and runs performance benchmarks to measure and compare system behavior under load.",
    "context-manager": "Manages and provides relevant context across agent interactions for coherent multi-step workflows.",
    "tooling-engineer": "Builds and maintains developer tooling, automation scripts, and productivity enhancements.",
    "cli-developer": "Designs and implements command-line tools with intuitive interfaces and robust error handling.",
    "documentation-engineer": "Creates comprehensive technical documentation systems with API docs, tutorials, and automated generation.",
    "api-governance-lead": "Enforces API design standards, consistency rules, and governance policies across the organization.",
    "dx-optimizer": "Improves developer workflows through streamlined tooling, automation, and friction reduction.",
    "search-specialist": "Implements and optimizes search functionality including full-text search, faceted search, and ranking.",
    "research-scientist": "Conducts scientific research, literature reviews, and experimental design for technical investigations.",
    "tech-research-strategist": "Evaluates emerging technologies and provides strategic recommendations for technology adoption.",
    "trend-analyst": "Identifies and analyzes technology and market trends to inform product and strategy decisions.",
    "data-researcher": "Gathers, validates, and analyzes data from multiple sources to support research and decision-making.",
    "website-foundation-planner": "Creates comprehensive website planning dossiers with folder structures and best-practice alignment.",
    
    # === Fintech & Payments ===
    "fintech-engineer": "Builds financial systems with regulatory compliance, secure transaction processing, and audit trails.",
    "payment-integration": "Integrates payment gateways with PCI compliance, transaction routing, and error handling.",
    "risk-manager": "Assesses and mitigates risks across operations, security, compliance, and business continuity.",
    
    # === IoT ===
    "iot-engineer": "Develops connected device solutions with edge computing, sensor integration, and IoT platform architecture.",
    
    # === SOTA Personas ===
    "core-reasoning-architect": "Provides foundational reasoning architecture and structured thinking for complex problem-solving.",
    "formula-cascade-oracle": "Applies Fractal Formula Notation for systematic, multi-layered analytical reasoning.",
    "fractal-elaborator": "Performs deep recursive analysis with infinite zoom into architectural and conceptual details.",
    "high-perf-engineer": "Delivers high-performance engineering solutions with optimization at every layer of the stack.",
    "sota-stack-master": "Applies state-of-the-art engineering practices across the full development stack.",
    "uiux-vibe-master": "Ensures pixel-perfect, accessible, and aesthetically cohesive user interfaces.",
    "anti-fiction-sentinel": "Verifies claims and assertions against evidence, ensuring factual accuracy and logical consistency.",
    "devops-observability-sentinel": "Monitors system observability and ensures comprehensive telemetry coverage.",
    "problem-solving-maestro": "Applies systematic problem-solving heuristics and multi-perspective analysis.",
    "cognitive-multi-thinker": "Simulates multiple reasoning perspectives for comprehensive problem analysis.",
    "agentic-swarm-conductor": "Orchestrates multi-agent swarms with hive-mind coordination and stuck-state recovery.",
    
    # === Specialized ===
    "product-analytics-scientist": "Analyzes product usage metrics, user behavior, and feature adoption to guide product strategy.",
    "game-developer": "Builds games across platforms with graphics, physics, audio, and engaging gameplay mechanics.",
    "supabase-admin": "Manages Supabase projects including database, authentication, storage, and real-time subscriptions.",
    "websocket-engineer": "Implements real-time WebSocket communication with connection management, scaling, and fallback strategies.",
    "powershell-assistant": "Automates Windows tasks using PowerShell scripts, modules, and system administration.",
    "powershell-autopilot": "Autonomously executes PowerShell-based system administration and automation tasks.",
    "electron-pro": "Builds cross-platform desktop applications with native features and optimized performance.",
    "flutter-expert": "Develops cross-platform mobile and desktop apps with Flutter and Dart.",
    "mobile-developer": "Builds performant cross-platform mobile applications with native platform features.",
    "graphql-architect": "Designs efficient, scalable GraphQL schemas with federation, data loading optimization, and resolver patterns.",
    "claude-code": "An elite software engineer specializing in systematic code optimization and full-stack development.",
    "edge-computing-architect": "Designs geo-distributed, low-latency edge computing architectures for real-time applications.",
    "postgres-pro": "Administers and optimizes PostgreSQL databases with performance tuning, replication, and high availability.",
    "incident-command-director": "Coordinates major incident response with structured command, communication, and resolution tracking.",
    "sre-engineer": "Balances feature velocity with system reliability through SLOs, error budgets, and automation.",
    "systems-expert": "Specializes in high-performance computing, kernel development, and systems-level optimization.",
    "intellectual-property-canada": "Provides legal guidance on Canadian IP law including CIPO procedures, patents, and trademarks.",
    "experience-polish-director": "Leads multidisciplinary QA for web experiences, ensuring pixel-perfect, polished user interactions.",
    "policy-as-code-auditor": "Enforces compliance policies using OPA/Rego with automated drift detection and enforcement.",
    "supply-chain-security-auditor": "Safeguards build systems and software supply chains against compromise and dependency attacks.",
    "api-documenter": "Creates comprehensive, developer-friendly API documentation with examples, specifications, and guides.",
    "embedded-systems": "Programs microcontrollers, RTOS, and embedded firmware with resource-constrained optimization.",
    "quant-analyst": "Builds quantitative financial models, algorithmic trading strategies, and risk analytics.",
}


def generate_description(slug: str, name: str, role_def: str) -> str:
    """Generate a user-friendly description from the slug and roleDefinition."""
    # First check if we have a hand-crafted description for this slug
    if slug in USER_FRIENDLY_DESCRIPTIONS:
        return USER_FRIENDLY_DESCRIPTIONS[slug]
    
    # Fallback: intelligent extraction from roleDefinition
    if not role_def:
        return ""
    
    role_clean = role_def.strip()
    
    # Strip "You are an|a|the X" prefix
    prefixes = [
        r"^You are an?\s+(?:advanced\s+)?(?:Expert\s+)?",
        r"^You are an?\s+(?:elite\s+)?",
        r"^You are an?\s+(?:Senior\s+)?",
        r"^You are an?\s+(?:expert\s+)?",
        r"^You are the\s+",
        r"^You are a\s+",
        r"^You are an\s+",
        r"^You are\s+",
    ]
    
    core = role_clean
    for p in prefixes:
        if re.match(p, core, re.IGNORECASE):
            core = re.sub(p, "", core, flags=re.IGNORECASE)
            break
    
    first_sent = core.split('.')[0].strip()
    
    # Extract role title from name if available
    name_clean = name.strip()
    # Remove emoji prefix from name
    name_no_emoji = re.sub(r'^[^\w\s]{1,3}\s+', '', name_clean)
    
    # Check if the name gives us a good title
    if name_no_emoji and len(name_no_emoji) < 60:
        return f"{name_no_emoji} — {first_sent[:1].lower() + first_sent[1:] if first_sent else ''}."
    
    return f"{first_sent}."


def is_clone(description: str, role_definition: str) -> bool:
    """Check if description is a clone of roleDefinition."""
    if not description or not role_definition:
        return True
    
    desc_clean = description.strip().rstrip('.')
    role_clean = role_definition.strip()
    
    # Direct substring match
    if desc_clean in role_clean:
        return True
    
    # First sentence match
    first_sent = role_clean.split('.')[0].strip().rstrip('.')
    if desc_clean == first_sent:
        return True
    
    # Description matches stripped role
    stripped_role = re.sub(
        r"^You are (?:an?|the)\s+(?:Expert\s+)?(?:elite\s+)?(?:Senior\s+)?(?:expert\s+)?",
        "",
        first_sent,
        flags=re.IGNORECASE
    ).strip()
    if desc_clean == stripped_role:
        return True
    
    # roleDef starts with description
    if len(desc_clean) > 20 and role_clean.startswith(desc_clean):
        return True
    
    # Check if description is just the name
    if desc_clean == re.sub(r'^[^\w\s]{1,3}\s+', '', (role_definition.split('.')[0] if '.' in role_definition else role_definition)).strip():
        return True
    
    return False


def process_file(filepath: Path, format_type: str) -> bool:
    """Process a single YAML file and update its description."""
    with open(filepath) as f:
        content = f.read()
    
    data = yaml.safe_load(content)
    if not data:
        return False
    
    modified = False
    
    if format_type == 'flat':
        # agents/ format: flat dict
        if 'description' in data and 'roleDefinition' in data:
            old_desc = data.get('description', '')
            role_def = data.get('roleDefinition', '')
            slug = data.get('slug', '')
            name = data.get('name', '')
            
            should_replace = False
            new_desc = None
            
            # Always use hand-crafted description if available
            if slug in USER_FRIENDLY_DESCRIPTIONS:
                new_desc = USER_FRIENDLY_DESCRIPTIONS[slug]
                should_replace = True
            elif is_clone(old_desc, role_def):
                new_desc = generate_description(slug, name, role_def)
                should_replace = True
            
            if should_replace and new_desc and new_desc != old_desc:
                data['description'] = new_desc
                modified = True
    
    elif format_type == 'nested':
        # custom_modes.d/ and vs-code/ format
        if 'customModes' in data and isinstance(data['customModes'], list):
            for mode in data['customModes']:
                if 'description' in mode and 'roleDefinition' in mode:
                    old_desc = mode.get('description', '')
                    role_def = mode.get('roleDefinition', '')
                    slug = mode.get('slug', '')
                    name = mode.get('name', '')
                    
                    should_replace = False
                    new_desc = None
                    
                    # Always use hand-crafted description if available
                    if slug in USER_FRIENDLY_DESCRIPTIONS:
                        new_desc = USER_FRIENDLY_DESCRIPTIONS[slug]
                        should_replace = True
                    elif is_clone(old_desc, role_def):
                        new_desc = generate_description(slug, name, role_def)
                        should_replace = True
                    
                    if should_replace and new_desc and new_desc != old_desc:
                        mode['description'] = new_desc
                        modified = True
                        # Also fix whenToUse if it's stale (contains roleDefinition content)
                        if 'whenToUse' in mode:
                            old_when = mode.get('whenToUse', '')
                            # Check if whenToUse is just a rephrased version of roleDefinition
                            role_core = role_def.split('.')[0].strip().rstrip('.')
                            if role_core.lower() in old_when.lower() or old_when.lower() in role_def.lower():
                                mode['whenToUse'] = f"Activate this mode when you need a: {new_desc}"
    
    if modified:
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                     sort_keys=False, width=120, indent=2)
        return True
    
    return False


def process_directory(base_dir: Path, format_type: str) -> tuple:
    """Process all YAML files in a directory."""
    total = 0
    modified = 0
    errors = 0
    
    yaml_files = list(base_dir.rglob("*.yaml"))
    print(f"\n{'='*60}")
    print(f"Processing {len(yaml_files)} files in {base_dir.relative_to(REPO_ROOT.parent)}")
    print(f"{'='*60}")
    
    # Track which slugs were NOT in the user-friendly dict
    missing_slugs = set()
    
    for fpath in sorted(yaml_files):
        rel_path = fpath.relative_to(REPO_ROOT)
        try:
            # Quick read to check slug
            with open(fpath) as f:
                raw_data = yaml.safe_load(f)
            
            if format_type == 'flat':
                slug = raw_data.get('slug', '') if raw_data else ''
            else:
                slug = raw_data.get('customModes', [{}])[0].get('slug', '') if raw_data and raw_data.get('customModes') else ''
            
            if slug and slug not in USER_FRIENDLY_DESCRIPTIONS:
                missing_slugs.add(slug)
            
            result = process_file(fpath, format_type)
            total += 1
            if result:
                modified += 1
                print(f"  ✓ {rel_path}")
        except Exception as e:
            errors += 1
            print(f"  ✗ Error: {rel_path}: {e}")
    
    if missing_slugs:
        print(f"\n⚠️  {len(missing_slugs)} slugs missing from USER_FRIENDLY_DESCRIPTIONS:")
        for s in sorted(missing_slugs):
            print(f"    - {s}")
    
    return total, modified, errors


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fix mode descriptions")
    parser.add_argument("--dir", choices=['agents', 'custom_modes.d', 'vs-code/converted_modes.d', 'all'],
                       default='all', help="Which directory to process")
    args = parser.parse_args()
    
    dirs_to_process = []
    if args.dir == 'all' or args.dir == 'agents':
        dirs_to_process.append((REPO_ROOT / "agents", "flat"))
    if args.dir == 'all' or args.dir == 'custom_modes.d':
        dirs_to_process.append((REPO_ROOT / "custom_modes.d", "nested"))
    if args.dir == 'all' or args.dir == 'vs-code/converted_modes.d':
        dirs_to_process.append((REPO_ROOT / "vs-code" / "converted_modes.d", "nested"))
    
    grand_total = 0
    grand_modified = 0
    grand_errors = 0
    
    for base_dir, fmt in dirs_to_process:
        if base_dir.exists():
            t, m, e = process_directory(base_dir, fmt)
            grand_total += t
            grand_modified += m
            grand_errors += e
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {grand_total} files processed, {grand_modified} modified, {grand_errors} errors")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
