---
name: ai-workflow-architecture
description: Master collection integrating context engineering knowledge with a standardized AI workflow architecture. Use when building production AI agent systems, implementing cross-platform skill portation (Claude Code → Gemini CLI), orchestrating multi-agent development pipelines, or establishing quality-gated workflows with the Non-Commit Policy. Activates on "build an agent system", "port skills to Gemini", "set up the workflow pipeline", "orchestrate agent tasks", or any request related to structured AI-assisted software development.
allowed-tools: Read Write Glob Bash TodoWrite
---

# AI Workflow Architecture — Agent Skills Collection

This collection merges two complementary disciplines: **context engineering knowledge** (the science of how LLMs use information) and **standardized AI workflow architecture** (the engineering of how agents should execute work in production pipelines).

## Architecture Overview

The collection is organized around the **Universal Agent Workflow** — a three-paradigm framework governing how all skills in this collection operate:

```
┌─────────────────────────────────────────────────────────────────┐
│                  UNIVERSAL AGENT WORKFLOW                       │
│                                                                 │
│  Paradigm 1: Abstraction Hierarchy (L0 → L3)                   │
│  Paradigm 2: Mandatory State Tracking (TodoWrite checklists)    │
│  Paradigm 3: Non-Commit Policy + Definition of Done             │
└─────────────────────────────────────────────────────────────────┘
          ▼                    ▼                    ▼
   L0 Orchestration    Knowledge Layer      Cross-Platform Port
   L1 Story Mgmt.     (Context Eng.)        (Claude → Gemini)
   L2 Quality Gate
   L3 Workers
```

## Skill Map

### Tier 1: Workflow Execution Layer (New in v2.0)

The operational backbone of the AI workflow. These skills implement the universal workflow standard and enable autonomous, quality-gated software development.

| Skill | Level | Role |
|-------|-------|------|
| `pipeline-orchestrator` | L0 | Decomposes requirements into Epics/Stories; manages kanban_board.md |
| `story-executor` | L1 | Translates Epics into L3-ready implementation stories |
| `task-reviewer` | L2 | Quality gatekeeper; **exclusive commit authority** |
| `task-executor` | L3 | Implements code changes (non-committing) |
| `task-rework` | L3 | Repairs reviewer-rejected implementations |
| `test-executor` | L3 | Creates test suites (non-committing) |

**Bootstrap sequence** (port in this order for cross-platform migration):
`pipeline-orchestrator` → `task-reviewer` → `story-executor` → `task-executor` + `task-rework` + `test-executor`

### Tier 2: Cross-Platform Migration (New in v2.0)

| Skill | Role |
|-------|------|
| `cross-skill-porter` | 5-phase autonomous pipeline for Claude Code → Gemini CLI portation |
| `universal-agent-workflow` | The binding standard for all skill authoring and execution |

**The Cross-Skill Porter** implements:
- Phase 1: Platform detection and IR extraction
- Phase 2: `gemini-extension.json` manifest generation with secure settings
- Phase 3: Permission inversion (`allowed-tools` whitelist → `excludeTools` blacklist)
- Phase 4: Path translation (`${CLAUDE_PLUGIN_ROOT}` → `${extensionPath}`)
- Phase 5: Mathematical validation and `TEST_RESULTS.md` report

**Tool name mapping** (Claude PascalCase → Gemini snake_case):
`Read→read_file`, `Write→write_file`, `Edit→edit_file`, `Grep→search_file_content`, `Glob→glob`, `Bash→execute_script`

### Tier 3: Context Engineering Knowledge Base (Original Collection)

Reference skills consulted by executing agents during pipeline operations:

**Foundational:**
- `context-fundamentals` — Context window anatomy, attention mechanics, progressive disclosure
- `context-degradation` — Lost-in-middle, context poisoning, clash, confusion patterns

**Operational:**
- `context-compression` — Tokens-per-task optimization, structured summarization, probe evaluation
- `context-optimization` — KV-cache, observation masking, context partitioning

**Architectural:**
- `multi-agent-patterns` — Supervisor, swarm, hierarchical patterns; context isolation
- `memory-systems` — Temporal knowledge graphs, vector stores, file-system-as-memory
- `tool-design` — Consolidation principle, MCP integration, tool naming conventions

**Methodology:**
- `project-development` — Task-model fit, staged pipeline architecture, structured output
- `evaluation` — Multi-dimensional rubrics, LLM-as-judge patterns
- `advanced-evaluation` — Pairwise comparison, position bias mitigation, production evaluation

**Filesystem-Based Context**
The filesystem provides a single interface for storing, retrieving, and updating effectively unlimited context. Key patterns include scratch pads for tool output offloading, plan persistence for long-horizon tasks, sub-agent communication via shared files, and dynamic skill loading. Agents use `ls`, `glob`, `grep`, and `read_file` for targeted context discovery, often outperforming semantic search for structural queries.

**Hosted Agent Infrastructure**
Background coding agents run in remote sandboxed environments rather than on local machines. Key patterns include pre-built environment images refreshed on regular cadence, warm sandbox pools for instant session starts, filesystem snapshots for session persistence, and multiplayer support for collaborative agent sessions. Critical optimizations include allowing file reads before git sync completes (blocking only writes), predictive sandbox warming when users start typing, and self-spawning agents for parallel task execution.

**Tool Design Principles**
Tools are contracts between deterministic systems and non-deterministic agents. Effective tool design follows the consolidation principle (prefer single comprehensive tools over multiple narrow ones), returns contextual information in errors, supports response format options for token efficiency, and uses clear namespacing.

### Paradigm 1: Abstraction Hierarchy

No agent crosses its level boundary. L0/L1 agents never touch source files. L3 agents never commit. This creates focused, token-efficient execution at every level.

### Paradigm 2: Mandatory State Tracking

Every executing skill writes a TodoWrite checklist as its first action. Steps are marked `in_progress` before executing and `completed` immediately after. External state prevents context drift across long pipelines.

### Paradigm 3: Non-Commit Policy

L3 workers generate code but never commit. Only `task-reviewer` (L2) has commit authority, and only after full checklist validation. This enforces a mandatory four-eyes principle on all AI-generated code.

## Cross-Platform Strategy

This collection is designed to be portable between Claude Code and Gemini CLI. The `cross-skill-porter` automates the conversion using a non-destructive pipeline (output always in `<dirname>-ported/`).

**Why port to Gemini CLI:**
- 63.8% SWE-bench Verified accuracy
- 1M+ token context windows for massive codebase analysis
- Superior execution speed for rapid iteration
- Native multimodality

The `universal-agent-workflow` standard ensures that ported skills behave identically on both platforms, preserving security boundaries and quality gates regardless of the execution environment.

## Quick Start

### Start a new workflow pipeline:
Invoke `pipeline-orchestrator` with your requirements. It will initialize `kanban_board.md` and orchestrate the full development cycle autonomously.

### Port an existing Claude skill to Gemini:
```bash
python skills/cross-skill/scripts/cross_skill_porter.py ./my-skill-directory
```

### Learn about context engineering:
Start with `context-fundamentals`, then `context-degradation`, then follow the architectural skills based on your system requirements.

## Integration

All skills reference each other through the workflow architecture:
- Knowledge skills are consulted by executing agents
- Workflow agents delegate upward and downward through defined levels
- `cross-skill-porter` makes the entire collection portable
- `universal-agent-workflow` is the binding standard for everything

## References

**Workflow Skills:**
- [universal-agent-workflow](skills/universal-agent-workflow/SKILL.md)
- [pipeline-orchestrator](skills/pipeline-orchestrator/SKILL.md)
- [story-executor](skills/story-executor/SKILL.md)
- [task-reviewer](skills/task-reviewer/SKILL.md)
- [task-executor](skills/task-executor/SKILL.md)
- [task-rework](skills/task-rework/SKILL.md)
- [test-executor](skills/test-executor/SKILL.md)
- [cross-skill-porter](skills/cross-skill/SKILL.md)

**Knowledge Skills:**
- [context-fundamentals](skills/context-fundamentals/SKILL.md)
- [context-degradation](skills/context-degradation/SKILL.md)
- [context-compression](skills/context-compression/SKILL.md)
- [context-optimization](skills/context-optimization/SKILL.md)
- [multi-agent-patterns](skills/multi-agent-patterns/SKILL.md)
- [memory-systems](skills/memory-systems/SKILL.md)
- [tool-design](skills/tool-design/SKILL.md)
- [filesystem-context](skills/filesystem-context/SKILL.md)
- [hosted-agents](skills/hosted-agents/SKILL.md)
- [context-optimization](skills/context-optimization/SKILL.md)
- [evaluation](skills/evaluation/SKILL.md)
- [project-development](skills/project-development/SKILL.md)
- [evaluation](skills/evaluation/SKILL.md)
- [advanced-evaluation](skills/advanced-evaluation/SKILL.md)

---

## Skill Metadata

**Created**: 2025-12-20
**Last Updated**: 2026-03-03
**Author**: Agent Skills for Context Engineering Contributors
**Version**: 2.0.0
**Architecture**: Universal Agent Workflow v1.0 — L0/L1/L2/L3 Hierarchy
