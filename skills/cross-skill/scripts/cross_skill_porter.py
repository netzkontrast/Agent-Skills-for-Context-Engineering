#!/usr/bin/env python3
"""
Cross-Skill Porter: Claude Code → Gemini CLI conversion pipeline.

Implements a non-destructive 5-phase pipeline:
  Phase 1: Semantic detection and source identification
  Phase 2: Manifest generation and variable mapping
  Phase 3: Permission architecture inversion (whitelist→blacklist)
  Phase 4: Context translation and path resolution
  Phase 5: Mathematical validation and report generation

Output is always written to <source-directory>-ported/.
Source files are never modified.
"""

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Tool mapping: Claude PascalCase → Gemini snake_case
# ---------------------------------------------------------------------------

CLAUDE_TO_GEMINI: dict[str, str] = {
    "Read": "read_file",
    "Write": "write_file",
    "Edit": "edit_file",
    "Grep": "search_file_content",
    "Glob": "glob",
    "Bash": "execute_script",
    "WebFetch": "web_fetch",
    "WebSearch": "web_search",
    "TodoWrite": "write_todo",
    "NotebookEdit": "edit_notebook",
}

ALL_GEMINI_TOOLS: list[str] = list(CLAUDE_TO_GEMINI.values())

SENSITIVE_PATTERNS = re.compile(
    r"(password|secret|key|token|credential|auth|private|pwd|api_key)",
    re.IGNORECASE,
)

ENV_VAR_PATTERN = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class SkillRecord:
    """Intermediate representation of a single skill."""
    source_path: Path
    name: str
    description: str
    allowed_tools: list[str]
    frontmatter_raw: dict
    body: str


@dataclass
class IntermediateRepresentation:
    """Platform-agnostic IR extracted from the source directory."""
    name: str
    version: str
    description: str
    skills: list[SkillRecord] = field(default_factory=list)
    mcp_servers: list[dict] = field(default_factory=list)
    env_vars: list[str] = field(default_factory=list)
    context_file_path: Optional[Path] = None
    context_file_content: str = ""
    source_platform: str = "unknown"


@dataclass
class TransformReport:
    """Audit record for the full portation run."""
    source_dir: str
    output_dir: str
    platform_detected: str
    metadata_transforms: list[str] = field(default_factory=list)
    permission_inversion: list[str] = field(default_factory=list)
    path_substitutions: list[str] = field(default_factory=list)
    sensitive_vars: list[str] = field(default_factory=list)
    edge_cases: list[str] = field(default_factory=list)
    validation_results: list[str] = field(default_factory=list)
    success: bool = True


# ---------------------------------------------------------------------------
# Phase 1: Detection
# ---------------------------------------------------------------------------


def parse_yaml_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter delimited by --- markers. Returns (metadata, body)."""
    if not content.startswith("---"):
        return {}, content

    end = content.find("\n---", 3)
    if end == -1:
        return {}, content

    frontmatter_text = content[3:end].strip()
    body = content[end + 4:].lstrip()

    metadata: dict = {}
    for line in frontmatter_text.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            metadata[k.strip()] = v.strip()

    return metadata, body


def detect_source_platform(source_dir: Path) -> str:
    """Return 'claude' or 'gemini' based on directory contents."""
    if (source_dir / ".claude-plugin" / "plugin.json").exists():
        return "claude"
    if (source_dir / "gemini-extension.json").exists():
        return "gemini"
    # Fall back to inspecting SKILL.md frontmatter
    skill_md = source_dir / "SKILL.md"
    if skill_md.exists():
        fm, _ = parse_yaml_frontmatter(skill_md.read_text())
        if "allowed-tools" in fm:
            return "claude"
    return "claude"  # Default to Claude for forward-porting


def collect_skills(source_dir: Path) -> list[SkillRecord]:
    """Discover and parse all SKILL.md files under the source directory."""
    records: list[SkillRecord] = []
    for skill_md in sorted(source_dir.rglob("SKILL.md")):
        content = skill_md.read_text(encoding="utf-8")
        fm, body = parse_yaml_frontmatter(content)
        allowed_raw = fm.get("allowed-tools", "")
        allowed_tools = allowed_raw.split() if allowed_raw else []
        records.append(
            SkillRecord(
                source_path=skill_md,
                name=fm.get("name", skill_md.parent.name),
                description=fm.get("description", ""),
                allowed_tools=allowed_tools,
                frontmatter_raw=fm,
                body=body,
            )
        )
    return records


def extract_env_vars(text: str) -> list[str]:
    """Find all ${VAR_NAME} occurrences in a string."""
    return list(set(ENV_VAR_PATTERN.findall(text)))


def extract_mcp_servers(plugin_json_path: Path) -> tuple[list[dict], list[str]]:
    """Parse plugin.json and return (mcp_servers, discovered_env_vars)."""
    if not plugin_json_path.exists():
        return [], []

    try:
        data = json.loads(plugin_json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return [], []

    servers = data.get("mcpServers", [])
    env_vars: list[str] = []
    raw_text = json.dumps(servers)
    env_vars.extend(extract_env_vars(raw_text))
    return servers, env_vars


def build_ir(source_dir: Path) -> IntermediateRepresentation:
    """Phase 1: Extract all metadata into an Intermediate Representation."""
    platform = detect_source_platform(source_dir)

    # Load plugin metadata
    plugin_json = source_dir / ".claude-plugin" / "plugin.json"
    plugin_data: dict = {}
    if plugin_json.exists():
        try:
            plugin_data = json.loads(plugin_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    # Extract top-level metadata from plugin.json or SKILL.md
    top_skill_md = source_dir / "SKILL.md"
    top_fm: dict = {}
    if top_skill_md.exists():
        top_fm, _ = parse_yaml_frontmatter(top_skill_md.read_text(encoding="utf-8"))

    name = (
        plugin_data.get("metadata", {}).get("name")
        or top_fm.get("name")
        or source_dir.name
    )
    version = plugin_data.get("metadata", {}).get("version", "1.0.0")
    description = (
        plugin_data.get("metadata", {}).get("description")
        or top_fm.get("description")
        or ""
    )

    mcp_servers, env_vars = extract_mcp_servers(plugin_json)
    skills = collect_skills(source_dir)

    # Collect additional env vars from all skill files
    for skill in skills:
        env_vars.extend(extract_env_vars(skill.body))
        env_vars.extend(extract_env_vars(json.dumps(skill.frontmatter_raw)))

    unique_env_vars = sorted(set(env_vars))

    # Context file (CLAUDE.md)
    context_path: Optional[Path] = None
    context_content = ""
    claude_md = source_dir / "CLAUDE.md"
    if claude_md.exists():
        context_path = claude_md
        context_content = claude_md.read_text(encoding="utf-8")

    return IntermediateRepresentation(
        name=name,
        version=version,
        description=description,
        skills=skills,
        mcp_servers=mcp_servers,
        env_vars=unique_env_vars,
        context_file_path=context_path,
        context_file_content=context_content,
        source_platform=platform,
    )


# ---------------------------------------------------------------------------
# Phase 2: Manifest generation
# ---------------------------------------------------------------------------


def to_kebab_case(name: str) -> str:
    """Convert any string to kebab-case."""
    name = re.sub(r"[^a-zA-Z0-9\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    name = re.sub(r"([A-Z])", r"-\1", name).lstrip("-")
    return name.lower()


def build_settings_entry(var_name: str) -> dict:
    """Generate a Gemini settings object for an environment variable."""
    entry: dict = {
        "name": var_name,
        "description": (
            f"Value for {var_name}. Check your project configuration "
            "or cloud console (e.g., GCP Console under IAM, or your CI/CD secrets)."
        ),
        "default": "",
    }
    if SENSITIVE_PATTERNS.search(var_name):
        entry["sensitive"] = True
    return entry


def build_gemini_manifest(ir: IntermediateRepresentation, report: TransformReport) -> dict:
    """Phase 2: Scaffold the gemini-extension.json manifest."""
    kebab_name = to_kebab_case(ir.name)
    if kebab_name != ir.name:
        report.metadata_transforms.append(
            f"Name: '{ir.name}' → '{kebab_name}' (enforced kebab-case)"
        )

    settings = [build_settings_entry(v) for v in ir.env_vars]
    for s in settings:
        if s.get("sensitive"):
            report.sensitive_vars.append(s["name"])

    manifest: dict = {
        "name": kebab_name,
        "version": ir.version,
        "description": ir.description,
    }

    if settings:
        manifest["settings"] = settings

    if ir.mcp_servers:
        manifest["mcpServers"] = ir.mcp_servers

    return manifest


# ---------------------------------------------------------------------------
# Phase 3: Permission inversion
# ---------------------------------------------------------------------------


def translate_tool(tool: str) -> Optional[str]:
    """
    Translate a Claude tool name to its Gemini equivalent.
    MCP tools (mcp__*) are returned unchanged.
    Unknown tools return None.
    """
    if tool.startswith("mcp__"):
        return tool  # Preserve MCP identifiers verbatim
    return CLAUDE_TO_GEMINI.get(tool)


def invert_permissions(allowed_tools: list[str], report: TransformReport) -> list[str]:
    """
    Phase 3: Convert a Claude whitelist into a Gemini blacklist.

    Algorithm:
        excluded = ALL_GEMINI_TOOLS - translate(allowed_tools)
    """
    translated: set[str] = set()
    for tool in allowed_tools:
        mapped = translate_tool(tool)
        if mapped and mapped in ALL_GEMINI_TOOLS:
            translated.add(mapped)
        elif mapped and mapped.startswith("mcp__"):
            pass  # MCP tools are not part of the excludeTools list
        else:
            report.edge_cases.append(
                f"Tool '{tool}' has no Gemini equivalent — skipped in permission inversion."
            )

    excluded = sorted(set(ALL_GEMINI_TOOLS) - translated)

    report.permission_inversion.append(
        f"  Source allowed-tools: {allowed_tools}"
    )
    report.permission_inversion.append(
        f"  Translated allowed:   {sorted(translated)}"
    )
    report.permission_inversion.append(
        f"  All Gemini tools:     {sorted(ALL_GEMINI_TOOLS)}"
    )
    report.permission_inversion.append(
        f"  Computed excludeTools: {excluded}"
    )

    return excluded


# ---------------------------------------------------------------------------
# Phase 4: Path translation and file generation
# ---------------------------------------------------------------------------


def substitute_paths(text: str, report: TransformReport) -> str:
    """Replace ${CLAUDE_PLUGIN_ROOT} with ${extensionPath}."""
    if "${CLAUDE_PLUGIN_ROOT}" in text:
        count = text.count("${CLAUDE_PLUGIN_ROOT}")
        report.path_substitutions.append(
            f"  Replaced {count} occurrence(s) of ${{CLAUDE_PLUGIN_ROOT}} → ${{extensionPath}}"
        )
        text = text.replace("${CLAUDE_PLUGIN_ROOT}", "${extensionPath}")
    return text


def strip_allowed_tools_from_frontmatter(content: str) -> str:
    """Remove the allowed-tools line from YAML frontmatter."""
    lines = content.splitlines(keepends=True)
    in_frontmatter = False
    result = []
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            result.append(line)
            continue
        if in_frontmatter and line.strip() == "---":
            in_frontmatter = False
            result.append(line)
            continue
        if in_frontmatter and line.strip().startswith("allowed-tools"):
            continue  # Drop this line
        result.append(line)
    return "".join(result)


def generate_output(
    ir: IntermediateRepresentation,
    manifest: dict,
    source_dir: Path,
    output_dir: Path,
    report: TransformReport,
) -> None:
    """Phase 4: Write all output files to the output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write gemini-extension.json
    manifest_path = output_dir / "gemini-extension.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    report.metadata_transforms.append("Generated gemini-extension.json")

    # Write GEMINI.md from CLAUDE.md
    if ir.context_file_content:
        gemini_md = output_dir / "GEMINI.md"
        gemini_md.write_text(ir.context_file_content, encoding="utf-8")
        report.metadata_transforms.append("Copied CLAUDE.md → GEMINI.md")
        if len(ir.context_file_content.splitlines()) > 200:
            report.edge_cases.append(
                "WARNING: GEMINI.md exceeds 200 lines. "
                "Consider moving procedural detail into individual skill files."
            )

    # Process and copy skills
    skills_output_root = output_dir / "skills"
    skills_output_root.mkdir(exist_ok=True)

    for skill in ir.skills:
        # Determine relative path of skill inside source_dir
        try:
            rel = skill.source_path.relative_to(source_dir)
        except ValueError:
            rel = Path(skill.name) / "SKILL.md"

        skill_out_dir = output_dir / rel.parent
        skill_out_dir.mkdir(parents=True, exist_ok=True)

        # Build SKILL.md content — strip allowed-tools, substitute paths
        skill_content = skill.source_path.read_text(encoding="utf-8")
        skill_content = strip_allowed_tools_from_frontmatter(skill_content)
        skill_content = substitute_paths(skill_content, report)

        (skill_out_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")

        # Copy companion directories (scripts/, references/, assets/)
        for subdir_name in ("scripts", "references", "assets"):
            src_subdir = skill.source_path.parent / subdir_name
            if src_subdir.exists():
                dst_subdir = skill_out_dir / subdir_name
                shutil.copytree(src_subdir, dst_subdir, dirs_exist_ok=True)
                # Substitute paths in all copied text files
                for fpath in dst_subdir.rglob("*"):
                    if fpath.is_file() and fpath.suffix in {
                        ".py", ".js", ".ts", ".sh", ".md", ".json", ".yaml", ".yml"
                    }:
                        text = fpath.read_text(encoding="utf-8", errors="replace")
                        new_text = substitute_paths(text, report)
                        if new_text != text:
                            fpath.write_text(new_text, encoding="utf-8")

    report.metadata_transforms.append(
        f"Processed {len(ir.skills)} skill(s) into output directory"
    )


# ---------------------------------------------------------------------------
# Phase 5: Validation and report
# ---------------------------------------------------------------------------


def validate_output(output_dir: Path, report: TransformReport) -> None:
    """Phase 5: Run all mathematical validation checks."""
    # Check manifest exists and is valid JSON
    manifest_path = output_dir / "gemini-extension.json"
    if not manifest_path.exists():
        report.validation_results.append("FAIL: gemini-extension.json not found")
        report.success = False
    else:
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            report.validation_results.append("PASS: gemini-extension.json is valid JSON")
            # Check no Claude remnants
            raw = json.dumps(data)
            if "CLAUDE_PLUGIN_ROOT" in raw:
                report.validation_results.append(
                    "FAIL: ${CLAUDE_PLUGIN_ROOT} still present in gemini-extension.json"
                )
                report.success = False
        except json.JSONDecodeError as exc:
            report.validation_results.append(
                f"FAIL: gemini-extension.json is malformed JSON — {exc}"
            )
            report.success = False

    # Check no CLAUDE_PLUGIN_ROOT variables remain anywhere
    remnant_files: list[str] = []
    for fpath in output_dir.rglob("*"):
        if fpath.is_file():
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
                if "${CLAUDE_PLUGIN_ROOT}" in content:
                    remnant_files.append(str(fpath.relative_to(output_dir)))
            except Exception:
                pass

    if remnant_files:
        report.validation_results.append(
            f"FAIL: ${{CLAUDE_PLUGIN_ROOT}} still found in: {remnant_files}"
        )
        report.success = False
    else:
        report.validation_results.append(
            "PASS: No ${CLAUDE_PLUGIN_ROOT} remnants in output"
        )

    # Check no allowed-tools in SKILL.md files
    skill_failures: list[str] = []
    for skill_md in output_dir.rglob("SKILL.md"):
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        if "allowed-tools" in content:
            skill_failures.append(str(skill_md.relative_to(output_dir)))

    if skill_failures:
        report.validation_results.append(
            f"FAIL: 'allowed-tools' still present in SKILL.md files: {skill_failures}"
        )
        report.success = False
    else:
        report.validation_results.append(
            "PASS: All SKILL.md files have 'allowed-tools' removed"
        )

    # Check all skill bodies are non-empty
    empty_skills: list[str] = []
    for skill_md in output_dir.rglob("SKILL.md"):
        fm, body = parse_yaml_frontmatter(skill_md.read_text(encoding="utf-8"))
        if not body.strip():
            empty_skills.append(str(skill_md.relative_to(output_dir)))

    if empty_skills:
        report.validation_results.append(
            f"FAIL: Empty skill bodies found: {empty_skills}"
        )
        report.success = False
    else:
        report.validation_results.append("PASS: All skill bodies are non-empty")


def write_report(report: TransformReport, output_dir: Path) -> None:
    """Write TEST_RESULTS.md to the output directory."""
    status_badge = "✅ SUCCESS" if report.success else "❌ FAILURE"
    lines = [
        f"# Cross-Skill Porter — Transformation Report",
        "",
        f"**Status**: {status_badge}",
        f"**Source**: `{report.source_dir}`",
        f"**Output**: `{report.output_dir}`",
        f"**Platform detected**: {report.platform_detected}",
        "",
        "---",
        "",
        "## Metadata Transformations",
        "",
    ]
    for t in report.metadata_transforms:
        lines.append(f"- {t}")

    lines += [
        "",
        "## Permission Inversion Calculation",
        "",
        "```",
    ]
    lines.extend(report.permission_inversion or ["  (no allowed-tools found in source)"])
    lines += [
        "```",
        "",
        "## Path Variable Substitutions",
        "",
    ]
    if report.path_substitutions:
        lines.extend(f"- {s}" for s in report.path_substitutions)
    else:
        lines.append("- None required")

    lines += [
        "",
        "## Sensitive Variables Detected",
        "",
    ]
    if report.sensitive_vars:
        for v in report.sensitive_vars:
            lines.append(f"- `{v}` → marked `sensitive: true` (OS keychain storage)")
    else:
        lines.append("- None detected")

    lines += [
        "",
        "## Validation Results",
        "",
    ]
    for r in report.validation_results:
        prefix = "✅" if r.startswith("PASS") else "❌"
        lines.append(f"{prefix} {r}")

    lines += [
        "",
        "## Edge Cases Requiring Manual Review",
        "",
    ]
    if report.edge_cases:
        for e in report.edge_cases:
            lines.append(f"⚠️  {e}")
    else:
        lines.append("None — clean portation.")

    report_path = output_dir / "TEST_RESULTS.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Report written to: {report_path}")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def port_directory(source_dir: Path) -> bool:
    """Run the full 5-phase pipeline for a single source directory."""
    output_dir = source_dir.parent / (source_dir.name + "-ported")
    report = TransformReport(
        source_dir=str(source_dir),
        output_dir=str(output_dir),
        platform_detected="",
    )

    print(f"\n[Cross-Skill Porter] Source: {source_dir}")
    print(f"[Cross-Skill Porter] Output: {output_dir}")

    # --- Phase 1 ---
    print("  Phase 1: Detecting source platform and extracting IR...")
    ir = build_ir(source_dir)
    report.platform_detected = ir.source_platform
    print(f"    Detected: {ir.source_platform}, {len(ir.skills)} skill(s), {len(ir.env_vars)} env var(s)")

    # --- Phase 2 ---
    print("  Phase 2: Generating Gemini manifest...")
    manifest = build_gemini_manifest(ir, report)

    # --- Phase 3 ---
    print("  Phase 3: Inverting permission architecture...")
    # Compute union of allowed-tools across all skills
    all_allowed: list[str] = []
    for skill in ir.skills:
        all_allowed.extend(skill.allowed_tools)
    unique_allowed = sorted(set(all_allowed))
    excluded_tools = invert_permissions(unique_allowed, report)
    if excluded_tools:
        manifest["excludeTools"] = excluded_tools

    # --- Phase 4 ---
    print("  Phase 4: Generating output files...")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    generate_output(ir, manifest, source_dir, output_dir, report)

    # --- Phase 5 ---
    print("  Phase 5: Validating output...")
    validate_output(output_dir, report)
    write_report(report, output_dir)

    status = "SUCCESS" if report.success else "FAILURE"
    print(f"\n[Cross-Skill Porter] {status}")
    for result in report.validation_results:
        print(f"  {result}")

    return report.success


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-Skill Porter: Claude Code → Gemini CLI conversion pipeline"
    )
    parser.add_argument(
        "source",
        help="Source skill directory (or use --batch for multiple directories)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Treat SOURCE as a parent directory and port all subdirectories",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    if not source.exists():
        print(f"Error: '{source}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if args.batch:
        subdirs = [d for d in source.iterdir() if d.is_dir() and not d.name.startswith(".")]
        if not subdirs:
            print(f"No subdirectories found in '{source}'.", file=sys.stderr)
            sys.exit(1)
        results = [port_directory(d) for d in subdirs]
        failed = results.count(False)
        print(f"\nBatch complete: {len(results) - failed}/{len(results)} succeeded.")
        sys.exit(0 if failed == 0 else 1)
    else:
        success = port_directory(source)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
