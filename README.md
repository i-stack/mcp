# MCP 配置同步

本仓库用**一份** `servers.json` 作为数据源，**同时**同步到 **Cursor**、**Codex** 与 **Claude Code**，避免在多个工具里重复维护 MCP 列表。

## 功能概览

| 目标 | 同步方式 | 说明 |
|------|----------|------|
| **Cursor** | 符号链接 | `~/.cursor/mcp.json` → 本仓库的 `servers.json`，改源文件即生效 |
| **Codex** | 生成 TOML + 合并 | 写入 `~/.codex/mcp.generated.toml`，并把 `[mcp_servers.*]` 合并进 `~/.codex/config.toml` 中带标记的区块，**不覆盖**你在该文件中的其他设置 |
| **Claude Code** | JSON 合并 | 将 `mcpServers` 合并进 `~/.claude.json`，**仅更新** MCP 相关键，其它配置保留 |

一次执行 `sync_all.sh` 即可完成上述三步。

## 环境要求

- macOS / Linux（需 `bash`）
- Python 3（用于 Codex / Claude 同步脚本）

## 快速开始

1. 克隆本仓库并进入目录。

2. 准备本地配置（勿提交密钥）：

   ```bash
   cp servers.json.example servers.json
   ```

   编辑 `servers.json`，填入你的 Token、项目 ID 等。

3. 执行同步：

   ```bash
   chmod +x sync_all.sh   # 仅需首次
   ./sync_all.sh
   ```

4. 重启或重新加载 **Cursor / Codex / Claude Code**（若当前会话未自动读取新配置）。

## 脚本说明

| 文件 | 作用 |
|------|------|
| `sync_all.sh` | 一键：Cursor 软链 → `sync_mcp.py` → `sync_claude.py` |
| `sync_mcp.py` | 从 `servers.json` 生成 Codex 用 TOML，并合并进 `config.toml` |
| `sync_claude.py` | 将 `mcpServers` 合并进 `~/.claude.json` |
| `servers.json` | **唯一数据源**（本地文件，已加入 `.gitignore`） |
| `servers.json.example` | 无密钥的模板，可安全提交到 Git |

也可单独运行：

```bash
python3 sync_mcp.py
python3 sync_claude.py
```

单独执行 `sync_mcp.py` 时仍会更新 Codex 侧配置；Cursor 需自行保证 `~/.cursor/mcp.json` 指向本仓库的 `servers.json`（或直接运行 `sync_all.sh`）。

## 蓝湖 MCP（可选）

`lanhu-mcp/` 为蓝湖相关 MCP 服务实现，需单独按目录内说明启动服务；`servers.json` 中通过 `url` 指向本地 HTTP 端点即可，与上述同步逻辑独立。

## 安全提示

- 勿将含真实 Token 的 `servers.json` 提交到远程仓库。
- 若密钥曾泄露，请在对应平台**轮换** Token。
