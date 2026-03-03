---
name: cross-skill-porter
description: Use when porting or converting Agent Skills between CLI platforms, specifically from Claude Code to Gemini CLI. Triggers on requests like "port this skill to Gemini", "convert Claude skills", "migrate agent skills cross-platform", "translate allowed-tools to excludeTools", or any cross-platform skill migration. Implements a non-destructive 5-phase pipeline: detection, extraction, transformation, generation, and validation. Output is always placed in a separate <dirname>-ported/ directory.
allowed-tools: Read Write Glob Bash
---

# Cross-Skill Porter

This skill converts Agent Skills between CLI platforms using a strict, non-destructive 5-phase pipeline. The primary direction is Claude Code → Gemini CLI. Original source files are never modified.

## When to Activate

Activate this skill when:
- Porting a Claude Code skill directory to Gemini CLI format
- Translating `allowed-tools` whitelists into Gemini `excludeTools` blacklists
- Converting `${CLAUDE_PLUGIN_ROOT}` path variables to `${extensionPath}`
- Migrating `CLAUDE.md` persona files to `GEMINI.md`
- Scaffolding a `gemini-extension.json` manifest from an existing Claude plugin
- Running batch migrations of skill collections

## Core Principle: Non-Destructive Operation

**Under no circumstances may source files be overwritten, deleted, or modified.**

All output is written into a new directory named `<source-directory-name>-ported/`. This guarantees full rollback capability at all times.

## Five-Phase Pipeline

### Phase 1: Semantic Detection and Source Identification

Scan the target directory to determine the source platform:

**Detected as Claude Code when any of these are present:**
- A `.claude-plugin/` directory containing a `plugin.json`
- A `SKILL.md` file whose YAML frontmatter contains the `allowed-tools` field
- A `CLAUDE.md` file at the directory root

**Detected as Gemini CLI when:**
- A `gemini-extension.json` exists (contains `excludeTools` array)

After detection, extract all metadata into a platform-agnostic Intermediate Representation (IR) with these fields:
```
IR = {
  name, version, description, author,
  skills: [{ path, frontmatter, body }],
  mcpServers: [...],
  envVars: [...],
  allowedTools: [...],
  contextFile: { path, content }
}
```

### Phase 2: Manifest Generation and Variable Mapping

Scaffold the `gemini-extension.json` manifest:

1. **Name field**: Enforce `kebab-case` format. Strip spaces, convert to lowercase, replace special characters with hyphens.
2. **Environment variables**: Scan all MCP server configurations for `${VAR_NAME}` patterns. For each discovered variable, generate a settings entry:
   ```json
   {
     "name": "VAR_NAME",
     "description": "Human-readable description of where to find this value",
     "default": ""
   }
   ```
3. **Sensitive variable detection**: Apply heuristic matching. If the variable name contains any of: `password`, `secret`, `key`, `token`, `credential`, `auth`, `private`, `pwd`, `api_key` — add `"sensitive": true` to force OS keychain storage and terminal masking.

### Phase 3: Permission Architecture Inversion

This is the most critical transformation. Claude Code uses a **whitelist** (allowed-tools); Gemini CLI uses a **blacklist** (excludeTools). The inversion algorithm:

```
EXCLUDED_TOOLS = ALL_GEMINI_NATIVE_TOOLS - TRANSLATED_ALLOWED_TOOLS
```

**Complete Claude → Gemini tool name mapping (PascalCase → snake_case):**

| Claude Code | Gemini CLI | Role |
|-------------|------------|------|
| `Read` | `read_file` | File content extraction |
| `Write` | `write_file` | File creation/overwrite |
| `Edit` | `edit_file` | In-place file modification |
| `Grep` | `search_file_content` | Pattern matching across files |
| `Glob` | `glob` | Path discovery by wildcard |
| `Bash` | `execute_script` | Shell command execution |
| `WebFetch` | `web_fetch` | HTTP content retrieval |
| `WebSearch` | `web_search` | Internet search |
| `TodoWrite` | `write_todo` | Task list management |
| `NotebookEdit` | `edit_notebook` | Jupyter notebook editing |

**Complete list of all Gemini native tools** (used to compute excludeTools):
```
read_file, write_file, edit_file, search_file_content, glob,
execute_script, web_fetch, web_search, write_todo, edit_notebook
```

**MCP Exception Rule**: Tool names that begin with `mcp__` (e.g., `mcp__postgres__query`, `mcp__stripe__charge`) are vendor-bound identifiers. They must be preserved verbatim and must never be snake_case-converted. These tools remain in the Gemini extension's `mcpServers` configuration unchanged.

### Phase 4: Context Translation and Path Resolution

1. **Path variable substitution**: Replace every occurrence of `${CLAUDE_PLUGIN_ROOT}` with `${extensionPath}` across all configuration files and script arguments. Incorrect path resolution causes Gemini runtime crashes.

2. **Persona file migration**: If a `CLAUDE.md` file exists at the source root, copy its entire content verbatim into a new `GEMINI.md` file in the output root. The GEMINI.md must remain concise — if the source CLAUDE.md exceeds 200 lines, emit a warning in the final report.

3. **SKILL.md restructuring**: Move each SKILL.md into `skills/<skill-name>/SKILL.md` within the extension directory. When copying the YAML frontmatter, **remove the `allowed-tools` field entirely** — permission governance is now handled by `excludeTools` in the manifest.

4. **Asset and script preservation**: Copy the `scripts/`, `references/`, and `assets/` subdirectories of each skill verbatim into the corresponding output skill directory.

### Phase 5: Mathematical Validation and Report Generation

Perform a recursive validation of the output directory:

**Mandatory checks:**
- `gemini-extension.json` exists and is syntactically valid JSON
- No `${CLAUDE_PLUGIN_ROOT}` variables remain in any output file
- No `allowed-tools` YAML fields remain in any output SKILL.md
- All skill bodies (Markdown content) are non-empty
- The `excludeTools` array contains only recognized Gemini tool names

**Report generation**: Write a `TEST_RESULTS.md` to the output root documenting:
- Every metadata transformation performed
- The permission inversion calculation (showing source allowed-tools, full tool set, and computed excludeTools)
- All path variable substitutions made
- Flagged edge cases requiring manual review (non-translatable shell scripts, complex multi-endpoint MCP configs)
- Validation pass/fail status for each check

## Execution Procedure

Run `scripts/cross_skill_porter.py` with the target skill directory as the argument. The script executes the full 5-phase pipeline autonomously.

```bash
python scripts/cross_skill_porter.py <source-directory>
# Example:
python scripts/cross_skill_porter.py ./my-claude-skill
# Output: ./my-claude-skill-ported/
```

For batch migration of an entire skill collection:
```bash
python scripts/cross_skill_porter.py --batch ./skills/
```

## Guidelines

1. Never modify, delete, or overwrite source files under any circumstances
2. Always output to `<dirname>-ported/` — never write in-place
3. Preserve MCP tool identifiers verbatim; only translate native Claude/Gemini tools
4. Apply `"sensitive": true` to any setting that matches credential heuristics
5. Remove `allowed-tools` from SKILL.md frontmatter in output; use `excludeTools` in manifest
6. Replace `${CLAUDE_PLUGIN_ROOT}` with `${extensionPath}` in every file
7. Generate `TEST_RESULTS.md` unconditionally after every run
8. Flag edge cases in the report rather than failing silently

## Integration

This skill is the entry point for the cross-platform bootstrapping strategy. After portation, activate the bootstrapped Gemini skills in this sequence:

1. `pipeline-orchestrator` — L0 meta-orchestrator (port first)
2. `task-reviewer` — Quality gatekeeper (port before executors)
3. `story-executor` — L1 delegation manager
4. `task-executor`, `task-rework`, `test-executor` — L3 workers
5. Specialized auditors and project scaffolding tools

## References

- [Tool Mapping Reference](./references/tool-mapping.md) — Complete Claude↔Gemini tool translation table
- [Gemini Extension Schema](./references/gemini-extension-schema.md) — Full gemini-extension.json specification
- [Porting Pipeline Architecture](./references/porting-pipeline.md) — Detailed pipeline design and IR specification

Related skills:
- `pipeline-orchestrator` — First skill to port; governs the migration workflow
- `task-reviewer` — Second skill to port; validates all porting outputs
- `universal-agent-workflow` — Workflow standard injected into every ported skill

---

## Skill Metadata

**Created**: 2026-03-03
**Last Updated**: 2026-03-03
**Author**: AI Workflow Architecture Initiative
**Version**: 1.0.0
