# Contributing to Agent Skills for Context Engineering

Thank you for your interest in contributing to this collection of Agent Skills for Context Engineering. This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Issues

If you find errors, unclear explanations, or missing topics, please open an issue with:
- A clear description of the problem
- The skill and section where the issue was found
- Suggested improvements if you have them

### Submitting Changes

For substantive changes, please:

1. Fork the repository
2. Create a feature branch for your changes
3. Make changes following the skill template structure
4. Ensure SKILL.md files remain under 500 lines
5. Add references or scripts as appropriate
6. Submit a pull request with a clear description of changes

### Adding New Skills

When adding new skills:

1. Use the template in `template/SKILL.md`
2. Follow naming conventions (lowercase with hyphens)
3. Include both SKILL.md and appropriate references/scripts
4. Update the root README.md to include the new skill
5. Ensure content is platform-agnostic (works across Cursor, Claude Code, etc.)

## Skill Structure Requirements (v2.0)

Each skill must include:

- YAML frontmatter with `name`, `description`, **and `allowed-tools`** fields
- Clear sections with logical organization
- Practical examples where appropriate
- Integration notes linking to related skills
- `## Workflow Compliance` section (see template)
- `## Skill Metadata` section with `**Level**:` field

**Mandatory v2.0 frontmatter fields:**
```yaml
---
name: skill-name
description: >
  Third-person trigger phrases. Starts with skill category
  ("Reference knowledge skill" | "L3 implementation worker" | etc.)
allowed-tools: Read Glob  # minimum for reference; expand for execution skills
---
```

**Mandatory v2.0 `## Workflow Compliance` section** (insert before `## Skill Metadata`):
```markdown
## Workflow Compliance

This skill conforms to the [universal-agent-workflow](../universal-agent-workflow/SKILL.md) standard:
- **Level**: [L0 | L1 | L2 | L3 | Reference]
- **Allowed tools**: [matches frontmatter]
- **Non-Commit Policy**: [Enforced | Not applicable]

When ported by `cross-skill-porter` to Gemini CLI:
`excludeTools: [computed inverse of allowed-tools in snake_case]`
```

**Level classifications:**

| Level | Examples | Code Access | Commit Access |
|-------|----------|-------------|---------------|
| L0 | pipeline-orchestrator | ✗ | ✗ |
| L1 | story-executor | ✗ | ✗ |
| L2 | task-reviewer | ✓ Read | ✓ Exclusive |
| L3 | task-executor, task-rework, test-executor | ✓ Full | ✗ |
| Reference | knowledge skills, cross-skill-porter | ✓ Read | ✗ |

**Tool name mapping** (Claude PascalCase → Gemini snake_case for `excludeTools` computation):
`Read→read_file`, `Write→write_file`, `Edit→edit_file`, `Grep→search_file_content`,
`Glob→glob`, `Bash→execute_script`, `WebFetch→web_fetch`, `WebSearch→web_search`,
`TodoWrite→write_todo`, `NotebookEdit→edit_notebook`

Optional additions:

- `references/` directory with additional documentation
- `scripts/` directory with executable examples
- Multiple markdown files for complex skills

## Content Guidelines

### Writing Style

- Be direct and precise
- Use technical terminology appropriately
- Include specific guidance, not vague recommendations
- Provide concrete examples
- Point out complexity and trade-offs

### Avoiding Platform Specificity

Skills should work across agent platforms. Avoid:
- Platform-specific tool names without abstraction
- Vendor-locked examples
- Features specific to one agent product

### Keeping Skills Focused

Each skill should have a single focus. If a topic grows too large, consider splitting into multiple skills with clear dependencies.

## Code of Conduct

This project follows a professional, technical collaboration model. Be respectful of different perspectives and focus on improving the collective knowledge base.

## Questions

For questions about contributing, please open an issue for discussion.



*Note: For comprehensive documentation on the system architecture and workflow, please refer to [docs/architecture_and_usage.md](docs/architecture_and_usage.md).*
