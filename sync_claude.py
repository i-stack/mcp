#!/usr/bin/env python3
"""
Merge MCP servers from this repo's mcp-servers.json into Claude Code user config.
Updates only mcpServers; does not overwrite other keys in the config.
Target: ~/.claude.json (user-level MCP for Claude Code).
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SRC = REPO_ROOT / "mcp-servers.json"
CLAUDE_JSON = Path.home() / ".claude.json"


def main():
    if not SRC.exists():
        print(f"Skip Claude sync: {SRC} not found.")
        return
    servers = json.loads(SRC.read_text(encoding="utf-8")).get("mcpServers", {})

    if CLAUDE_JSON.exists():
        data = json.loads(CLAUDE_JSON.read_text(encoding="utf-8"))
    else:
        data = {}

    existing = data.get("mcpServers") or {}
    # Merge: same keys from mcp-servers.json overwrite; other keys in existing stay
    data["mcpServers"] = {**existing, **servers}

    CLAUDE_JSON.parent.mkdir(parents=True, exist_ok=True)
    CLAUDE_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated MCP servers in {CLAUDE_JSON} (merge, no overwrite of other config).")


if __name__ == "__main__":
    main()
