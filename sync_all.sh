#!/usr/bin/env bash
# Sync MCP data from this repo's servers.json to Cursor / Codex / Claude Code.
# 1) Cursor: symlink → .cursor updates when data source updates.
# 2) Codex: generate mcp.generated.toml and merge into config.toml (marked block only; rest unchanged).
# 3) Claude Code: merge mcpServers into ~/.claude.json (no overwrite of other keys).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[1/3] Sync Cursor (symlink)"
mkdir -p ~/.cursor
ln -sf "$SCRIPT_DIR/servers.json" ~/.cursor/mcp.json

echo "[2/3] Sync Codex (generate TOML)"
python3 "$SCRIPT_DIR/sync_mcp.py"

echo "[3/3] Sync Claude Code (merge into ~/.claude.json)"
if [ -f "$SCRIPT_DIR/sync_claude.py" ]; then
  python3 "$SCRIPT_DIR/sync_claude.py"
else
  echo "sync_claude.py not found; skip Claude."
fi

echo "Done."
