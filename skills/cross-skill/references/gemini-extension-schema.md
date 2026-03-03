# Gemini Extension Manifest Schema Reference

This reference documents the complete `gemini-extension.json` schema that the Cross-Skill Porter generates during Phase 2.

## Full Schema

```json
{
  "name": "string (kebab-case, required)",
  "version": "string (semver, required)",
  "description": "string (required)",
  "settings": [
    {
      "name": "ENV_VAR_NAME",
      "description": "Human-readable explanation and where to find the value",
      "default": "",
      "sensitive": true
    }
  ],
  "excludeTools": [
    "write_file",
    "execute_script"
  ],
  "mcpServers": [
    {
      "name": "server-name",
      "command": "npx",
      "args": ["-y", "@scope/mcp-server", "--flag"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  ]
}
```

## Field Specifications

### `name` (required)
- **Format**: kebab-case only (lowercase, hyphens, alphanumeric)
- **Role**: Acts as the namespace prefix for all tools and slash commands this extension exposes
- **Example**: `"context-engineering-collection"`
- **Validation**: Cross-Skill Porter enforces kebab-case conversion automatically

### `version` (required)
- **Format**: Semantic Versioning (SemVer) `MAJOR.MINOR.PATCH`
- **Source**: Copied from the Claude `plugin.json` metadata version field
- **Default when absent**: `"1.0.0"`

### `description` (required)
- **Format**: Free text, one to three sentences
- **Source**: Copied from Claude SKILL.md frontmatter or plugin.json metadata.description
- **Recommendation**: Focus on high-level purpose; avoid procedural detail

### `settings` (optional)
Generated automatically from discovered `${ENV_VAR}` placeholders in MCP configurations.

Each entry:
- **`name`**: Exact environment variable name (SCREAMING_SNAKE_CASE)
- **`description`**: Where the user can find this value; should reference specific UI locations
- **`default`**: Pre-filled value if applicable; empty string for secrets
- **`sensitive`**: Boolean. When `true`, Gemini CLI masks terminal input and routes the stored value through the OS-native keychain (e.g., macOS Keychain, Windows Credential Manager, Linux Secret Service)

**Sensitive variable heuristics** (any match triggers `sensitive: true`):
```
password, secret, key, token, credential, auth, private, pwd, api_key
```

### `excludeTools` (optional)
Array of Gemini native tool identifiers that the agent is **forbidden** from using.

This is the inverse of Claude's `allowed-tools` whitelist. The Cross-Skill Porter computes:
```
excludeTools = ALL_GEMINI_TOOLS - translate(allowed-tools)
```

When absent from the manifest, the Gemini agent has access to all native tools (full autonomy mode).

### `mcpServers` (optional)
Array of MCP server configurations. Copied verbatim from the Claude source.

The `${CLAUDE_PLUGIN_ROOT}` path variable in `args` arrays is replaced with `${extensionPath}` during Phase 4 path translation.

## Installation Flow

When a user runs:
```bash
gemini extensions install ./my-extension/
```

Gemini CLI:
1. Reads `gemini-extension.json`
2. For each entry in `settings`, prompts the user interactively
3. Stores sensitive values in the OS keychain
4. Stores non-sensitive values in the extension configuration file
5. Registers `excludeTools` in the agent's permission model
6. Loads MCP servers defined in `mcpServers`

## Comparison: Claude vs Gemini Manifest

| Feature | Claude `plugin.json` | Gemini `gemini-extension.json` |
|---------|---------------------|-------------------------------|
| Tool permissions | `allowed-tools` in SKILL.md (whitelist) | `excludeTools` in manifest (blacklist) |
| Environment variables | Exported by developer before CLI start | `settings` array → interactive install prompts |
| Sensitive secrets | Developer manages export | OS keychain via `"sensitive": true` |
| Path variable | `${CLAUDE_PLUGIN_ROOT}` | `${extensionPath}` |
| Context file | `CLAUDE.md` | `GEMINI.md` |
| Skill location | Anywhere in directory | `skills/<name>/SKILL.md` |

## Development Testing

Use `gemini extensions link` to test a locally developed extension without packaging:
```bash
cd ./my-extension-ported/
gemini extensions link .
```

This mounts the extension in the active CLI session. Open the debug console (F12) to verify:
- Tools appear with correct names
- Slash commands are registered
- `excludeTools` restrictions are applied
- MCP server connections are established
