Activate the `cross-skill-porter` skill (Cross-Platform Migration Tool).

Arguments: $ARGUMENTS  (path to source skill directory, or --batch <directory>)

You are the Cross-Skill Porter. Convert the Claude Code skill(s) at $ARGUMENTS to Gemini CLI format:

1. Write a TodoWrite checklist as your first action.
2. Run the 5-phase pipeline:
   - Phase 1: Detect source platform, extract Intermediate Representation
   - Phase 2: Generate `gemini-extension.json` manifest (kebab-case name, settings for env vars,
     `"sensitive": true` for credential vars)
   - Phase 3: Invert permissions (`allowed-tools` whitelist → `excludeTools` blacklist)
     Tool mapping: Read→read_file, Write→write_file, Edit→edit_file, Grep→search_file_content,
     Glob→glob, Bash→execute_script (MCP tools preserved verbatim)
   - Phase 4: Translate paths (`${CLAUDE_PLUGIN_ROOT}` → `${extensionPath}`), copy CLAUDE.md → GEMINI.md,
     remove `allowed-tools` from output SKILL.md frontmatter
   - Phase 5: Validate output, generate `TEST_RESULTS.md`

3. Output is written to `<source-dir>-ported/` — source files are never modified.

Execute: `python skills/cross-skill/scripts/cross_skill_porter.py $ARGUMENTS`

For the full operational specification, load: `skills/cross-skill/SKILL.md`
