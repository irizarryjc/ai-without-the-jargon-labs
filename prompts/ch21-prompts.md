# Chapter 21 Prompt Toolkit: Subagents, Hooks, Slash Commands, and Plugins

Copy-ready prompts from Chapter 21 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Pre-Tool Safety Hook Policy Generator

**Use it when:** You want a fail-closed `PreToolUse` hook script and host JSON config blocking `rm -rf`, `DROP`, `TRUNCATE`, and outbound network calls tailored to your stack.

```text
Write a fail-closed pre-tool safety hook script in Python 3 and the matching JSON
hook configuration for <Claude Code | Google Antigravity | GitHub Copilot CLI>
(format as of November 2026; note to verify against current vendor docs).

Block these command categories in a LAB repository:
1. Recursive or forced file deletion (`rm -rf`, `rm --recursive`, `Remove-Item -Recurse -Force`).
2. Destructive SQL statements (`DROP`, `TRUNCATE`, `ALTER DATABASE`).
3. Outbound network calls (`curl`, `wget`, `nc`, `scp`, `Invoke-WebRequest`).
4. Any additional project-specific risky command: <extra_command_or_none>

Requirements:
- Wrap stdin JSON parsing in try/except so any script error fails closed (blocks).
- Include a `--self-test` mode testing at least 3 allowed commands and 5 blocked
  commands without executing any shell command.
- Explain the risk of regex bypasses and how to pair this hook with sandboxing;
  do not assume the hook or config will run without review.
```

**What good output looks like:** A clean Python script matching the exact target host's stdin/stdout/exit-code contract, a minimal JSON config, and honest notes on regex limits.

**Safety note:** Test hooks with piped JSON in a disposable lab folder first, and never rely on hooks alone to protect production credentials.

---

## 2. Focused Subagent Brief Template

**Use it when:** You want to define a narrow, read-only custom subagent (`.claude/agents/`, `.github/agents/*.agent.md`, or Antigravity subagent) that investigates cleanly without modifying files.

```text
Draft a reusable READ-ONLY subagent definition for <Claude Code | GitHub Copilot CLI | Google Antigravity>
focused on <subagent_specialty_e.g_log_triage_or_sql_migration_review> in a LAB repo.

Include:
1. Valid YAML frontmatter restricting allowed tools to read/search only (no write,
   edit, or shell execution tools).
2. A concise role statement, exact inputs the subagent should inspect, and explicit
   out-of-scope boundaries.
3. A fixed 6-line summary output format so it returns clean facts to the main
   conversation without bloating context.
4. Explicit stop conditions (when to stop searching and escalate to a human).
Explain the risk of each step and how to verify it; do not assume it will run without review.
```

**What good output looks like:** A tight, copy-ready subagent Markdown file with restricted tool access and a compact output contract that avoids wasting tokens.

---

## 3. Custom Slash Command for Read-Only Code or SQL Review

**Use it when:** You want a manual `/` shortcut that reviews staged diffs or lab SQL migrations against your team's checklist without ever auto-editing files.

```text
Create a manual-only custom slash command named `/<command_name>` (packaged as a
`SKILL.md` with `disable-model-invocation: true` or `.github/prompts/<command_name>.prompt.md`)
that performs a strictly READ-ONLY review of <code_or_sql_migration_type> in a LAB repo.

Checklist items the command must verify:
1. <check_1_e.g_parameterized_queries_or_table_locks>
2. <check_2_e.g_missing_rollback_or_error_handling>
3. <check_3_e.g_hardcoded_secrets_or_unsafe_defaults>

Requirements:
- Forbid editing files or running destructive commands.
- Format findings as a Markdown table: Severity, File/Line, Risk, Suggested Fix,
  and Verification Check.
- End every review reminding the engineer to validate changes in a lab before
  applying; explain the risk of each step and do not assume it will run without review.
```

**What good output looks like:** A short, reusable slash-command file that turns ad-hoc reviews into a consistent, non-destructive safety net.

**Safety note:** Never pass real production dumps or credentials as arguments to a slash command.
