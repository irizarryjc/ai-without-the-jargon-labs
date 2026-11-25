# Chapter 18 Prompt Toolkit: The Model Context Protocol (MCP)

Copy-ready prompts from Chapter 18 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, tokens, hostnames, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Generate a Read-Only MCP Config for `<host>`

**Use it when:** You want a clean, placeholder-based starter MCP configuration file tailored to one host without accidentally enabling write flags.

```text
Generate a minimal READ-ONLY MCP client configuration for <host> (for example,
Claude Code, VS Code with GitHub Copilot, Cursor, Google Antigravity, Codex CLI,
or Kiro) using the verified late-2026 config path and root key for that host.

Server to configure (LAB only): <mcp_server_package_or_command>
Allowed local lab path: <project_root>/lab-docs

Requirements:
1. Enable read-only mode or explicitly note which write tools must be disabled.
2. Use placeholders (<project_root>, <your_api_key>) with zero real secrets.
3. Add a dated comment noting the config format should be verified against current
   official vendor docs.
4. Explain the risk of each setting and how to verify no write tools are exposed;
   do not assume it will run without review.
```

**What good output looks like:** A valid JSON or TOML snippet with the exact host file path, read-only flags set, and a quick checklist to verify connected tools before use.

**Safety note:** Confirm the exact flag names against the server's official README before running, and point only at a disposable lab folder.

---

## 2. Audit an MCP Server's Tool List for Risky Capabilities

**Use it when:** You are evaluating a new MCP server and want to spot scope creep, dangerous write tools, or suspicious tool descriptions before approving it.

```text
Act as an application security reviewer auditing the tool list of an MCP server
against the OWASP MCP Top 10 (beta) before I enable it in a LAB environment.

Server name and source: <mcp_server_name_and_repo>
Exported tool names, descriptions, and JSON Schemas (sanitized):
<paste_tool_list_json>

Return:
1. A table classifying each tool as Read-Only, State-Changing, or High-Risk
   (shell, raw SQL, arbitrary HTTP, file delete).
2. Any suspicious instructions or hidden directives inside tool descriptions
   (potential tool poisoning).
3. Which tools I should disable immediately to follow least privilege.
4. Concrete checks to verify version pinning and sandboxing before running it.
```

**What good output looks like:** A clear risk matrix calling out overly broad tools (like raw shell or write methods) and flagging any imperative phrasing hidden inside descriptions.

**Safety note:** Never paste internal URLs, API tokens, or proprietary schemas when auditing a tool list in an external chat assistant.

---

## 3. Write Clean, Injection-Free MCP Tool Descriptions

**Use it when:** You are authoring your own internal read-only MCP server and want crisp tool docstrings/descriptions that guide models cleanly without leaking secrets or ambiguous scope.

```text
Help me write clean, concise Python MCP SDK (`MCPServer` in v2+ or `FastMCP` in v1.x)
tool docstrings and parameter types for a READ-ONLY LAB MCP server serving <fictional_org>:

Proposed tools:
<list_2_to_4_read_only_functions_and_inputs>

For each tool:
1. Write a 2-sentence docstring stating exact return format, read-only scope,
   and when the model should NOT call it.
2. Keep descriptions free of credentials, internal hostnames, or imperative
   override language.
3. Recommend strict allowlist validation checks to put in the Python handler.

Explain the risk of each exposed parameter and how to verify read-only behavior
with a local self-test; do not assume the code will run without review.
```

**What good output looks like:** Tight, unambiguous `MCPServer`/`FastMCP` tool signatures and docstrings paired with defensive allowlist rules and `stderr`-only audit logging reminders.

**Safety note:** Keep all sample schemas fictional and test locally with `--self-test` or MCP Inspector against disposable lab data first.

---

## 4. Pre-Upgrade "Rug Pull" Diff Review

**Use it when:** An MCP server package or remote endpoint was updated and you want to check whether tool schemas, permissions, or descriptions changed unexpectedly.

```text
Compare these two snapshots of an MCP server's tool definitions (BEFORE and AFTER
an update in a LAB environment):

BEFORE:
<paste_previous_tool_list_json>

AFTER:
<paste_new_tool_list_json>

Identify:
1. Any newly added tools or widened parameter types/enums.
2. Any wording changes in tool descriptions that could alter agent behavior,
   bypass confirmations, or look like tool poisoning.
3. Whether the update is safe to approve as-is, needs specific tools disabled,
   or should stay pinned on the older version.
```

**What good output looks like:** A sharp diff highlighting new write capabilities or subtle wording additions so you catch scope creep or rug pulls before updating.

**Safety note:** Capture tool snapshots in an isolated lab environment before upgrading any MCP server used on daily work machines.
