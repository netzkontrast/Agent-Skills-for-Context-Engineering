# Porting Pipeline Architecture Reference

This reference documents the internal design of the Cross-Skill Porter's 5-phase pipeline, including the Intermediate Representation (IR) schema and phase-by-phase data flow.

## Pipeline Overview

```
Source Directory
      │
      ▼
┌─────────────────────────────────┐
│  Phase 1: Detection & Extraction│  → Intermediate Representation (IR)
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  Phase 2: Manifest Generation   │  → gemini-extension.json scaffold
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  Phase 3: Permission Inversion  │  → excludeTools array computed
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  Phase 4: File Generation       │  → Output directory written
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  Phase 5: Validation & Report   │  → TEST_RESULTS.md
└─────────────────────────────────┘
      │
      ▼
  <source>-ported/ directory
```

## Intermediate Representation (IR) Schema

The IR is a platform-agnostic in-memory structure populated during Phase 1 and consumed by Phases 2–4.

```python
@dataclass
class IntermediateRepresentation:
    name: str              # Extension/plugin name
    version: str           # SemVer string
    description: str       # Human-readable description
    skills: list[SkillRecord]      # All discovered SKILL.md files
    mcp_servers: list[dict]        # MCP server configurations
    env_vars: list[str]            # All ${VAR} placeholders found
    context_file_path: Path | None # Path to CLAUDE.md if present
    context_file_content: str      # Content of CLAUDE.md
    source_platform: str           # "claude" | "gemini"

@dataclass
class SkillRecord:
    source_path: Path      # Absolute path to SKILL.md
    name: str              # Skill name from frontmatter
    description: str       # Skill description from frontmatter
    allowed_tools: list[str]   # Tools from allowed-tools field
    frontmatter_raw: dict  # Full parsed YAML frontmatter
    body: str              # Markdown body (after frontmatter)
```

## Phase 1: Detection Logic

**Claude Code detection** (any condition matches):
1. `.claude-plugin/plugin.json` exists
2. Root `SKILL.md` frontmatter contains `allowed-tools`
3. `CLAUDE.md` exists at directory root

**Gemini CLI detection**:
1. `gemini-extension.json` exists

**Skill discovery**: Recursive `rglob("SKILL.md")` from the source directory root. All SKILL.md files are included, including the root-level one.

## Phase 2: Settings Generation Algorithm

```python
for var_name in ir.env_vars:
    entry = {
        "name": var_name,
        "description": f"Value for {var_name}. Check your configuration...",
        "default": ""
    }
    if regex_matches_sensitive_patterns(var_name):
        entry["sensitive"] = True
```

Sensitive detection regex (case-insensitive):
```
(password|secret|key|token|credential|auth|private|pwd|api_key)
```

## Phase 3: Permission Inversion in Detail

The inversion preserves security boundaries across platform boundaries:

```
SOURCE (Claude whitelist)     →    TARGET (Gemini blacklist)
────────────────────────────────────────────────────────────
allowed-tools: Read Grep       →    excludeTools: [
                                      write_file, edit_file,
                                      execute_script, web_fetch,
                                      web_search, write_todo,
                                      edit_notebook
                                    ]
```

**Edge case: no allowed-tools present**

If a Claude skill has no `allowed-tools` field, it means the skill relies entirely on Claude's default permission prompting. For Gemini, this maps to no `excludeTools` (full autonomy). The report flags this as a manual review item.

**Edge case: `Bash` in allowed-tools**

If the source skill includes `Bash`, the porter translates this to `execute_script` being allowed in Gemini (i.e., removed from excludeTools). This is the highest-risk tool and should be flagged in the report.

**MCP tool preservation rule:**
```python
if tool_name.startswith("mcp__"):
    # Preserve verbatim — never translate
    pass
```

## Phase 4: File Structure Transformation

### Source Layout (Claude)
```
my-skill/
├── .claude-plugin/
│   └── plugin.json
├── CLAUDE.md
├── SKILL.md
└── skills/
    ├── skill-one/
    │   ├── SKILL.md
    │   ├── scripts/
    │   └── references/
    └── skill-two/
        └── SKILL.md
```

### Output Layout (Gemini)
```
my-skill-ported/
├── gemini-extension.json    ← Generated from plugin.json + frontmatter
├── GEMINI.md                ← Copied verbatim from CLAUDE.md
├── TEST_RESULTS.md          ← Validation report
└── skills/
    ├── skill-one/
    │   ├── SKILL.md         ← allowed-tools removed, paths substituted
    │   ├── scripts/
    │   └── references/
    └── skill-two/
        └── SKILL.md
```

### SKILL.md Frontmatter Transformation

**Before (Claude):**
```yaml
---
name: my-skill
description: Does something useful.
allowed-tools: Read Write Glob
---
```

**After (Gemini):**
```yaml
---
name: my-skill
description: Does something useful.
---
```

The `allowed-tools` field is removed. Permission governance moves to `excludeTools` in `gemini-extension.json`.

## Phase 5: Validation Checklist

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Manifest exists | Path.exists() | `gemini-extension.json` present |
| Manifest is valid JSON | json.loads() | No JSONDecodeError |
| No CLAUDE_PLUGIN_ROOT remnants | rglob + string search | Zero occurrences |
| No allowed-tools in SKILL.md | rglob + string search | Zero occurrences |
| All skill bodies non-empty | YAML parse + strip | len(body.strip()) > 0 |
| excludeTools valid identifiers | Set membership | All in ALL_GEMINI_TOOLS |

## Error Handling Philosophy

The porter follows **non-halting error collection**: it records all errors into the report and continues processing. This ensures that one malformed skill does not block the portation of the remaining skills.

After all phases complete, if any validation check failed, the process exits with code 1 and all failures are listed in `TEST_RESULTS.md` under the "Validation Results" section.

## Batch Mode

When invoked with `--batch`, the porter iterates over all subdirectories in the specified parent and runs the full 5-phase pipeline for each. Each subdirectory produces its own `<name>-ported/` output directory and `TEST_RESULTS.md`.

```bash
python cross_skill_porter.py --batch ./skills/
# Produces:
#   skills/context-fundamentals-ported/
#   skills/context-optimization-ported/
#   skills/multi-agent-patterns-ported/
#   ...
```
