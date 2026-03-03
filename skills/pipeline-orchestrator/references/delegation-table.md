# Delegation Table Reference

Extended routing logic for the Pipeline Orchestrator. Covers escalation paths, parallel delegation, and edge case handling.

## Primary Routing Matrix

| Story Status | Story Category | Assigned Agent | Expected Output State |
|-------------|----------------|----------------|-----------------------|
| `Todo` | Feature implementation | `task-executor` | Uncommitted code changes |
| `Todo` | Test suite creation | `test-executor` | Uncommitted test files |
| `Todo` | Infrastructure change | `task-executor` | Uncommitted config changes |
| `Todo` | Epic requiring breakdown | `story-executor` | New child stories in `kanban_board.md` |
| `In Progress` | (any) | — | Monitor; escalate if stale > 30 min |
| `To Review` | (any) | `task-reviewer` | `Done` or `To Rework` decision |
| `To Rework` | (any) | `task-rework` | Back to `To Review` |
| `Done` | (any) | — | Archive; no further action |

## Escalation Paths

### Stale Story (In Progress > 30 minutes)
1. Log a `⚠️ STALE` annotation in kanban_board.md
2. Delegate the story to `task-reviewer` for a partial review
3. If reviewer confirms partial progress: split into two stories (`Done` part + new `Todo`)
4. If reviewer finds no progress: reset to `Todo` and re-delegate

### Rework Loop Detected (3+ rework cycles)
1. Mark the story with `🔴 LOOP-DETECTED`
2. Escalate to human review — do not re-delegate automatically
3. Document the repeated rejection reasons in the story comments

### Dependency Blocking
If Story B depends on Story A and A is not `Done`:
1. Mark B with `🔒 BLOCKED: STORY-A-ID`
2. Prioritize Story A in the next delegation cycle
3. Re-evaluate B only after A reaches `Done`

## Parallel Delegation Rules

The orchestrator may delegate multiple independent stories simultaneously when:
- Stories have no shared file dependencies
- Stories are assigned to different L3 workers
- Total active delegations ≤ 3 concurrent

Stories sharing the same files must be serialized. The orchestrator maintains a `file_lock_registry` in memory during each session to prevent concurrent writes to the same file.

## Story Type Classification

The orchestrator classifies incoming tasks using these heuristics:

| Keywords in Story Title/Description | Classification |
|------------------------------------|----------------|
| "implement", "add", "create", "build" | Feature implementation |
| "test", "spec", "coverage", "suite" | Test creation |
| "fix", "bug", "error", "regression" | Bug fix (routes to task-executor) |
| "refactor", "cleanup", "rename" | Refactoring |
| "port", "migrate", "convert" | Migration (often uses cross-skill-porter) |
| "audit", "review", "analyze" | Analysis (routes to reviewer variant) |
| "epic", "initiative", "milestone" | Requires story-executor decomposition |

## Board State Machine

```
                    ┌─────────────────┐
                    │      TODO       │
                    └────────┬────────┘
                             │ delegate to executor
                             ▼
                    ┌─────────────────┐
                    │   IN PROGRESS   │
                    └────────┬────────┘
                             │ executor signals completion
                             ▼
                    ┌─────────────────┐
                    │   TO REVIEW     │◄───────────────────┐
                    └────────┬────────┘                    │
                             │                             │
              ┌──────────────┴──────────────┐             │
              │ approved                    │ rejected     │
              ▼                             ▼             │
     ┌─────────────────┐         ┌─────────────────┐      │
     │      DONE       │         │   TO REWORK     │      │
     └─────────────────┘         └────────┬────────┘      │
                                          │ rework complete│
                                          └───────────────┘
```

No story may skip a state. Any attempt to transition directly from `In Progress` to `Done` must be rejected and the story must enter `To Review`.
