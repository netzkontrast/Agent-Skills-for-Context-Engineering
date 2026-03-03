# Detailed Planning for the Autonomous Claude Suite

## 1. Project Objectives and Scope
This document outlines the systematic engineering phases required to construct a minimal, fully interconnected CLI toolkit. This toolkit will utilize the `Agent-Skills-for-Context-Engineering` repository's L0-L3 workflow architecture, integrating philosophies from `get-shit-done` and the foremost repositories from the `awesome-claude-code` ecosystem.

The primary goals are:
1. Eradicate context rot via Spec-Driven Development (SDD).
2. Establish strict Bounded Contexts using Domain-Driven Design (DDD).
3. Implement an autonomous execution loop with circuit breakers.
4. Enforce a "Non-Commit Policy" where only the L2 Quality Gate can modify the main branch.

## 2. Integration Strategies for Core Dependencies

### 2.1 Extensible Command Registry (`pranftw/aiter`)
*   **Strategy:** Decouple orchestration logic from execution. Develop a dynamic plugin loader that registers Bounded Context commands explicitly.
*   **Implementation:** Commands will spawn specific L1 Pipeline Orchestrators rather than injecting all skills into the global L0 context.

### 2.2 State Persistence and Telemetry (`ryoppippi/ccusage`)
*   **Strategy:** Maintain conversation history, token usage, and caching metrics locally in `.jsonl` format.
*   **Implementation:** The L0 Universal Agent Workflow will parse this telemetry via an MCP server to self-regulate iteration budgets and halt loops if token burn exceeds predefined thresholds.

### 2.3 Dependency Graph and Spec-Driven Memory (`steveyegge/beads`)
*   **Strategy:** Replace conversational chat logs with a version-controlled SQL database (Dolt) that maps a strict task hierarchy (Epics -> Sub-tasks).
*   **Implementation:** Agents will exclusively communicate via terse markdown specifications (`PLAN.md`, `STATE.md`). The "Compaction" engine will enforce semantic memory decay, leaving only high-level summaries of completed tasks in the active context window.

### 2.4 Autonomous Execution Engine (`frankbria/ralph-claude-code`)
*   **Strategy:** The L3 Task Executors will sit "on the loop, not in it."
*   **Implementation:** Enforce a dual-condition exit gate (requiring both natural language completion indicators and a structured `EXIT_SIGNAL: true` payload). Hard circuit breakers will trigger after three consecutive loops with zero file modifications or five consecutive identical standard errors.

### 2.5 Multi-Agent Swarm Orchestration (`MaTriXy/claude-swarm-orchestration`)
*   **Strategy:** Agents communicate via structured JSON inboxes.
*   **Implementation:** L1 Orchestrators will dispatch `plan_approval_request` to L2 Task Reviewers. Parallel L3 Task Executors (e.g., UI vs. Backend) will emit `idle_notification` to sync before the Opus Quality Gate executes integration tests.

## 3. Backlog Repository Extraction
*   **`jeffallan/claude-skills`:** Implement a `/common-ground` command at the L0 initialization phase to surface hidden assumptions and align the project vision.
*   **`trailofbits/skills`:** Isolate static analysis (CodeQL/Semgrep) entirely within the L2 Task Reviewer boundary.
*   **`jawwadfirdousi/agent-skills`:** Apply strict validation limits and timeouts to all read-only database MCPs to prevent context flooding from massive data dumps.
*   **`ThibautMelen/agentic-workflow-patterns`:** Standardize the Master-Clone Architecture, ensuring all L3 instances are instantiated from a pristine, immutable base prompt.

## 4. Skill Selection Methodology
To ensure high performance and strict adherence to the L0-L3 hierarchy, skills from the current repository will be selected based on the following strict criteria:

### Criteria 1: Progressive Disclosure Compliance
The skill must rely on a lean `SKILL.md` file (strictly `< 500 lines`). Complex logic, especially abstract syntax tree parsing, must be offloaded to executable Python/Bash scripts within a `scripts/` subdirectory. These scripts must return clear, deterministic standard error strings for the agent to auto-correct.

### Criteria 2: L0-L3 Hierarchy Compatibility
The skill must clearly map to the current architecture:
*   **L0 (Universal Agent Workflow):** Initializes Bounded Contexts, queries the Code Digital Twin (CDT), and triggers the `/common-ground` alignment.
*   **L1 (Pipeline Orchestrator):** Manages domain-specific routing. Generates the initial spec and assigns it via the `beads` dependency graph.
*   **L2 (Task Reviewer):** The strict Quality Gate. It performs variant analysis and security linting. *Crucial:* It is the only agent with Git commit authority.
*   **L3 (Task Executor, Test Executor, Task Rework):** Non-committing code generators. They execute the failing test (Agentic TDD), write minimal logic, and iterate based on local compiler errors.

### Criteria 3: Negative Trigger Optimization
The skill must utilize YAML frontmatter containing explicit instructions on when *not* to use the skill (e.g., restricting Python formatters from executing within a Vue Bounded Context). This prevents the orchestrator from hallucinating capabilities.

### Criteria 4: Deterministic Output and Spec-Driven Development (SDD)
Skills such as `advanced-evaluation`, `context-optimization`, and `cross-skill` must prioritize SDD standards. Output must be high-density markdown, completely devoid of verbosity or conversational pleasantries.

## 5. Selection Results (Initial Pass)
Based on the current repository (`Agent-Skills-for-Context-Engineering`), the following skills are immediately selected for the core suite integration:
1.  **`universal-agent-workflow`** (L0 Orchestrator base)
2.  **`pipeline-orchestrator`** (L1 Domain Router)
3.  **`task-reviewer`** (L2 Quality Gate - holds commit rights)
4.  **`task-executor`** (L3 Code Generator)
5.  **`test-executor`** (L3 TDD Operator)
6.  **`task-rework`** (L3 Bug Fixer)
7.  **`context-optimization`** (Compaction engine for semantic decay)
8.  **`filesystem-context`** (Basis for the Code Digital Twin physical layer)
