# AI Workflow Architecture — Agent Skills for Context Engineering

A comprehensive, open collection of Agent Skills combining **context engineering knowledge** with a **standardized AI workflow architecture** for building production-grade agent systems. Deployable to Claude Code, Gemini CLI, OpenCode, and Codex.

**18 skills** · **9 slash commands** · **L0–L3 workflow hierarchy** · **Claude → Gemini portation**

## Quick Start

### Claude Code (Slash Commands)
```bash
# Install workflow commands locally
bash bin/install.sh --claude-local

# Then use:
/workflow:orchestrate "Build a REST API with authentication"
/workflow:progress
/workflow:port ./my-claude-skill
```

### npm / npx
```bash
npx ai-workflow-skills --all --local
```

### Plugin Marketplace (knowledge skills only)
```
/plugin marketplace add muratcankoylan/Agent-Skills-for-Context-Engineering
/plugin install workflow-execution-layer@ai-workflow-architecture
/plugin install context-engineering-fundamentals@ai-workflow-architecture
```

---

## What is Context Engineering?

Context engineering is the discipline of managing the language model's context window. Unlike prompt engineering, which focuses on crafting effective instructions, context engineering addresses the holistic curation of all information that enters the model's limited attention budget: system prompts, tool definitions, retrieved documents, message history, and tool outputs.

The fundamental challenge is that context windows are constrained not by raw token capacity but by attention mechanics. As context length increases, models exhibit predictable degradation patterns: the "lost-in-the-middle" phenomenon, U-shaped attention curves, and attention scarcity. Effective context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of desired outcomes.

## Recognition

This repository is cited in academic research as foundational work on static skill architecture:

> "While static skills are well-recognized [Anthropic, 2025b; Muratcan Koylan, 2025], MCE is among the first to dynamically evolve them, bridging manual skill engineering and autonomous self-improvement."

— [Meta Context Engineering via Agentic Skill Evolution](https://arxiv.org/pdf/2601.21557), Peking University State Key Laboratory of General Artificial Intelligence (2026)

## Skills Overview

### Tier 1 — Workflow Execution (New in v2.0)

The operational backbone: an L0–L3 agent hierarchy implementing the Universal Agent Workflow standard.

| Skill | Level | Description |
|-------|-------|-------------|
| [pipeline-orchestrator](skills/pipeline-orchestrator/) | L0 | Epic decomposition, `kanban_board.md` state management, delegation orchestration |
| [story-executor](skills/story-executor/) | L1 | Epic-to-story decomposition, L3 worker routing |
| [task-reviewer](skills/task-reviewer/) | L2 | **Exclusive git commit authority**; clean code + AC validation |
| [task-executor](skills/task-executor/) | L3 | Non-committing code generation; minimal-footprint implementation |
| [task-rework](skills/task-rework/) | L3 | Defect repair with rework-loop detection |
| [test-executor](skills/test-executor/) | L3 | Non-committing test suite creation; risk-based coverage |

### Tier 2 — Cross-Platform Migration (New in v2.0)

| Skill | Description |
|-------|-------------|
| [cross-skill-porter](skills/cross-skill/) | 5-phase Claude Code → Gemini CLI portation pipeline. Non-destructive. Outputs `TEST_RESULTS.md`. |
| [universal-agent-workflow](skills/universal-agent-workflow/) | Binding standard: abstraction hierarchy, state tracking, Non-Commit Policy |

### Tier 3 — Context Engineering Knowledge Base

**Foundational:**

| Skill | Description |
|-------|-------------|
| [context-fundamentals](skills/context-fundamentals/) | Context window anatomy, attention mechanics, progressive disclosure |
| [context-degradation](skills/context-degradation/) | Lost-in-middle, context poisoning, distraction, and clash patterns |
| [context-compression](skills/context-compression/) | Compression strategies, tokens-per-task optimization, probe-based evaluation |

**Architectural:**

| Skill | Description |
|-------|-------------|
| [multi-agent-patterns](skills/multi-agent-patterns/) | Supervisor, swarm, and hierarchical multi-agent architectures |
| [memory-systems](skills/memory-systems/) | Temporal knowledge graphs, vector stores, file-system-as-memory |
| [tool-design](skills/tool-design/) | Consolidation principle, MCP integration, tool naming conventions |

**Operational:**

| Skill | Description |
|-------|-------------|
| [context-optimization](skills/context-optimization/) | KV-cache prefix caching, observation masking, context partitioning |
| [evaluation](skills/evaluation/) | Multi-dimensional rubrics, LLM-as-judge patterns |
| [advanced-evaluation](skills/advanced-evaluation/) | Pairwise comparison, position bias mitigation, production evaluation |

**Methodology:**

| Skill | Description |
|-------|-------------|
| [project-development](skills/project-development/) | Task-model fit analysis, staged pipeline architecture, structured output design |

**Cognitive Architecture:**

| Skill | Description |
|-------|-------------|
| [bdi-mental-states](skills/bdi-mental-states/) | Transform RDF context into BDI mental states (beliefs, desires, intentions) for deliberative reasoning |
| [filesystem-context](skills/filesystem-context/) | Dynamic context discovery via filesystem, tool output offloading, plan persistence |
| [hosted-agents](skills/hosted-agents/) | Background coding agents: sandboxed VMs, pre-built images, multiplayer support |

## Design Philosophy

### Progressive Disclosure

Each skill is structured for efficient context use. At startup, agents load only skill names and descriptions. Full content loads only when a skill is activated for relevant tasks.

### Platform Agnosticism

These skills focus on transferable principles rather than vendor-specific implementations. The patterns work across Claude Code, Cursor, and any agent platform that supports skills or allows custom instructions.

### Conceptual Foundation with Practical Examples

Scripts and examples demonstrate concepts using Python pseudocode that works across environments without requiring specific dependency installations.

## Slash Commands

Install the workflow commands and invoke the full agent pipeline directly from Claude Code:

| Command | Description |
|---------|-------------|
| `/workflow:orchestrate` | Decompose requirements into Epics/Stories; initialize `kanban_board.md` |
| `/workflow:plan` | Break an Epic into implementable L3 stories; route to workers |
| `/workflow:execute` | Implement a story (non-committing); updates board to `To Review` |
| `/workflow:review` | Validate + commit approved code; reject to `To Rework` |
| `/workflow:rework` | Fix reviewer-rejected implementation; loop detection after 3 attempts |
| `/workflow:test` | Create test suites (non-committing); risk-based coverage targets |
| `/workflow:port` | Convert a Claude Code skill to Gemini CLI format (5-phase pipeline) |
| `/workflow:progress` | Show current `kanban_board.md` pipeline status |
| `/workflow:quick` | Fast path for single-step tasks (no Epic decomposition) |

**Three core workflow rules:**
1. **L0/L1 orchestrators** never write application code
2. **L3 workers** never commit — leave all changes uncommitted
3. **Only `task-reviewer` (L2)** may run `git commit`

## Installation

### Claude Code (recommended)

**Slash commands + skills:**
```bash
git clone https://github.com/netzkontrast/Agent-Skills-for-Context-Engineering
cd Agent-Skills-for-Context-Engineering
bash bin/install.sh --claude-local   # or --claude-global for all projects
```

**Plugin marketplace (skills only):**
```
/plugin marketplace add muratcankoylan/Agent-Skills-for-Context-Engineering
/plugin install workflow-execution-layer@ai-workflow-architecture
/plugin install cross-platform-migration@ai-workflow-architecture
/plugin install context-engineering-fundamentals@ai-workflow-architecture
/plugin install agent-architecture-patterns@ai-workflow-architecture
/plugin install agent-evaluation@ai-workflow-architecture
/plugin install agent-development-methodology@ai-workflow-architecture
```

### Gemini CLI

Port skills using the Cross-Skill Porter, then install:
```bash
python skills/cross-skill/scripts/cross_skill_porter.py ./skills/pipeline-orchestrator
gemini extensions install ./skills/pipeline-orchestrator-ported/
# Or install all:
bash bin/install.sh --gemini-local
```

### Codex / OpenCode

Copy `commands/workflow/` to your platform's command directory. Skills follow the standard
`skills/<name>/SKILL.md` format compatible with Codex skill conventions.

### npm / npx

```bash
npx ai-workflow-skills --all --local
```

## Skill Triggers

| Skill | Triggers On |
|-------|-------------|
| `pipeline-orchestrator` | "orchestrate", "decompose requirement", "create kanban board" |
| `story-executor` | "break down epic", "execute next story", "advance pipeline" |
| `task-executor` | "implement this story", "write the code for", "execute task" |
| `task-reviewer` | "review this implementation", "validate story", "approve and commit" |
| `task-rework` | "rework this story", "fix reviewer findings", "address rejection" |
| `test-executor` | "write tests for", "create test suite", "add coverage" |
| `cross-skill-porter` | "port skill to Gemini", "convert Claude skills", "migrate cross-platform" |
| `universal-agent-workflow` | "what is the standard workflow", "how should skills be structured" |
| `context-fundamentals` | "understand context", "explain context windows", "design agent architecture" |
| `context-degradation` | "diagnose context problems", "fix lost-in-middle", "debug agent failures" |
| `context-compression` | "compress context", "summarize conversation", "reduce token usage" |
| `context-optimization` | "optimize context", "reduce token costs", "implement KV-cache" |
| `multi-agent-patterns` | "design multi-agent system", "implement supervisor pattern" |
| `memory-systems` | "implement agent memory", "build knowledge graph", "track entities" |
| `tool-design` | "design agent tools", "reduce tool complexity", "implement MCP tools" |
| `filesystem-context` | "offload context to files", "dynamic context discovery", "agent scratch pad", "file-based context" |
| `hosted-agents` | "build background agent", "create hosted coding agent", "sandboxed execution", "multiplayer agent", "Modal sandboxes" |
| `evaluation` | "evaluate agent performance", "build test framework", "measure quality" |
| `advanced-evaluation` | "implement LLM-as-judge", "compare model outputs", "mitigate bias" |
| `project-development` | "start LLM project", "design batch pipeline", "evaluate task-model fit" |
| `bdi-mental-states` | "model agent mental states", "implement BDI architecture", "transform RDF to beliefs", "build cognitive agent" |
| `accessibility-tester` | Use this agent when you need comprehensive accessibility testing, WCAG compli... |
| `ad-security-reviewer` | Use this agent when you need to audit Active Directory security posture, eval... |
| `agent-installer` | Use this agent when the user wants to discover, browse, or install Claude Cod... |
| `agent-organizer` | Use when assembling and optimizing multi-agent teams to execute complex proje... |
| `ai-engineer` | Use this agent when architecting, implementing, or optimizing end-to-end AI s... |
| `angular-architect` | Use when architecting enterprise Angular 15+ applications with complex state ... |
| `api-design` | Agent skill |
| `api-designer` | Use this agent when designing new APIs, creating API specifications, or refac... |
| `api-documenter` | Use this agent when creating or improving API documentation, writing OpenAPI ... |
| `architect-reviewer` | Use this agent when you need to evaluate system design decisions, architectur... |
| `article-writing` | Agent skill |
| `azure-infra-engineer` | Use when designing, deploying, or managing Azure infrastructure with focus on... |
| `backend-developer` | Use this agent when building server-side APIs, microservices, and backend sys... |
| `backend-patterns` | Agent skill |
| `blockchain-developer` | Use this agent when building smart contracts, DApps, and blockchain protocols... |
| `build-engineer` | Use this agent when you need to optimize build performance, reduce compilatio... |
| `business-analyst` | Use when analyzing business processes, gathering requirements from stakeholde... |
| `chaos-engineer` | Use this agent when you need to design and execute controlled failure experim... |
| `cli-developer` | Use this agent when building command-line tools and terminal applications tha... |
| `clickhouse-io` | Agent skill |
| `cloud-architect` | Use this agent when you need to design, evaluate, or optimize cloud infrastru... |
| `code-reviewer` | Use this agent when you need to conduct comprehensive code reviews focusing o... |
| `coding-standards` | Agent skill |
| `competitive-analyst` | Use when you need to analyze direct and indirect competitors, benchmark again... |
| `compliance-auditor` | Use this agent when you need to achieve regulatory compliance, implement comp... |
| `configure-ecc` | Agent skill |
| `content-engine` | Agent skill |
| `content-hash-cache-pattern` | Agent skill |
| `content-marketer` | Use this agent when you need to develop comprehensive content strategies, cre... |
| `context-manager` | Use for managing shared state, information retrieval, and data synchronizatio... |
| `continuous-learning` | Agent skill |
| `continuous-learning-v2` | Agent skill |
| `cost-aware-llm-pipeline` | Agent skill |
| `cpp-coding-standards` | Agent skill |
| `cpp-pro` | Use this agent when building high-performance C++ systems requiring modern C+... |
| `cpp-testing` | Agent skill |
| `cross-skill` | Agent skill |
| `csharp-developer` | Use this agent when building ASP.NET Core web APIs, cloud-native .NET solutio... |
| `customer-success-manager` | Use this agent when you need to assess customer health, develop retention str... |
| `data-analyst` | Use when you need to extract insights from business data, create dashboards a... |
| `data-engineer` | Use this agent when you need to design, build, or optimize data pipelines, ET... |
| `data-researcher` | Use this agent when you need to discover, collect, and validate data from mul... |
| `data-scientist` | Use this agent when you need to analyze data patterns, build predictive model... |
| `database-administrator` | Use this agent when optimizing database performance, implementing high-availa... |
| `database-migrations` | Agent skill |
| `database-optimizer` | Use this agent when you need to analyze slow queries, optimize database perfo... |
| `debugger` | Use this agent when you need to diagnose and fix bugs, identify root causes o... |
| `dependency-manager` | Use this agent when you need to audit dependencies for vulnerabilities, resol... |
| `deployment-engineer` | Use this agent when designing, building, or optimizing CI/CD pipelines and de... |
| `deployment-patterns` | Agent skill |
| `devops-engineer` | Use this agent when building or optimizing infrastructure automation, CI/CD p... |
| `devops-incident-responder` | Use when actively responding to production incidents, diagnosing critical ser... |
| `django-developer` | Use when building Django 4+ web applications, REST APIs, or modernizing exist... |
| `django-patterns` | Agent skill |
| `django-security` | Agent skill |
| `django-tdd` | Agent skill |
| `django-verification` | Agent skill |
| `docker-expert` | Use this agent when you need to build, optimize, or secure Docker container i... |
| `docker-patterns` | Agent skill |
| `documentation-engineer` | Use this agent when you need to create, architect, or overhaul comprehensive ... |
| `dotnet-core-expert` | Use when building .NET Core applications requiring cloud-native architecture,... |
| `dotnet-framework-4.8-expert` | Use this agent when working on legacy .NET Framework 4.8 enterprise applicati... |
| `dx-optimizer` | Use this agent when optimizing the complete developer workflow including buil... |
| `e2e-testing` | Agent skill |
| `electron-pro` | Use this agent when building Electron desktop applications that require nativ... |
| `elixir-expert` | Use this agent when you need to build fault-tolerant, concurrent systems leve... |
| `embedded-systems` | Use when developing firmware for resource-constrained microcontrollers, imple... |
| `error-coordinator` | Use this agent when distributed system errors occur and need coordinated hand... |
| `error-detective` | Use this agent when you need to diagnose why errors are occurring in your sys... |
| `eval-harness` | Agent skill |
| `fintech-engineer` | Use when building payment systems, financial integrations, or compliance-heav... |
| `flutter-expert` | Use when building cross-platform mobile applications with Flutter 3+ that req... |
| `foundation-models-on-device` | Agent skill |
| `frontend-developer` | Use when building complete frontend applications across React, Vue, and Angul... |
| `frontend-patterns` | Agent skill |
| `frontend-slides` | Agent skill |
| `fullstack-developer` | Use this agent when you need to build complete features spanning database, AP... |
| `game-developer` | Use this agent when implementing game systems, optimizing graphics rendering,... |
| `git-workflow-manager` | Use this agent when you need to design, establish, or optimize Git workflows,... |
| `golang-patterns` | Agent skill |
| `golang-pro` | Use when building Go applications requiring concurrent programming, high-perf... |
| `golang-testing` | Agent skill |
| `graphql-architect` | Use this agent when designing or evolving GraphQL schemas across microservice... |
| `incident-responder` | Use this agent when an active security breach, service outage, or operational... |
| `investor-materials` | Agent skill |
| `investor-outreach` | Agent skill |
| `iot-engineer` | Use when designing and deploying IoT solutions requiring expertise in device ... |
| `it-ops-orchestrator` | Use for orchestrating complex IT operations tasks that span multiple domains ... |
| `iterative-retrieval` | Agent skill |
| `java-architect` | Use this agent when designing enterprise Java architectures, migrating Spring... |
| `java-coding-standards` | Agent skill |
| `javascript-pro` | Use this agent when you need to build, optimize, or refactor modern JavaScrip... |
| `jpa-patterns` | Agent skill |
| `knowledge-synthesizer` | Use when you need to extract actionable patterns from agent interactions, syn... |
| `kotlin-specialist` | Use when building Kotlin applications requiring advanced coroutine patterns, ... |
| `kubernetes-specialist` | Use this agent when you need to design, deploy, configure, or troubleshoot Ku... |
| `laravel-specialist` | Use when building Laravel 10+ applications, architecting Eloquent models with... |
| `legacy-modernizer` | Use this agent when modernizing legacy systems that need incremental migratio... |
| `legal-advisor` | Use this agent when you need to draft contracts, review compliance requiremen... |
| `liquid-glass-design` | Agent skill |
| `llm-architect` | Use when designing LLM systems for production, implementing fine-tuning or RA... |
| `m365-admin` | Use when automating Microsoft 365 administrative tasks including Exchange Onl... |
| `machine-learning-engineer` | Use this agent when you need to deploy, optimize, or serve machine learning m... |
| `market-research` | Agent skill |
| `market-researcher` | Use this agent when you need to analyze markets, understand consumer behavior... |
| `mcp-developer` | Use this agent when you need to build, debug, or optimize Model Context Proto... |
| `microservices-architect` | Use when designing distributed system architecture, decomposing monolithic ap... |
| `ml-engineer` | Use this agent when building production ML systems requiring model training p... |
| `mlops-engineer` | Use this agent when you need to design and implement ML infrastructure, set u... |
| `mobile-app-developer` | Use this agent when developing iOS and Android mobile applications with focus... |
| `mobile-developer` | Use this agent when building cross-platform mobile applications requiring nat... |
| `multi-agent-coordinator` | Use when coordinating multiple concurrent agents that need to communicate, sh... |
| `network-engineer` | Use this agent when designing, optimizing, or troubleshooting cloud and hybri... |
| `nextjs-developer` | Use this agent when building production Next.js 14+ applications that require... |
| `nlp-engineer` | Use when building production NLP systems, implementing text processing pipeli... |
| `nutrient-document-processing` | Agent skill |
| `payment-integration` | Use this agent when implementing payment systems, integrating payment gateway... |
| `penetration-tester` | Use this agent when you need to conduct authorized security penetration tests... |
| `performance-engineer` | Use this agent when you need to identify and eliminate performance bottleneck... |
| `performance-monitor` | Use when establishing observability infrastructure to track system metrics, d... |
| `php-pro` | Use this agent when working with PHP 8.3+ projects that require strict typing... |
| `platform-engineer` | Use when building or improving internal developer platforms (IDPs), designing... |
| `postgres-patterns` | Agent skill |
| `postgres-pro` | Use when you need to optimize PostgreSQL performance, design high-availabilit... |
| `powershell-5.1-expert` | Use when automating Windows infrastructure tasks requiring PowerShell 5.1 scr... |
| `powershell-7-expert` | Use when building cross-platform cloud automation scripts, Azure infrastructu... |
| `powershell-module-architect` | Use this agent when architecting and refactoring PowerShell modules, designin... |
| `powershell-security-hardening` | Use this agent when you need to harden PowerShell automation, secure remoting... |
| `powershell-ui-architect` | Use when designing or building desktop graphical interfaces (WinForms, WPF, M... |
| `product-manager` | Use this agent when you need to make product strategy decisions, prioritize f... |
| `project-guidelines-example` | Agent skill |
| `project-manager` | Use this agent when you need to establish project plans, track execution prog... |
| `prompt-engineer` | Use this agent when you need to design, optimize, test, or evaluate prompts f... |
| `python-patterns` | Agent skill |
| `python-pro` | Use this agent when you need to build type-safe, production-ready Python code... |
| `python-testing` | Agent skill |
| `qa-expert` | Use this agent when you need comprehensive quality assurance strategy, test p... |
| `quant-analyst` | Use this agent when you need to develop quantitative trading strategies, buil... |
| `rails-expert` | Use when building or modernizing Rails applications requiring full-stack deve... |
| `react-specialist` | Use when optimizing existing React applications for performance, implementing... |
| `refactoring-specialist` | Use when you need to transform poorly structured, complex, or duplicated code... |
| `regex-vs-llm-structured-text` | Agent skill |
| `research-analyst` | Use this agent when you need comprehensive research across multiple sources w... |
| `risk-manager` | Use this agent when you need to identify, quantify, and mitigate enterprise-l... |
| `rust-engineer` | Use when building Rust systems where memory safety, ownership patterns, zero-... |
| `sales-engineer` | Use this agent when you need to conduct technical pre-sales activities includ... |
| `scientific-literature-researcher` | Use when you need to search scientific literature and retrieve structured exp... |
| `scrum-master` | Use when teams need facilitation, process optimization, velocity improvement,... |
| `search-first` | Agent skill |
| `search-specialist` | Use when you need to find specific information across multiple sources using ... |
| `security-auditor` | Use this agent when conducting comprehensive security audits, compliance asse... |
| `security-engineer` | Use this agent when implementing comprehensive security solutions across infr... |
| `security-review` | Agent skill |
| `security-scan` | Agent skill |
| `seo-specialist` | Use this agent when you need comprehensive SEO optimization encompassing tech... |
| `skill-stocktake` | Agent skill |
| `slack-expert` | Use this agent when developing Slack applications, implementing Slack API int... |
| `spring-boot-engineer` | Use this agent when building enterprise Spring Boot 3+ applications requiring... |
| `springboot-patterns` | Agent skill |
| `springboot-security` | Agent skill |
| `springboot-tdd` | Agent skill |
| `springboot-verification` | Agent skill |
| `sql-pro` | Use this agent when you need to optimize complex SQL queries, design efficien... |
| `sre-engineer` | Use this agent when you need to establish or improve system reliability throu... |
| `strategic-compact` | Agent skill |
| `swift-actor-persistence` | Agent skill |
| `swift-concurrency-6-2` | Agent skill |
| `swift-expert` | Use this agent when building native iOS, macOS, or server-side Swift applicat... |
| `swift-protocol-di-testing` | Agent skill |
| `swiftui-patterns` | Agent skill |
| `task-distributor` | Use when distributing tasks across multiple agents or workers, managing queue... |
| `tdd-workflow` | Agent skill |
| `technical-writer` | Use this agent when you need to create, improve, or maintain technical docume... |
| `terraform-engineer` | Use when building, refactoring, or scaling infrastructure as code using Terra... |
| `terragrunt-expert` | Expert Terragrunt specialist mastering infrastructure orchestration, DRY conf... |
| `test-automator` | Use this agent when you need to build, implement, or enhance automated test f... |
| `tooling-engineer` | Use this agent when you need to build or enhance developer tools including CL... |
| `trend-analyst` | Use when analyzing emerging patterns, predicting industry shifts, or developi... |
| `typescript-pro` | Use when implementing TypeScript code requiring advanced type system patterns... |
| `ui-designer` | Use this agent when designing visual interfaces, creating design systems, bui... |
| `ux-researcher` | Use this agent when you need to conduct user research, analyze user behavior,... |
| `verification-loop` | Agent skill |
| `visa-doc-translate` | Agent skill |
| `vue-expert` | Use this agent when building Vue 3 applications that require Composition API ... |
| `websocket-engineer` | Use this agent when implementing real-time bidirectional communication featur... |
| `windows-infra-admin` | Use when managing Windows Server infrastructure, Active Directory, DNS, DHCP,... |
| `wordpress-master` | Use this agent when you need to architect, optimize, or troubleshoot WordPres... |
| `workflow-orchestrator` | Use this agent when you need to design, implement, or optimize complex busine... |

<img width="1014" height="894" alt="Screenshot 2025-12-26 at 12 34 47 PM" src="https://github.com/user-attachments/assets/f79aaf03-fd2d-4c71-a630-7027adeb9bfe" />
## Examples

The [examples](examples/) folder contains complete system designs that demonstrate how multiple skills work together in practice.

| Example | Description | Skills Applied |
|---------|-------------|----------------|
| [digital-brain-skill](examples/digital-brain-skill/) | **NEW** Personal operating system for founders and creators. Complete Claude Code skill with 6 modules, 4 automation scripts | context-fundamentals, context-optimization, memory-systems, tool-design, multi-agent-patterns, evaluation, project-development |
| [x-to-book-system](examples/x-to-book-system/) | Multi-agent system that monitors X accounts and generates daily synthesized books | multi-agent-patterns, memory-systems, context-optimization, tool-design, evaluation |
| [llm-as-judge-skills](examples/llm-as-judge-skills/) | Production-ready LLM evaluation tools with TypeScript implementation, 19 passing tests | advanced-evaluation, tool-design, context-fundamentals, evaluation |
| [book-sft-pipeline](examples/book-sft-pipeline/) | Train models to write in any author's style. Includes Gertrude Stein case study with 70% human score on Pangram, $2 total cost | project-development, context-compression, multi-agent-patterns, evaluation |

Each example includes:
- Complete PRD with architecture decisions
- Skills mapping showing which concepts informed each decision
- Implementation guidance

### Digital Brain Skill Example

The [digital-brain-skill](examples/digital-brain-skill/) example is a complete personal operating system demonstrating comprehensive skills application:

- **Progressive Disclosure**: 3-level loading (SKILL.md → MODULE.md → data files)
- **Module Isolation**: 6 independent modules (identity, content, knowledge, network, operations, agents)
- **Append-Only Memory**: JSONL files with schema-first lines for agent-friendly parsing
- **Automation Scripts**: 4 consolidated tools (weekly_review, content_ideas, stale_contacts, idea_to_draft)

Includes detailed traceability in [HOW-SKILLS-BUILT-THIS.md](examples/digital-brain-skill/HOW-SKILLS-BUILT-THIS.md) mapping every architectural decision to specific skill principles.

### LLM-as-Judge Skills Example

The [llm-as-judge-skills](examples/llm-as-judge-skills/) example is a complete TypeScript implementation demonstrating:

- **Direct Scoring**: Evaluate responses against weighted criteria with rubric support
- **Pairwise Comparison**: Compare responses with position bias mitigation
- **Rubric Generation**: Create domain-specific evaluation standards
- **EvaluatorAgent**: High-level agent combining all evaluation capabilities

### Book SFT Pipeline Example

The [book-sft-pipeline](examples/book-sft-pipeline/) example demonstrates training small models (8B) to write in any author's style:

- **Intelligent Segmentation**: Two-tier chunking with overlap for maximum training examples
- **Prompt Diversity**: 15+ templates to prevent memorization and force style learning
- **Tinker Integration**: Complete LoRA training workflow with $2 total cost
- **Validation Methodology**: Modern scenario testing proves style transfer vs content memorization

Integrates with context engineering skills: project-development, context-compression, multi-agent-patterns, evaluation.

## Star History
<img width="3664" height="2648" alt="star-history-2026224" src="https://github.com/user-attachments/assets/b3bdbf23-4b6a-4774-ae85-42ef4d9b2d79" />

## Structure

```
/
├── CLAUDE.md                     # Root project context (loaded every session)
├── SKILL.md                      # Master collection skill definition
├── CHANGELOG.md                  # Version history
├── package.json                  # npm distribution metadata
├── bin/
│   └── install.sh                # Cross-platform installer (Claude/Gemini/all)
├── commands/
│   └── workflow/                 # Slash commands for Claude Code
│       ├── orchestrate.md        # /workflow:orchestrate
│       ├── plan.md               # /workflow:plan
│       ├── execute.md            # /workflow:execute
│       ├── review.md             # /workflow:review
│       ├── rework.md             # /workflow:rework
│       ├── test.md               # /workflow:test
│       ├── port.md               # /workflow:port
│       ├── progress.md           # /workflow:progress
│       └── quick.md              # /workflow:quick
├── skills/
│   ├── pipeline-orchestrator/    # L0 workflow skill
│   ├── story-executor/           # L1 workflow skill
│   ├── task-reviewer/            # L2 workflow skill
│   ├── task-executor/            # L3 workflow skill
│   ├── task-rework/              # L3 workflow skill
│   ├── test-executor/            # L3 workflow skill
│   ├── cross-skill/              # Cross-platform portation
│   ├── universal-agent-workflow/ # Workflow standard reference
│   └── [10 context-engineering knowledge skills]
└── template/
    └── SKILL.md                  # v2.0 skill template
```

Each skill follows the v2.0 structure:
```
skill-name/
├── SKILL.md              # Required: frontmatter (allowed-tools), instructions, Workflow Compliance
├── references/           # Optional: detailed docs, checklists, schemas
└── scripts/              # Optional: executable code demonstrating concepts
```

See [template/SKILL.md](template/SKILL.md) and [CONTRIBUTING.md](CONTRIBUTING.md) for v2.0 requirements.

## Contributing

This repository follows the Agent Skills open development model. Contributions are welcome. When contributing:

1. Use `template/SKILL.md` — it includes all v2.0 required fields
2. Add `allowed-tools` to YAML frontmatter (see CONTRIBUTING.md for level-based values)
3. Include `## Workflow Compliance` section with your skill's excludeTools mapping
4. Declare `**Level**:` in Skill Metadata
5. Keep SKILL.md under 500 lines; move detailed content to `references/`

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full v2.0 skill authoring requirements.

Feel free to contact [Muratcan Koylan](https://x.com/koylanai) for collaboration opportunities or any inquiries.

## License

MIT License - see LICENSE file for details.

## References

The principles in these skills are derived from research and production experience at leading AI labs and framework developers. Each skill includes references to the underlying research and case studies that inform its recommendations.

## Comprehensive Documentation
For a complete overview of the architecture and workflow, see [Architecture and Usage Documentation](docs/architecture_and_usage.md).
