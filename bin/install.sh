#!/usr/bin/env bash
# AI Workflow Skills — Installer
# Usage: bash bin/install.sh [flags]
#
# Flags:
#   --claude-local    Install slash commands to ./.claude/commands/workflow/
#   --claude-global   Install slash commands to ~/.claude/commands/workflow/
#   --gemini-local    Port skills to Gemini format in ./.gemini/
#   --gemini-global   Port skills to Gemini format in ~/.gemini/
#   --all             Install to all detected runtimes
#   --help            Show this help

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMMANDS_SRC="$REPO_ROOT/commands/workflow"
PORTER="$REPO_ROOT/skills/cross-skill/scripts/cross_skill_porter.py"

print_usage() {
  grep '^#' "$0" | sed 's/^# *//' | tail -n +2
}

install_claude() {
  local target="$1"
  local dest="$target/commands/workflow"
  mkdir -p "$dest"
  cp -r "$COMMANDS_SRC/"* "$dest/"
  echo "✓ Slash commands installed to: $dest"
  echo "  Available: /workflow:orchestrate  /workflow:plan  /workflow:execute"
  echo "             /workflow:review       /workflow:rework /workflow:test"
  echo "             /workflow:port         /workflow:progress /workflow:quick"
}

install_gemini() {
  local target="$1"
  if ! command -v python3 &>/dev/null; then
    echo "✗ python3 not found — required for Gemini skill portation" >&2
    return 1
  fi
  mkdir -p "$target"
  echo "  Porting skills to Gemini CLI format (this may take a moment)..."
  python3 "$PORTER" --batch "$REPO_ROOT/skills" --output-dir "$target"
  echo "✓ Gemini skills installed to: $target"
  echo "  Install with: gemini extensions install $target/<skill-name>-ported/"
}

if [[ $# -eq 0 ]]; then
  print_usage
  exit 0
fi

INSTALL_CLAUDE_LOCAL=false
INSTALL_CLAUDE_GLOBAL=false
INSTALL_GEMINI_LOCAL=false
INSTALL_GEMINI_GLOBAL=false

for arg in "$@"; do
  case "$arg" in
    --claude-local)  INSTALL_CLAUDE_LOCAL=true ;;
    --claude-global) INSTALL_CLAUDE_GLOBAL=true ;;
    --gemini-local)  INSTALL_GEMINI_LOCAL=true ;;
    --gemini-global) INSTALL_GEMINI_GLOBAL=true ;;
    --all)
      INSTALL_CLAUDE_LOCAL=true
      INSTALL_CLAUDE_GLOBAL=true
      INSTALL_GEMINI_LOCAL=true
      ;;
    --help) print_usage; exit 0 ;;
    *)
      echo "Unknown flag: $arg" >&2
      print_usage
      exit 1
      ;;
  esac
done

$INSTALL_CLAUDE_LOCAL  && install_claude "$(pwd)/.claude"
$INSTALL_CLAUDE_GLOBAL && install_claude "$HOME/.claude"
$INSTALL_GEMINI_LOCAL  && install_gemini "$(pwd)/.gemini"
$INSTALL_GEMINI_GLOBAL && install_gemini "$HOME/.gemini"

echo ""
echo "Installation complete."
