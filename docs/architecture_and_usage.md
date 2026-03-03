# Comprehensive Documentation

## Overview

This repository provides Agent Skills for Context Engineering. It contains a collection of skills combining context engineering knowledge with a standardized AI workflow architecture for building production-grade agent systems. The skills are deployable to Claude Code, Gemini CLI, OpenCode, and Codex.

## Architecture and Workflow

The system uses a Universal Agent Workflow based on three core paradigms:

1. **Abstraction Hierarchy**:
   - **L0 Orchestrator**: `pipeline-orchestrator` handles epic decomposition and state management (`kanban_board.md`).
   - **L1 Story Management**: `story-executor` delegates tasks to L3 workers.
   - **L2 Quality Gate**: `task-reviewer` holds exclusive commit authority and validates criteria.
   - **L3 Workers**: `task-executor`, `task-rework`, `test-executor` implement code without committing.
2. **Mandatory State Tracking**: Skills write TodoWrite checklists. Steps are marked `in_progress` before execution and `completed` immediately after.
3. **Non-Commit Policy**: L3 workers generate code but never commit. Only the L2 `task-reviewer` can commit after validating checklists.

## Platform Agnosticism

The skills apply transferable principles and work across Claude Code, Cursor, and other agent platforms.

The `cross-skill-porter` enables Claude-to-Gemini portation. It is a 5-phase autonomous pipeline:
- Detects the platform and extracts internal representation (IR).
- Generates a `gemini-extension.json` manifest.
- Inverts permissions (converts `allowed-tools` to `excludeTools`).
- Translates paths.
- Validates the migration and outputs `TEST_RESULTS.md`.

## Context Engineering Knowledge Base

The repository includes foundational, operational, and architectural skills for managing the context window effectively:
- **Fundamentals**: Explains attention mechanics and progressive disclosure.
- **Degradation**: Discusses the lost-in-the-middle phenomenon and context poisoning.
- **Compression**: Optimizes tokens-per-task.
- **Multi-Agent Patterns**: Covers supervisor, swarm, and hierarchical patterns.
- **Memory Systems**: Uses the file system as memory (`FILESYSTEM_AS_MEMORY`).
- **Tool Design**: Follows the consolidation principle, reducing complex toolsets.

## Execution via Slash Commands

If installed locally, the following commands trigger workflow operations:
- `/workflow:orchestrate`: Initialize requirements into a Kanban board.
- `/workflow:plan`: Break down epics into implementable L3 stories.
- `/workflow:execute`: Run an L3 implementation task.
- `/workflow:review`: Review implementation and conditionally commit.
- `/workflow:port`: Migrate a Claude Code skill to Gemini.

## Best Practices

When writing new skills:
- Follow the `template/SKILL.md` format.
- Define `allowed-tools` explicitly.
- Keep `SKILL.md` under 500 lines.
- Implement progressive disclosure using the `references/` directory.
- Use explicit instructions and concrete examples instead of generic summaries.
