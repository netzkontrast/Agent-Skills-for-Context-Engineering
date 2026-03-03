# Tool Mapping Reference: Claude Code ↔ Gemini CLI

This reference defines the authoritative bidirectional mapping between Claude Code tool identifiers (PascalCase) and Gemini CLI tool identifiers (snake_case). Used by the Cross-Skill Porter during Phase 3 permission inversion.

## Core Tool Translation Table

| Claude Code (PascalCase) | Gemini CLI (snake_case) | Security Class | Architectural Role |
|--------------------------|-------------------------|----------------|--------------------|
| `Read` | `read_file` | Safe | Elementary read tool. Enables file content extraction into context. Absence blocks all code analysis. |
| `Write` | `write_file` | Destructive | Creates new files or fully overwrites existing content. Must be blocked in audit-only skills. |
| `Edit` | `edit_file` | Moderate | In-place file modification. Safer than Write for targeted changes. |
| `Grep` | `search_file_content` | Safe | High-speed pattern matching across directory trees. Critical for L1 orchestrators during codebase exploration. |
| `Glob` | `glob` | Safe | File path discovery by wildcard patterns. Essential for structural auditors and migration scripts. |
| `Bash` | `execute_script` | Highest Risk | Executes arbitrary OS commands in the host shell. Enables CI/CD pipelines and test execution. Must be explicitly whitelisted. |
| `WebFetch` | `web_fetch` | Moderate | Retrieves HTTP content from external URLs. Network access carries data exfiltration risk in sandboxed environments. |
| `WebSearch` | `web_search` | Moderate | Executes internet search queries. Requires outbound network connectivity. |
| `TodoWrite` | `write_todo` | Safe | Manages structured task checklists in agent memory. Core to the universal workflow state-tracking paradigm. |
| `NotebookEdit` | `edit_notebook` | Moderate | Modifies Jupyter notebook cells. Domain-specific; block if project has no notebooks. |

## Complete Gemini Native Tool Set

The following is the authoritative list of all Gemini CLI native tools. This list is used as the universe `U` in the permission inversion formula:

```
excludeTools = U - translate(allowed-tools)
```

```
read_file
write_file
edit_file
search_file_content
glob
execute_script
web_fetch
web_search
write_todo
edit_notebook
```

## Permission Inversion Algorithm

### Claude Code Philosophy: Zero-Trust Whitelist
Everything is forbidden unless explicitly listed in `allowed-tools`. This is a **Deny by Default** model.

### Gemini CLI Philosophy: Frictionless Autonomy Blacklist
Everything is permitted unless explicitly listed in `excludeTools`. This is an **Allow by Default** model.

### Inversion Calculation

Given a Claude skill with:
```yaml
allowed-tools: Read Grep Glob
```

The porter computes:

1. Translate allowed tools: `{read_file, search_file_content, glob}`
2. Compute excluded: `U - {read_file, search_file_content, glob}`
3. Result: `excludeTools: [write_file, edit_file, execute_script, web_fetch, web_search, write_todo, edit_notebook]`

This guarantees the Gemini agent cannot perform operations that were forbidden in the original Claude specification.

## MCP Tool Exception

MCP (Model Context Protocol) tools follow the naming convention:
```
mcp__<server-name>__<operation>
```

Examples:
- `mcp__postgres__query`
- `mcp__stripe__create_charge`
- `mcp__figma__get_component`

**These identifiers must never be modified.** MCP tools are cross-platform by design — they are defined by the external MCP server, not the CLI platform. Translating them to snake_case would destroy the binding to the external server protocol.

MCP tools are also not included in the `excludeTools` computation — they are governed separately through the `mcpServers` manifest configuration.

## Security Classification Guide

When deciding whether to permit `execute_script` in a ported skill:

| Scenario | Recommendation |
|----------|---------------|
| Read-only code audit | Block: `execute_script` in excludeTools |
| CI/CD orchestration | Permit: remove `execute_script` from excludeTools |
| Test execution | Permit: remove `execute_script` from excludeTools |
| Documentation generation | Block: unnecessary capability for docs tasks |
| Project scaffolding | Permit with review: scaffolding requires file and shell access |

## Version History

| Version | Change |
|---------|--------|
| 1.0.0 | Initial tool mapping table |
| 1.0.0 | Added MCP exception documentation |
| 1.0.0 | Defined complete Gemini native tool set |
