# Chapter 15 Prompt Toolkit: Cloud and Background Agents

Copy-ready prompts from Chapter 15 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Issue-to-Task Description for a Cloud Agent

**Use it when:** You want to turn a rough backlog note into a self-contained issue ready for Codex Cloud, Copilot cloud agent, Cursor Cloud Agents, or Devin.

```text
Turn the rough backlog item below into a self-contained cloud-agent task
description for our LAB repository `<repo_url>`.

Rough request: <short_request>
Target files: <allowed_file_paths>
Verification command: <test_or_lint_command>

Include:
1. Objective (2 sentences).
2. Explicit In-Scope and Out-of-Scope paths (list files that must NOT change).
3. Testable Acceptance Criteria (4 to 5 `WHEN / SHALL` bullets).
4. Constraints (no new third-party dependencies, synthetic lab data only, no secrets).
5. Verification command that must pass before opening the draft PR.
```

**What good output looks like:** A tight, unambiguous GitHub issue that a remote agent can execute without guessing unstated rules.

**Safety note:** Verify the Out-of-Scope list protects CI workflows, `AGENTS.md`, Dockerfiles, and infrastructure configs.

---

## 2. Agent Pull-Request Review Checklist

**Use it when:** A cloud agent opens a draft PR and you want a structured second-pass audit before running local verification.

```text
Review the sanitized agent pull request diff below for `<repo_url>` as a senior
security and operations reviewer. Do NOT approve or merge anything.

Original task scope: <one_line_scope>
Sanitized diff:
<paste_sanitized_git_diff>

Audit and report:
1. Scope creep: files or behaviors changed outside requested scope.
2. Supply chain: added or modified dependencies, scripts, or CI workflows.
3. Test integrity: whether tests genuinely verify failure modes or were weakened.
4. Security & ops risks: unvalidated inputs, unsafe shell/SQL, or stray secrets.
5. Exact local commands to verify this branch before merging; do not assume any
   change will run without review.
```

**What good output looks like:** A line-referenced review highlighting scope creep, suspicious dependencies, or softened assertions in seconds.

**Safety note:** Use only approved enterprise or local tools for proprietary diffs, and verify all findings directly in the raw diff.

---

## 3. Summarize What This Agent Changed and Why

**Use it when:** You open a multi-file background-agent PR and want a fast plain-English orientation before inspecting every hunk.

```text
Read the sanitized diff below from `<branch_name>` and produce a plain-English
briefing for a human reviewer using ONLY facts present in the diff.

Sanitized diff:
<paste_sanitized_git_diff>

Include:
- Overview (under 75 words).
- File-by-file change table (File | What changed | Potential risk).
- Any user-facing CLI, API, or output changes.
- Questions the human reviewer should verify directly in the code.
```

**What good output looks like:** A crisp orientation table that speeds up human review without masking subtle edits.

**Safety note:** Treat the summary strictly as a reading aid; always inspect every modified line yourself before approving.
