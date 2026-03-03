---
name: skill-name
description: >
  [Third person. Trigger phrases the agent will match. E.g.: "Use when the user asks to 'do X',
  'implement Y', or mentions Z. Triggers on 'keyword1', 'keyword2'."]
allowed-tools: Read Glob  # adjust: Reference skills use Read Glob; L3 workers add Write Edit Grep Bash TodoWrite
---

# Skill Name

Provide a clear, concise description of what this skill covers and when to use it. This description
appears in skill discovery and should help agents (and humans) determine when this skill is relevant.

**Important**: Keep the total SKILL.md body under 500 lines for optimal performance. Move detailed
reference material to separate files in the `references/` directory.

## When to Activate

Describe specific situations, tasks, or contexts where this skill should be activated. Include both
direct triggers (specific keywords or task types) and indirect signals.

Write in third person. The description is injected into the system prompt, and inconsistent
point-of-view can cause discovery problems.

- Good: "Processes Excel files and generates reports"
- Avoid: "I can help you process Excel files"

## Core Concepts

Explain the fundamental concepts covered by this skill. Only add context the model does not
already have. Challenge each sentence:
- "Does the model really need this explanation?"
- "Does this paragraph justify its token cost?"

## Detailed Topics

### Topic 1

Provide detailed explanation of the first major topic. Include specific techniques, patterns, or
approaches. Use examples to illustrate concepts.

### Topic 2

Continue with additional topics as needed.

For longer topics, consider moving content to `references/` and linking:
- See [detailed reference](./references/topic-details.md) for complete implementation

## Practical Guidance

Provide actionable guidance. Match specificity to fragility:
- **High freedom**: Multiple valid approaches exist
- **Medium freedom**: Preferred pattern exists, variation acceptable
- **Low freedom**: Fragile sequence — must be followed exactly

## Examples

```
Input: [describe input]
Output: [show expected output]
```

## Guidelines

1. Guideline with specific, verifiable criteria
2. Guideline with clear success conditions

## Integration

List related skills as plain text (not links) to avoid cross-directory reference issues:
- skill-name-one — Brief description of relationship
- skill-name-two — Brief description of relationship

## References

Internal reference (use relative path to this skill's own files):
- [Reference Name](./references/reference-file.md) — Description

Related skills in this collection:
- skill-name — Relationship description

External resources:
- Research papers, documentation, or guides

---

## Workflow Compliance

This skill conforms to the [universal-agent-workflow](../universal-agent-workflow/SKILL.md) standard:
- **Level**: [L0 | L1 | L2 | L3 | Reference] — choose one; see universal-agent-workflow for definitions
- **Allowed tools**: [matches the `allowed-tools` frontmatter field]
- **Non-Commit Policy**: [Enforced (L3 workers) | Not applicable (reference/orchestration skills)]

When ported by `cross-skill-porter` to Gemini CLI:
`excludeTools: [ALL_GEMINI_TOOLS minus your allowed-tools, translated to snake_case]`

## Skill Metadata

**Created**: [Date]
**Last Updated**: [Date]
**Author**: [Author or Attribution]
**Version**: [Version number]
**Level**: [L0 | L1 | L2 | L3 | Reference]
