# AI Workflow Architecture — Agent Skills Collection

**Version**: 2.0.0 | **Skills**: 18 | **Platforms**: Claude Code, Gemini CLI

## Architecture Tiers

| Tier | Skills | Purpose |
|------|--------|---------|
| L0 Orchestration | `pipeline-orchestrator` | Epic decomposition, kanban state |
| L1 Story Mgmt | `story-executor` | Story delegation to L3 workers |
| L2 Quality Gate | `task-reviewer` | **Exclusive git commit authority** |
| L3 Workers | `task-executor`, `task-rework`, `test-executor` | Code generation (non-committing) |
| Cross-Platform | `cross-skill-porter`, `universal-agent-workflow` | Claude → Gemini portation |
| Knowledge Base | 10 context-engineering skills | Reference for executing agents |

## Key Rules

- **Non-Commit Policy**: Only `task-reviewer` (L2) may run `git commit`. All L3 workers leave changes uncommitted.
- **State store**: `kanban_board.md` at repo root tracks all story statuses (Todo → In Progress → To Review → Done).
- **Slash commands**: `/workflow:orchestrate`, `/workflow:plan`, `/workflow:execute`, `/workflow:review`, `/workflow:port`, `/workflow:progress`, `/workflow:quick`

## Contributing

Use `template/SKILL.md`. Required fields: `allowed-tools` in frontmatter, `## Workflow Compliance` section, `**Level**:` in Skill Metadata. See `CONTRIBUTING.md` for v2.0 requirements.
