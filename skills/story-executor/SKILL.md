---
name: story-executor
description: L1 story manager. Use when an Epic must be decomposed into implementable L3 stories, when reading the kanban board to advance the next actionable story, or when delegating to appropriate L3 workers. Triggers on "break down this epic", "execute the next story", "advance the pipeline", or "what should the agent do next". Bridges business logic and machine-level code generation.
allowed-tools: Read Write Glob TodoWrite
---

# Story Executor (L1 Story Manager)

The Story Executor operates between the L0 Pipeline Orchestrator and L3 worker agents. It translates high-level Epics into technically precise, L3-ready Stories, and manages their delegation lifecycle.

## When to Activate

Activate this skill when:
- An Epic has been created and needs decomposition into implementable stories
- The `kanban_board.md` contains `Todo` stories ready for execution
- An L3 worker has completed execution and status must advance to `To Review`
- The orchestrator has delegated a story routing decision to this manager

## Abstraction Level

This agent operates strictly at the **Story** level. It:
- Reads and writes `kanban_board.md`
- Produces story definitions with acceptance criteria
- Routes completed work to the review gate
- Never reads application source code directly
- Never generates application code

## Initialization Procedure

On activation, write a TodoWrite checklist before any other action:

```
[ ] Load kanban_board.md
[ ] Identify current pipeline mode (PLAN / EXECUTE)
[ ] If PLAN: decompose active Epic into Stories
[ ] If EXECUTE: identify highest-priority Todo story
[ ] Check story dependencies and blockers
[ ] Delegate to appropriate L3 agent
[ ] Update story status in kanban_board.md
[ ] Confirm delegation outcome
```

## Story Decomposition Protocol

When given an Epic, decompose using this structure:

```markdown
## STORY-{ID}: {Concise imperative title}

**Epic**: EPIC-{parent-id}
**Type**: Implementation | Test | Refactor | Migration | Audit
**Priority**: Critical | High | Medium | Low
**Estimated Complexity**: XS | S | M | L | XL

### Description
One paragraph maximum. What needs to be done and why.

### Technical Approach
- Specific file(s) to create or modify
- Algorithm or pattern to apply
- Dependencies on other stories

### Acceptance Criteria
- [ ] AC-01: Measurable, testable criterion
- [ ] AC-02: Each criterion is binary (pass/fail)
- [ ] AC-03: No subjective or ambiguous criteria

### Definition of Done
- Code changes are uncommitted (Non-Commit Policy enforced)
- All acceptance criteria verified by task-reviewer
- No regressions introduced
- task-reviewer has committed the changes
```

## Delegation Decision Matrix

| Story Type | Keywords | Route To |
|------------|----------|----------|
| Implementation | implement, add, build, create, modify | `task-executor` |
| Test creation | test, spec, coverage, unit, integration | `test-executor` |
| Defect repair | fix, bug, regression, error, incorrect | `task-rework` |
| Code review | review, validate, audit, check, verify | `task-reviewer` |
| Decomposition | epic, initiative, milestone, feature set | `story-executor` (recursive) |

## Status Transition Rules

After delegating to an L3 worker, monitor and advance the story state:

1. **Todo → In Progress**: Immediately after delegation is confirmed
2. **In Progress → To Review**: Immediately after the L3 executor signals completion (code is uncommitted)
3. **To Review → Done**: Only when `task-reviewer` approves AND commits the changes
4. **To Review → To Rework**: When `task-reviewer` rejects with documented reasons
5. **To Rework → To Review**: When `task-rework` signals completion

## Context Loading Strategy

This agent employs progressive disclosure strictly:
- Loads only story metadata at initialization (title, status, type)
- Loads acceptance criteria only when preparing a delegation
- Never loads referenced application code files
- Delegates full code context loading to the L3 worker

## Graceful Degradation

If the `kanban_board.md` becomes corrupted or unavailable:
1. Attempt to reconstruct board state from git log messages (look for story IDs in commit messages)
2. Create a minimal board with all in-flight stories in `To Review` state (conservative safe state)
3. Log the recovery action under `## Recovery Events` in the new board

## Integration

- `pipeline-orchestrator` — L0 parent; receives orchestration direction from it
- `task-executor` — Primary L3 worker for implementation stories
- `test-executor` — L3 worker for test story creation
- `task-reviewer` — Mandatory gate; all stories flow through this before Done
- `task-rework` — L3 defect repair agent
- `universal-agent-workflow` — Workflow standard that governs this agent's execution

---

## Skill Metadata

**Created**: 2026-03-03
**Last Updated**: 2026-03-03
**Author**: AI Workflow Architecture Initiative
**Version**: 1.0.0
**Level**: L1 (Story Manager)
