---
name: universal-agent-workflow
description: Foundational workflow standard that governs all agent skills in this collection. Use when designing a new skill, reviewing whether an existing skill follows architectural standards, or understanding the three core paradigms: abstraction hierarchy, mandatory state tracking, and the Non-Commit Policy. Triggers on "what is the standard workflow", "how should skills be structured", "explain the workflow architecture", or "does this skill conform to standards".
allowed-tools: Read Glob TodoWrite
---

# Universal Agent Workflow Standard

This document defines the architectural standards that apply to every skill in this collection — whether manually authored or ported by the `cross-skill-porter`. All skills must conform to these three irreversible paradigms.

## Why This Standard Exists

Modern LLM-based agent systems fail in predictable ways:
1. **Context drift**: Long sessions accumulate irrelevant tokens, diluting model attention
2. **Circular hallucination**: Multi-step tasks produce self-reinforcing logical errors
3. **Unreviewed code injection**: Agents commit code directly without quality gates

This workflow standard eliminates these failure modes through structural enforcement rather than model capability assumptions.

---

## Paradigm 1: Abstraction Hierarchy (L0–L3)

Every skill occupies exactly one level of abstraction. Levels never mix responsibilities.

```
L0 — Meta-Orchestrator (pipeline-orchestrator)
│    Scope: Business requirements → Epics
│    Output: Status assignments, delegation decisions
│    Never: Reads application source code, writes code
│
L1 — Story Manager (story-executor)
│    Scope: Epics → implementable Stories
│    Output: Story definitions with AC, delegation signals
│    Never: Reads application source code, writes code
│
L2 — Quality Gatekeeper (task-reviewer)
│    Scope: Implementation validation and git commits
│    Output: Approval/rejection decisions, committed code
│    Never: Implements features, reworks defects independently
│
L3 — Workers (task-executor, task-rework, test-executor, cross-skill-porter)
     Scope: Physical file creation/modification
     Output: Uncommitted file changes
     Never: Commits to git, orchestrates other agents
```

### Boundary Enforcement Rules

- An L0 agent that reads application source code is violating its boundary
- An L3 agent that commits to git is violating the Non-Commit Policy
- An agent routing work to a peer at the same level without L1/L0 mediation is creating an untracked pipeline
- Skill authors must declare their level in the Skill Metadata section

### Token Efficiency Rationale

The hierarchy ensures each agent loads only the minimal context for its task:
- L0/L1 agents never load file contents — they work with metadata only (100–500 tokens/task)
- L3 agents load only the specific files they modify (1,000–5,000 tokens/task)
- L2 agents load the diff and reference checklists (2,000–8,000 tokens/task)

This hierarchical context partitioning is the primary mechanism for maintaining focus across long-running multi-step pipelines.

---

## Paradigm 2: Mandatory State Tracking

Every skill must externalize its execution state before performing any file operations.

### TodoWrite Initialization

On activation, every skill must write a TodoWrite checklist as its **first action**:

```python
# Pattern — adapt to the skill's actual steps
[
  { "content": "Load story context", "status": "pending" },
  { "content": "Read target files", "status": "pending" },
  { "content": "Execute primary transformation", "status": "pending" },
  { "content": "Verify acceptance criteria", "status": "pending" },
  { "content": "Generate completion report", "status": "pending" },
]
```

Mark each item `in_progress` before starting, `completed` immediately after finishing. Never mark complete in batches — each step is marked individually as the agent works.

### State Transition Sequence

```
[Activation]
     │
     ▼
[Write TodoWrite checklist — ALL steps pending]
     │
     ▼
[Mark step 1 in_progress → Execute → Mark completed]
     │
     ▼
[Mark step 2 in_progress → Execute → Mark completed]
     │
     ...
     ▼
[Mark final step in_progress → Execute → Mark completed]
     │
     ▼
[Signal completion to parent agent]
```

### Why External State Matters

Internal reasoning chains are ephemeral — they exist only within the current context window. By writing state to an external TodoWrite structure, the agent:
- Creates a recoverable checkpoint if the session is interrupted
- Forces a linear execution order that prevents circular reasoning
- Makes progress visible to humans monitoring the pipeline

### Graceful Degradation

If external systems (Jira, Linear, CI APIs) are unavailable:
1. Fall back to `kanban_board.md` as the sole state store
2. Log the degradation event in `kanban_board.md` under `## System Notes`
3. Continue execution — never halt waiting for external system recovery

---

## Paradigm 3: Non-Commit Policy and Definition of Done

### Non-Commit Policy (L3 Agents)

All L3 worker agents (task-executor, task-rework, test-executor, cross-skill-porter) are **forbidden** from executing git commit operations. Workers leave the filesystem in a modified, uncommitted state.

**Permitted git operations for L3 agents:**
- `git diff` — inspect current changes
- `git status` — inspect filesystem state
- `git stash` — temporarily preserve changes (if instructed)

**Forbidden git operations for L3 agents:**
- `git commit`
- `git push`
- `git add` (staging without committing is also forbidden — it implies pending commit)
- `git reset --hard` (destructive without review)

### Commit Authority

The **only** agent authorized to commit is `task-reviewer` (L2). Commit authority cannot be delegated or bypassed.

### Definition of Done (Algorithmic State)

The Definition of Done is a hard algorithmic state, not a subjective assessment. A story is `Done` if and only if all of the following are true:

```
1. task-reviewer has loaded the full modification context ✓
2. All clean_code_checklist.md items: PASS ✓
3. All acceptance criteria: PASS ✓
4. No unresolved side effects detected ✓
5. Side effects extracted as new stories in kanban_board.md ✓
6. git commit executed by task-reviewer with story ID reference ✓
7. kanban_board.md updated to Done status ✓
```

If any item is false, the story is not Done — regardless of how close it appears to be.

### Four-Eyes Principle

Every code change goes through at minimum two agents before reaching `Done`:
1. A worker agent (L3) — creates the change
2. A reviewer agent (L2) — validates and commits the change

This structure is the architectural equivalent of a mandatory code review for all changes, enforced at the agent protocol level rather than by human process compliance.

---

## Skill Authoring Compliance Checklist

When writing or reviewing a skill for inclusion in this collection, verify:

- [ ] YAML frontmatter contains `name`, `description`, `allowed-tools`
- [ ] `description` field triggers correctly (avoid "I" statements; use third-person)
- [ ] Skill body is under 500 lines
- [ ] Level declared in Skill Metadata section (L0/L1/L2/L3)
- [ ] Initialization Procedure includes a TodoWrite checklist
- [ ] Non-Commit Policy is stated explicitly if the skill is L3
- [ ] `allowed-tools` lists only the tools the skill genuinely requires
- [ ] Large reference content is in `references/` files, not inline
- [ ] Integration section lists all connected skills

---

## Platform Portability

This workflow standard is platform-agnostic. When a skill is ported by `cross-skill-porter`:
- The TodoWrite paradigm maps to Gemini's `write_todo` tool
- The `allowed-tools` whitelist inverts to `excludeTools` blacklist
- The Non-Commit Policy is enforced through Gemini's tool permission system
- `kanban_board.md` continues to serve as the fallback state store on both platforms

The universal workflow guarantees deterministic, auditable execution regardless of whether the agent runs in Claude Code or Gemini CLI.

## Integration

All skills in this collection are governed by this standard. Key relationships:

- `pipeline-orchestrator` — L0; enforces the abstraction hierarchy at the top
- `task-reviewer` — L2; holds exclusive commit authority
- `cross-skill-porter` — L3; the primary tool for migrating skills to new platforms
- All other skills — must conform to the three paradigms documented here

---

## Skill Metadata

**Created**: 2026-03-03
**Last Updated**: 2026-03-03
**Author**: AI Workflow Architecture Initiative
**Version**: 1.0.0
**Level**: Reference (non-executing — defines standards for all levels)
