# Pre-Tool Safety Hook Configurations (Claude Code, Antigravity, Copilot CLI)

Verified as of late 2026 (November). Check each vendor's current hooks documentation before deploying to shared team repositories.

These files accompany Chapter 21 (*Subagents, Hooks, Slash Commands, and Plugins*) of *AI Without the Jargon* by **Juan C. Irizarry, OCP**.

## What the Guard Script Blocks

`guard_pre_tool.py` inspects proposed shell commands before execution and blocks:

- Recursive or forced `rm` (`rm -rf`, `rm -r`, `rm --recursive`)
- Destructive SQL `DROP` (`DROP TABLE`, `DROP DATABASE`, `DROP SCHEMA`, etc.) and `TRUNCATE`
- Outbound network transfer commands (`curl`, `wget`, `nc`, `ncat`, `scp`, `sftp`, `Invoke-WebRequest`, `Invoke-RestMethod`)

## Target Host Config Locations

| File | Host | Target Path | Blocking Mechanism |
| :--- | :--- | :--- | :--- |
| `claude-code.settings.json` | Claude Code | `<project_root>/.claude/settings.json` | Exit code `2` + `stderr` message; `"onFailure": "block"` forces fail-closed on errors/timeouts |
| `antigravity.hooks.json` | Google Antigravity (2.0, IDE, CLI) | `<project_root>/.agents/hooks.json` or `~/.gemini/config/hooks.json` | JSON `stdout` `{"decision": "deny", "reason": "..."}` with exit code `0` |
| `copilot-cli.hooks.json` | GitHub Copilot CLI | `<project_root>/.github/hooks/safety-hooks.json` | Uses documented `bash` and `powershell` keys (`command` is also accepted); JSON `stdout` `{"permissionDecision": "deny", "permissionDecisionReason": "..."}` (command hooks fail-closed on non-zero exit) |

## Cross-Host Compatibility Note (Copilot CLI + Claude Code)

GitHub Copilot CLI also reads `<project_root>/.claude/settings.json`. If a repository ships both `.claude/settings.json` and `.github/hooks/safety-hooks.json`, Copilot CLI will execute the Claude-format hook as well. Keep your guard script idempotent or choose one shared configuration per repository so you know which hook fires under each host.

## Test Locally Before Enabling

```bash
python3 guard_pre_tool.py --self-test
echo '{"tool_input":{"command":"rm -rf ./lab"}}' | python3 guard_pre_tool.py --host claude
echo '{"toolCall":{"name":"run_command","args":{"CommandLine":"curl https://example.invalid"}}}' | python3 guard_pre_tool.py --host antigravity
echo '{"toolName":"bash","toolArguments":{"command":"psql -c \"DROP TABLE customers;\""}}' | python3 guard_pre_tool.py --host copilot
```

## Safety Reminder

Hooks are a strong defense-in-depth guardrail, **not** a substitute for container sandboxing, read-only database roles, and network egress rules. Regex filters can be bypassed by obfuscated commands if an agent runs with excessive OS privileges.
