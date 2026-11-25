# Read-Only MCP Client Configurations

Format verified as of late 2026 (November). Check each host's current documentation before copying into work environments.

These templates accompany Chapter 18 (*The Model Context Protocol (MCP)*) of *AI Without the Jargon* by **Juan C. Irizarry, OCP**. JSON files intentionally omit synthetic `_comment` keys so strict host schema validators accept them without warnings.

## Included Templates

| File | Host | Target Config Path | Root Key / Format |
| :--- | :--- | :--- | :--- |
| `claude-code.mcp.json` | Claude Code (also portable `.mcp.json`, Cursor `.cursor/mcp.json`, Kiro `.kiro/settings/mcp.json`) | `<project_root>/.mcp.json` | JSON `mcpServers` |
| `vscode.mcp.json` | VS Code with GitHub Copilot | `<project_root>/.vscode/mcp.json` | JSON `servers` (`"type": "stdio"`) |
| `antigravity.mcp_config.json` | Google Antigravity (IDE, 2.0, CLI) | `~/.gemini/config/mcp_config.json` or `<project_root>/.agents/mcp_config.json` | JSON `mcpServers` (`serverUrl` for Streamable HTTP; `url` also accepted) |
| `codex.config.toml` | OpenAI Codex CLI | `~/.codex/config.toml` | TOML `[mcp_servers.<name>]` |

## Version Pinning Note

All templates pin `@modelcontextprotocol/server-filesystem@2.4.0` (verified latest on npm as of November 2026) instead of running an unpinned package. Check npm periodically for newer security releases and update your pin deliberately.

## Safety Checklist Before Enabling Any MCP Server

1. Replace `<project_root>` and `<mcp_server>` with disposable lab paths only.
2. Start read-only (`--read-only` on the filesystem server; `?mode=ro` on the SQLite lab server).
3. Keep package versions pinned in team projects instead of running unpinned packages blindly.
4. Keep API keys and tokens in environment variables or OAuth flows, never hardcoded in committed JSON or TOML files.
5. Disable unused tools and turn on tool search / deferred loading when connecting more than ~10 tools.
