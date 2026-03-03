# Roadmap for the Autonomous Claude Suite

This roadmap outlines a structured, 8-week engineering timeline for building the minimal, highly interconnected CLI developer toolkit based on the `get-shit-done` methodology, Spec-Driven Development (SDD), and the Model Context Protocol (MCP).

## Phase 1: Core Scaffolding and Command Registry Infrastructure (Weeks 1-2)

**Objective:** Establish the extensible CLI environment that will house the L0 Universal Agent Workflow, manage state, and intercept user commands.

### Week 1: Framework Initialization
*   **Milestone 1.1:** Initialize a lightweight Node.js or Python CLI framework (structurally similar to `pranftw/aiter`).
*   **Milestone 1.2:** Implement the central Command Registry. Ensure dynamic loading of agent-specific commands to preserve the global context window.
*   **Milestone 1.3:** Scaffold the local `.claude_suite/` directory for environment configurations and `ALLOWED_TOOLS` limits.

### Week 2: State Management and MCP Host Deployment
*   **Milestone 2.1:** Integrate JSONL-based tracking for conversation history, token burn rates, and prompt caching metrics (inspired by `ryoppippi/ccusage`).
*   **Milestone 2.2:** Deploy the central MCP Host client to support multiple transport protocols (STDIO for local file manipulation, HTTP/SSE for external APIs).
*   **Milestone 2.3:** Establish the first set of unit tests for the command parser and local state trackers.

---

## Phase 2: Spec-Driven Memory and Dependency Graph Construction (Weeks 3-4)

**Objective:** Replace standard conversational memory architectures with a Git-backed, version-controlled dependency graph to eradicate context rot.

### Week 3: Database Integration and SDD
*   **Milestone 3.1:** Install and initialize the `steveyegge/beads` CLI framework backed by Dolt.
*   **Milestone 3.2:** Configure the initialization hook (`suite init`) to automatically generate Bounded Context documentation (`AGENTS.md`).
*   **Milestone 3.3:** Configure the L1 Pipeline Orchestrator to output high-density, terse markdown specifications, assigning hash-based IDs for Epics and Sub-tasks.

### Week 4: Compaction and Context Optimization
*   **Milestone 4.1:** Activate the semantic memory decay engine (compaction). Ensure closed tasks are summarized, freeing up token space in the active context window.
*   **Milestone 4.2:** Integrate the `context-optimization` and `filesystem-context` skills from the `Agent-Skills-for-Context-Engineering` repository to manage this decay locally.

---

## Phase 3: Capability Structuring and Skill Linkage (Weeks 5-6)

**Objective:** Structure the suite's capabilities using progressive disclosure and ensure metadata routing strictly follows Domain-Driven Design (DDD).

### Week 5: Progressive Disclosure Implementation
*   **Milestone 5.1:** Enforce the flat hierarchy for all skills within the `skills/` directory. Restrict `SKILL.md` files to `< 500 lines`.
*   **Milestone 5.2:** Offload all fragile or complex logic (e.g., Abstract Syntax Tree parsing) to executable Python or Bash scripts located in `scripts/`.
*   **Milestone 5.3:** Map the L3 `task-executor`, `test-executor`, and `task-rework` skills to these executable environments.

### Week 6: Metadata Routing and Quality Gates
*   **Milestone 6.1:** Write strict YAML frontmatter utilizing positive triggers (third-person imperative) and negative constraints for all core skills.
*   **Milestone 6.2:** Define the explicit boundary for the L2 `task-reviewer` (The Quality Gate). Implement the strict non-commit policy where only the L2 agent possesses Git commit authority.
*   **Milestone 6.3:** Integrate the Code Digital Twin (CDT) MCP server, mapping the physical and conceptual layers of the codebase to empower the L1 and L2 agents with history-sensitive architectural data.

---

## Phase 4: Swarm Orchestration and The Autonomous Loop (Weeks 7-8)

**Objective:** Finalize the automation engine that continuously drives specialized agents through the task graph until the ultimate specification is achieved.

### Week 7: Inter-Agent Communication
*   **Milestone 7.1:** Construct JSON inbox mechanisms for inter-agent communication (`plan_approval_request`, `idle_notification`, `shutdown_request`), modeled on the `TeammateTool` from `MaTriXy/claude-swarm-orchestration`.
*   **Milestone 7.2:** Spawn parallel L3 agents utilizing isolated execution environments (e.g., tmux backends) for execution tasks.
*   **Milestone 7.3:** Implement pre-commit review processes via advanced validation agents to prevent architectural regression during handoffs.

### Week 8: Ralph Loop and Final Delivery
*   **Milestone 8.1:** Wrap the toolkit within the autonomous evaluation loop inspired by the `frankbria/ralph-claude-code` architecture.
*   **Milestone 8.2:** Implement the dual-condition exit gate (requiring high natural language completion indicators AND an explicit `EXIT_SIGNAL: true` payload).
*   **Milestone 8.3:** Activate hard circuit breakers (terminating processes if there are three consecutive loops with no file modifications or five consecutive identical errors).
*   **Milestone 8.4:** Execute the "Landing the Plane" protocol. Ensure no agent shuts down without autonomously running the local test suite, closing tasks in Dolt, and handing over a succinct session summary.
*   **Milestone 8.5:** Finalize documentation and deployment scripts.
