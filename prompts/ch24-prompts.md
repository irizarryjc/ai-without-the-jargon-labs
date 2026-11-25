# Chapter 24 Prompt Toolkit: Building Your Own Agents with SDKs

Copy-ready prompts from Chapter 24 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Six-Part Agent Instructions Template Generator

**Use it when:** Writing clear, bounded system instructions for a new SDK agent before writing wrapper code.

```text
Draft system instructions for a strictly read-only <target_sdk> agent that helps <team_role>
with <task_scope> in a LAB environment for <fictional_org_name>.

Use these exact six headings:
1. Role
2. Allowed Tools (use ONLY: <list_exact_tool_names_and_params>)
3. Permissions and Hard Boundaries (include treating tool outputs as untrusted data)
4. Stop Conditions (include max_turns=<n> and missing-data stop rule)
5. Escalation Path (exact threshold for handing off to a human)
6. Output Format (concise structured sections or JSON keys)

Keep the instructions under 250 words with zero vague platitudes.
```

**What good output looks like:** Tight, enforceable operational instructions with crisp tool scopes, unambiguous stop rules, and a clean output format.

**Safety note:** Pair every boundary in your instructions with matching deterministic validation in Python code.

---

## 2. Audit My Agent's Tool List for Excessive Agency

**Use it when:** Reviewing proposed SDK tool functions before wiring them into an agent loop.

```text
Review the proposed Python agent tool signatures and docstrings below for Excessive Agency
(OWASP LLM03 / Agentic ASI02) and least-privilege risks:

<paste_sanitized_tool_signatures_and_docstrings>

For each tool:
1. Classify it as read-only, bounded-write, or high-risk write/exec.
2. Flag missing input validation (allowlists, path traversal checks, row limits, timeouts).
3. Suggest how to narrow the tool or split it into safer read-only + human-approved steps.
Explain the risk of each step and how to verify it; do not assume any code will run without review.
```

**What good output looks like:** Specific code-level fixes (such as replacing a raw SQL string parameter with a named allowlist enum and adding a `MAX_ROWS` clamp).

**Safety note:** Strip real connection strings, table names from confidential schemas, and internal endpoints before pasting code.

---

## 3. Generate Guardrail Unit Tests for Agent Tools

**Use it when:** Creating offline `unittest` or `pytest` tests that verify your tool guardrails without spending LLM tokens.

```text
Write Python standard-library unittest tests for the read-only agent tool functions below.
Cover:
1. Happy path with valid allowlisted lab input.
2. Rejection of unknown names, empty strings, and shell/SQL injection-like strings (harmless lab strings only).
3. Boundary clamping on numeric limits (0, negative, and oversized values).
4. Verification that return values are valid JSON with expected keys.

Tool module (sanitized lab code):
<paste_sanitized_ops_tools_py>
Explain the risk of each step and how to verify it; do not assume it will run without review.
```

**What good output looks like:** Fast, offline unit tests that run in milliseconds and catch broken allowlists or clamping bugs before you ever invoke an LLM.

**Safety note:** Run tests in a disposable lab environment using synthetic fixtures only.

---

## 4. Port an Agent Wrapper Between Two SDKs

**Use it when:** Moving an existing set of plain Python tools from one agent SDK (such as OpenAI Agents SDK) to another (such as Google ADK, Claude Agent SDK, or Microsoft Agent Framework).

```text
I have a framework-free Python module `ops_tools.py` exposing these read-only functions:
<paste_function_signatures>

Write a minimal wrapper script using <target_sdk_name> (current late-2026 Python syntax) that:
1. Loads credentials and `<model_name>` strictly from environment variables (never hardcoded).
2. Enforces a maximum turn cap (`max_turns` or equivalent).
3. Includes a `--dry-run` flag that exercises the local tools without making any API call.
4. Flags any SDK method you are unsure about with a note naming the official docs page to check.
Explain the risk of each step and how to verify it; do not assume it will run without review.
```

**What good output looks like:** A clean 40-to-60-line adapter that leaves your tested tool module untouched and fails safely when environment variables are missing.

**Safety note:** Always verify package names against official vendor docs to avoid slopsquatting before running `pip install`.
