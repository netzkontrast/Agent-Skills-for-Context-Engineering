# Changelog

All notable changes to this project are documented in this file.

Format: [Semantic Versioning](https://semver.org/). Latest version first.

---

## [2.0.0] — 2026-03-03

### Added — AI Workflow Architecture

**New Workflow Skills (L0–L3 Hierarchy):**
- `pipeline-orchestrator` (L0) — Epic decomposition, kanban_board.md state management, delegation orchestration
- `story-executor` (L1) — Epic-to-story decomposition, L3 worker routing, story lifecycle management
- `task-reviewer` (L2) — Exclusive git commit authority; clean code + acceptance criteria validation
- `task-executor` (L3) — Non-committing implementation worker; minimal-footprint code generation
- `task-rework` (L3) — Defect repair agent; rework loop detection after 3+ iterations
- `test-executor` (L3) — Non-committing test suite creation; risk-based coverage targets

**New Cross-Platform Migration Skills:**
- `cross-skill-porter` — 5-phase autonomous pipeline: detection → extraction → permission inversion
  → path translation → validation. Generates `TEST_RESULTS.md` with full audit trail.
- `universal-agent-workflow` — Binding standard defining the three core paradigms:
  abstraction hierarchy (L0-L3), mandatory state tracking (TodoWrite), Non-Commit Policy.

**New Infrastructure:**
- `commands/workflow/` — 9 Claude Code slash commands:
  `/workflow:orchestrate`, `/workflow:plan`, `/workflow:execute`, `/workflow:review`,
  `/workflow:rework`, `/workflow:test`, `/workflow:port`, `/workflow:progress`, `/workflow:quick`
- `bin/install.sh` — Cross-platform installer (Claude Code local/global, Gemini CLI local/global)
- `package.json` — npm/npx distribution (`npx ai-workflow-skills`)
- `CLAUDE.md` — Root project context loaded at every session start

**Tool Name Mapping (Claude PascalCase → Gemini snake_case):**
`Read→read_file`, `Write→write_file`, `Edit→edit_file`, `Grep→search_file_content`,
`Glob→glob`, `Bash→execute_script`, `WebFetch→web_fetch`, `WebSearch→web_search`,
`TodoWrite→write_todo`, `NotebookEdit→edit_notebook`

### Changed — Existing Skills Ported to v2.0 Standard

All 10 original knowledge skills updated:
- Added `allowed-tools: Read Glob` to YAML frontmatter
- Added `## Workflow Compliance` section with excludeTools mapping for Gemini CLI
- Added `**Level**: Reference` to Skill Metadata
- Updated descriptions to third-person trigger format

Updated files: `marketplace.json` (v2.0.0, 6 plugin groups covering all 18 skills),
`template/SKILL.md` (v2.0 fields), `CONTRIBUTING.md` (v2.0 requirements).

---

## [1.1.0] — 2025-12-26

### Added

- `context-compression` — Context compression strategies with probe-based evaluation framework.
  Covers anchored iterative summarization, opaque compression, regenerative summaries,
  and tokens-per-task optimization metric. Includes `compression_evaluator.py` script.

### Changed

- `tool-design` — Extended with MCP integration patterns and consolidation principle

---

## [1.0.0] — 2025-12-20

### Added — Initial Release

**Foundational Skills:**
- `context-fundamentals` — Context window anatomy, attention mechanics, progressive disclosure
- `context-degradation` — Lost-in-middle, context poisoning, clash, confusion patterns
- `context-optimization` — KV-cache prefix caching, observation masking, context partitioning

**Architectural Skills:**
- `multi-agent-patterns` — Supervisor, swarm, hierarchical patterns; context isolation
- `memory-systems` — Temporal knowledge graphs, vector stores, file-system-as-memory
- `tool-design` — Consolidation principle, tool naming conventions, MCP integration

**Methodology Skills:**
- `project-development` — Task-model fit, staged pipeline architecture, structured output
- `evaluation` — Multi-dimensional rubrics, LLM-as-judge patterns

**Advanced Skills:**
- `advanced-evaluation` — Pairwise comparison, position bias mitigation, production evaluation
