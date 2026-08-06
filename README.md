<div align="center">

![Custom Modes for Roo Code Banner](./assets/banner.png)

</div>

# Custom Modes for Roo Code 🤖

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-2026.1-blue)](https://github.com/jtgsystems/Custom-Modes-Roo-Code)
[![Agents](https://img.shields.io/badge/Agents-290-green)](https://github.com/jtgsystems/Custom-Modes-Roo-Code)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen)](https://github.com/jtgsystems/Custom-Modes-Roo-Code)
[![Security](https://img.shields.io/badge/Security-2026%20Standards-red)](https://github.com/jtgsystems/Custom-Modes-Roo-Code)

### ⭐ **[Star this repo](https://github.com/jtgsystems/Custom-Modes-Roo-Code/stargazers)** if you find it useful! ⭐

</div>

> **Professional AI Agent Configuration Library for Roo Code — 2026 Edition**
>
> A comprehensive collection of 290 specialized AI modes designed for modern software development, following 2026 security-first principles and best practices.

## 📦 Roo+ Canonical Model

This submodule is consumed by **Roo+** as its single source of custom modes.

**One canonical catalog:** all modes live in [`custom_modes.d/`](custom_modes.d/), organized as `<category>/<slug>.yaml` — **290 modes** total. Each file wraps a `customModes:` array.

**Two user-facing lists:**

| List | Artifact (parent repo) | Contents |
|------|------------------------|----------|
| **Preloaded** | `.roomodes` / `src/assets/marketplace/pre-installed-modes.yml` | **89 curated modes**, selected via `custom-modes/manifest.json` |
| **Marketplace** | `src/assets/marketplace/modes.yml` | **301 items** — the full 290-mode catalog + **11 preserved originals** |

**Built-in slug exclusion:** the Roo+ core modes `architect`, `code`, `ask`, `debug`, and `orchestrator` are excluded from every list — they are provided by the extension core and are never shipped from this catalog.

**Legacy artifacts removed:** the old `agents/` catalog, `vs-code/` conversion tooling, the monolithic `custom_modes.yaml`, the split `.roomodes.00–10` files, and `passing_slugs.txt` have been removed. [`custom_modes.d/`](custom_modes.d/) is the single source of truth.

### Adding a Mode

To add or change a mode:

1. Edit (or create) the mode file at `custom_modes.d/<category>/<slug>.yaml`, keeping the `customModes:` wrapper shape.
2. From the Roo+ repo root, regenerate the user-facing artifacts:
   ```bash
   node scripts/sync-custom-modes.mjs    # .roomodes, pre-installed-modes.yml, modes.yml
   node scripts/generate-catalog.mjs     # custom-modes/AGENT_CATALOG.md
   ```
3. To pre-load the new mode, add its `slug` to `includeSlugs` in `custom-modes/manifest.json` before running the sync.

See [AGENT_CATALOG.md](AGENT_CATALOG.md) for the full per-mode listing (slug, name, category, description, pre-load status).

## 🚀 Quick Start

For Roo+ consumers the modes are already wired in — see the **Roo+ Canonical Model** section above.

To use this catalog directly with Roo Code:

```bash
# Clone the repository
git clone https://github.com/jtgsystems/Custom-Modes-Roo-Code.git
cd Custom-Modes-Roo-Code

# Validate a mode file (optional)
python3 scripts/validate_custom_modes.py custom_modes.d/<category>/<slug>.yaml
```

## 📚 Table of Contents

- [Roo+ Canonical Model](#roo-canonical-model)
- [Overview](#overview)
- [Agent Categories](#agent-categories)
- [SOTA 2026 Personas](#sota-2026-personas)
- [Installation](#installation)
- [Usage](#usage)
- [Agent Structure](#agent-structure)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## 🎯 Overview

This repository contains a meticulously curated collection of AI agent configurations for Roo Code, designed to accelerate development workflows across multiple domains. Each agent is optimized for 2026 development standards with emphasis on:

- **Security-First Architecture** 🔒
- **Performance Optimization** ⚡
- **Modern Framework Support** 🏗️
- **Industry Best Practices** ✨
- **Comprehensive Domain Coverage** 🌐

### Key Features

- ✅ **290 Specialized Modes** across category directories
- ✅ **11 SOTA 2026 Reasoning Personas** for advanced cognitive workflows
- ✅ **YAML-based Configuration** for easy customization
- ✅ **2026 Security Standards** compliance (OWASP, Zero-Trust)
- ✅ **Production-Ready Templates**
- ✅ **Cross-Platform Compatibility**
- ✅ **Modular Architecture**

### 2026 Technology Stack

All agents are updated to reference the latest 2026 technology stack:

| Technology | Version |
|---|---|
| React | 19+ |
| Node.js | 22+ |
| Python | 3.13+ |
| TypeScript | 5.7+ |
| Go | 1.24+ |
| Java | 24 |
| Next.js | 16 |
| .NET | 9 |
| Kubernetes | 1.32 |
| Terraform | 1.11 |

## 🗂️ Agent Categories

### 🧠 AI & Machine Learning (14 agents)
**Specialized AI/ML development and deployment**
- Machine Learning Engineers
- AI System Architects
- Data Science Specialists
- MLOps Engineers
- Computer Vision Experts
- NLP Specialists
- LLM Integration Specialists
- RAG Evaluators

### 💼 Business & Product (18 agents)
**Business strategy and product development**
- Product Managers
- Business Analysts
- Marketing Specialists
- Sales Engineers
- Content Strategists
- Customer Success Managers

### 💻 Core Development (58 agents)
**Foundation development roles and architectures**
- Full-Stack Developers
- Backend Specialists
- Frontend Experts
- System Architects
- API Designers
- Integration Specialists
- Electron Desktop Experts
- Deep Research Protocol

### 🏗️ Infrastructure & DevOps (25 agents)
**Modern infrastructure and deployment**
- Cloud Engineers (AWS, Azure, GCP)
- Kubernetes Specialists
- Docker Experts
- Monitoring & Observability
- Network Engineers
- SRE Engineers
- Platform Engineers

### 💬 Language Specialists (23 agents)
**Programming language experts**
- **Python** - FastAPI, Django, asyncio
- **JavaScript/TypeScript** - React, Node.js, Next.js
- **Rust** - Systems programming, WebAssembly
- **Go** - Microservices, concurrent systems
- **Java** - Spring Boot, enterprise systems
- **C#** - .NET 9, Azure integration
- **Kotlin** - Coroutines, multiplatform
- **Swift** - SwiftUI, protocol-oriented
- **Angular** - Angular 15+ enterprise patterns
- **Vue.js** - Vue 3 Composition API

### ⚖️ Legal & Compliance (16 agents)
**Regulatory and legal expertise**
- GDPR Compliance
- Security Auditing
- Legal Documentation (Canada & USA)
- Regulatory Analysis
- Corporate Law
- Employment Law
- Criminal Law
- Intellectual Property

### 🎛️ Meta-Orchestration (37 agents)
**System coordination and workflow management**
- Workflow Orchestrators
- Project Coordinators
- System Monitors
- Process Optimizers
- Integration Managers
- Data Engineers & Analysts
- Search Specialists

### 🔐 Security & Quality (25 agents)
**Security-first development and quality assurance**
- Cybersecurity Experts
- Penetration Testers
- Security Auditors
- Accessibility Specialists
- Compliance Officers
- Debug Specialists
- Test Automators

### 🎯 Specialized Domains (16 agents)
**Industry-specific expertise**
- **Fintech** - Financial systems, compliance
- **Gaming** - Game development, engines
- **Blockchain** - Smart contracts, DeFi
- **IoT** - Edge computing, sensors
- **SEO** - Search optimization, analytics
- **Payment** - Gateway integration, PCI

### 🧠 SOTA 2026 Personas (11 agents)
**State-of-the-art reasoning and cognitive personas**

See [SOTA 2026 Personas](#sota-2026-personas) section below for details.

## 🧠 SOTA 2026 Personas

Advanced cognitive personas implementing cutting-edge reasoning patterns from the Agent Personas SOTA 2026 specification.

### Tier 1: Foundational Reasoning
| Persona | Level | Description |
|---|---|---|
| 🏛️ Core Reasoning Architect | L1 Root | Immutable reasoning foundation, RSC guard |
| 🔮 Formula Cascade Oracle | L2 | Fractal formula notation master |
| 🔬 Fractal Elaborator | L3-L6 | Infinite zoom specialist |

### Tier 2: Engineering Excellence
| Persona | Level | Description |
|---|---|---|
| ⚡ High-Performance Engineer | L2-L3 | Gallie-optimized hardware sympathizer |
| 🚀 SOTA Stack Master | L2 | Next-Gen Web & Language Virtuoso |
| 🎨 UI/UX Vibe Master | L2 | Aesthetic Intelligence + Layout Enforcer |

### Tier 3: Quality, Integrity & Operations
| Persona | Level | Description |
|---|---|---|
| 🛡️ Anti-Fiction Sentinel | L1 | Truth Enforcer & Neuro-Symbolic Verifier |
| 📡 DevOps Observability Sentinel | L3 | Production Guardian & Incident Commander |

### Tier 4: Problem-Solving & Cognitive
| Persona | Level | Description |
|---|---|---|
| 🧩 Problem Solving Maestro | L2-L3 | Master of All Heuristics |
| 🧠 Cognitive Multi-Thinker | L2 | Parallel Thought Stream + Six Hats |
| 🕸️ Agentic Swarm Conductor | L2-L3 | Hive-Mind Orchestrator |

See [AGENT_CATALOG.md](AGENT_CATALOG.md) for the full per-mode listing, including the SOTA reasoning personas.

## 📦 Installation

### Prerequisites

- **Roo Code** extension for VS Code / Antigravity IDE
- **Git** for repository management
- **Node.js 22+** (recommended)
- **Python 3.13+** (for AI/ML agents and conversion scripts)

### Method 1: Full Installation (Roo+)

In Roo+, modes are installed automatically: [`custom_modes.d/`](custom_modes.d/) is the canonical catalog, and the parent repo's sync regenerates `.roomodes`, `pre-installed-modes.yml`, and `modes.yml`. Run from the Roo+ repo root:

```bash
node scripts/sync-custom-modes.mjs
```

### Method 2: Selective Installation

Copy a specific mode file (or a whole category directory) from the canonical catalog into your Roo Code global storage:

```bash
# Install a single mode
cp custom_modes.d/<category>/<slug>.yaml ~/.config/Antigravity/User/globalStorage/rooveterinaryinc.roo-cline/settings/.roo/

# Install a whole category
cp -r custom_modes.d/<category> ~/.config/Antigravity/User/globalStorage/rooveterinaryinc.roo-cline/settings/.roo/
```

### Method 3: Direct YAML Usage

Each agent YAML file can be used directly with Roo Code's custom mode system:

```yaml
# Example: Loading an agent
slug: python-developer
name: 🐍 Python Developer
roleDefinition: ...
customInstructions: ...
groups: [read, edit, browser, command, mcp]
```

## 🔧 Agent Structure

### YAML Configuration Format

```yaml
slug: agent-name                    # Unique identifier (kebab-case)
name: 🏷️ Agent Display Name         # Display name with emoji
category: category-name             # Primary category
subcategory: subcategory-name       # Subcategory
roleDefinition: >-                  # Agent's role description
  You are a specialist in...
customInstructions: >-              # Detailed instructions
  ## 2026 Standards Compliance
  ...
groups:                             # Permission groups
  - read
  - edit
  - browser
  - command
  - mcp
version: '2026.1'                  # Schema version
lastUpdated: '2026-05-12'          # Last update date
```

### Directory Organization

```
custom_modes.d/               # Canonical catalog (290 modes)
├── <category>/               # One directory per category
│   ├── <slug>.yaml           # One mode per file (customModes: wrapper)
│   └── ...                   # Multiple modes per category
├── ai/                       # AI & Machine Learning modes
├── backend/                  # Backend development modes
├── docs/                     # Documentation modes
├── frontend/                 # Frontend development modes
├── i18n/                     # Localization modes
├── observability/            # Observability modes
├── react/                    # React modes
├── research/                 # Research modes
├── security/                 # Security modes
├── seo/                      # SEO modes
└── ...                       # ~238 categories total
```

## 🛠️ Scripts

| Script | Purpose |
|---|---|
| `scripts/validate_custom_modes.py` | Validate `custom_modes.d/` mode files against the schema |
| `scripts/verify_modes.py` | Verify every mode in the canonical catalog |
| `scripts/sync-custom-modes.mjs` (parent repo) | Regenerate `.roomodes`, `pre-installed-modes.yml`, `modes.yml` |
| `scripts/generate-catalog.mjs` (parent repo) | Regenerate `AGENT_CATALOG.md` |

## 🔐 Security

### Security Standards Compliance

All agents adhere to **2026 Security Standards**:

- ✅ **Zero-Trust Architecture**
- ✅ **Secure by Default Configuration**
- ✅ **OWASP Top 10 Compliance** (including LLM Top 10)
- ✅ **Supply Chain Security**
- ✅ **Container Security**
- ✅ **API Security Best Practices**
- ✅ **Sub-100ms Performance Targets**
- ✅ **>95% Test Coverage Standards**

### Reporting Security Issues

Please report security vulnerabilities to: **security@jtgsystems.com**

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Workflow

1. Fork → Branch → Add Agent → Test → PR
2. Follow YAML structure standards (see schema in `schemas/custom_modes.schema.json`)
3. Include comprehensive role description and 2026 security features
4. Validate with `python3 scripts/validate_custom_modes.py`

## 📊 Statistics

The catalog contains **290 modes** across **~238 category directories**. For the current per-mode breakdown (slug, name, category, description, pre-load status), see [AGENT_CATALOG.md](AGENT_CATALOG.md).

## 🔗 Related Resources

- **Roo Code Extension** - [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=RooCline.roo-cline) - AI coding assistant
- **Antigravity IDE** - Enhanced VS Code distribution with Roo Code integration
- **GitHub Repository** - [This Project](https://github.com/jtgsystems/Custom-Modes-Roo-Code) - Agent configurations

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/jtgsystems/Custom-Modes-Roo-Code/issues) - Report bugs or request features
- **Discussions**: [GitHub Discussions](https://github.com/jtgsystems/Custom-Modes-Roo-Code/discussions) - Ask questions and share ideas
- **Contact**: [JTG Systems](https://jtgsystems.com) - Professional support
- **Email**: support@jtgsystems.com

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025-2026 JTG Systems

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 Acknowledgments

- **Roo Code Team** - For the amazing development platform
- **Open Source Community** - For continuous inspiration
- **Contributors** - For making this project possible
- **Security Researchers** - For ensuring robust security standards

---

<div align="center">

**Built with ❤️ by [JTG Systems](https://github.com/jtgsystems)**

**Following 2026 Security-First Development Standards**

[![GitHub](https://img.shields.io/badge/GitHub-jtgsystems-black?logo=github)](https://github.com/jtgsystems)
[![Website](https://img.shields.io/badge/Website-jtgsystems.com-blue)](https://jtgsystems.com)

</div>
