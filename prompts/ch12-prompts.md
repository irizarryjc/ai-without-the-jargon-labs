# Chapter 12 Prompt Toolkit: Terminal Coding Agents

Copy-ready prompts from Chapter 12 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Investigate Only, Do Not Edit

**Use it when:** You open a terminal agent inside an unfamiliar repository or before a risky change and want a strictly read-only diagnosis first.

```text
Investigate <file_or_directory> in READ-ONLY mode. Do NOT edit files, install
packages, or run write commands.
Answer these four questions using only what you observe in the repository:
1. Where is <bug_or_behavior> defined and called? Cite exact file paths and line numbers.
2. What external commands, files, or environment variables does it depend on?
3. What are the top three failure modes or safety risks?
4. What minimal, reversible change would fix it, and how would we test it in a lab?
```

**What good output looks like:** Exact file paths, line references, concrete failure modes, and a clean `git status` showing zero modified files.

**Safety note:** Pair this prompt with Plan mode or read-only sandbox settings (`--permission-mode dontAsk` or `--sandbox read-only`) so the tool enforces read-only behavior even if a file contains unexpected text.

---

## 2. Headless CI Lint and Format Audit (Read-Only JSON)

**Use it when:** You want to run a non-interactive terminal agent inside a CI check or local pre-commit wrapper to report style or safety issues without editing code automatically.

```text
Inspect the staged diff or target path <target_path> without modifying any files.
Check for:
1. Hardcoded secrets, tokens, IP addresses, or connection strings.
2. Unvalidated external inputs, unquoted shell variables, or string-concatenated SQL.
3. Missing error handling or missing syntax/unit checks.

Return concise findings grouped by severity (high, medium, low) with exact file
path, line number, one-sentence explanation, and suggested fix. Do not edit files
or run commands that change repository state.
```

**What good output looks like:** Deterministic, compact findings (paired with `--output-format json` or `--json`) that a CI job can parse and post as a pull-request comment.

**Safety note:** Never pass raw secrets or production dumps through CI logs, and always lock headless runs with read-only permissions or `--permission-mode dontAsk`.

---

## 3. Shell-Script Hardening Review

**Use it when:** You maintain Bash or PowerShell operations scripts in a lab repository and want a defensive review before running them anywhere important.

```text
Review the lab operations script at <script_path> like a senior Linux systems
engineer. Do NOT execute the script.
Check for:
1. Missing strict mode (`set -euo pipefail` in Bash) or unhandled command failures.
2. Unquoted variables, unsafe glob expansion, or dangerous `rm`/`find -delete` defaults.
3. Missing argument validation, path-traversal risks, or hardcoded hostnames/secrets.
4. Lack of a `--dry-run` option or clear exit codes.

Propose a hardened version and list the risk of each change plus exact syntax
and dry-run verification commands; do not assume it will run without review.
```

**What good output looks like:** Specific line-by-line fixes (quoting, input validation, `--dry-run` default) plus `bash -n` and `shellcheck` verification commands.

**Safety note:** Test hardened scripts only inside a disposable lab directory or container with synthetic files before promoting to staging.

---

## 4. Conventional Commit-Message Writer From `git diff`

**Use it when:** You finished reviewing and testing edits on your feature branch and want a crisp, accurate commit message grounded strictly in the actual diff.

```text
Read ONLY the staged git diff (`git diff --cached`) in <project_root> without
modifying any files.
Draft a concise Conventional Commit message:
- Subject line under 72 characters (`type(scope): summary`).
- Short body (3 to 5 bullet points) stating what changed, why, and which tests ran.
- Explicitly note if any configuration, schema, or CLI flag changed.
Do not invent tests that were not run or files not present in the diff.
```

**What good output looks like:** A clean, factual commit message you can verify in five seconds and pass to `git commit` yourself.

**Safety note:** Always run `git diff --cached` yourself to confirm no `.env` files, keys, or unintended edits are staged before committing.
