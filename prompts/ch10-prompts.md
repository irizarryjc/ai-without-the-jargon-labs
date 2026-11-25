# Chapter 10 Prompt Toolkit: VS Code and GitHub Copilot, Step by Step

Copy-ready prompts from Chapter 10 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Explain Unfamiliar Code Line by Line

**Use it when:** You inherit an undocumented script in VS Code and want a clear read-only walkthrough in **Ask** mode before changing anything.

```text
Explain the selected code in <file_path> in plain English for an operations
engineer who did not write it.
Cover:
1. A two-sentence summary of what the code does.
2. A step-by-step walkthrough of the main execution path.
3. Every side effect (files written, network calls, DB queries, env vars, commands).
4. Up to three hidden assumptions or failure modes to check before editing.
Do not modify any files.
```

**What good output looks like:** A concise map of control flow and side effects that flags risky defaults (missing timeouts, unquoted variables) without guessing behavior absent from the file.

**Safety note:** Run in read-only **Ask** mode and verify every claimed side effect against the source file.

---

## 2. Write Focused Unit Tests for Existing Code

**Use it when:** You want to lock in behavior and cover invalid-input edge cases before refactoring a lab script.

```text
I am working in a LAB repository on <file_path> using <test_framework>.
Write unit tests covering:
1. Two normal happy-path inputs.
2. Boundary values (empty strings, zero, negative numbers, upper bounds).
3. Invalid types and malformed inputs that should raise clear errors.
4. Any path, encoding, or null-handling edge cases visible in the code.

Use synthetic lab fixtures only (no real hosts, secrets, or live data).
Explain the risk of each step and how to verify it; do not assume any change
will run without review.
```

**What good output looks like:** Small, isolated test functions with clear assertions that catch real regressions rather than mirroring the implementation blindly.

**Safety note:** Use lab data only; verify assertions fail when you intentionally break the underlying check.

---

## 3. Refactor With Explicit Constraints

**Use it when:** You want **Edit** or **Agent** mode to clean up messy code without altering interfaces or adding dependencies.

```text
Refactor <file_path> to improve readability and input validation while keeping
public function signatures and CLI output format identical.

Constraints:
- Do NOT add third-party packages or change dependencies.
- Keep helper functions under <max_lines> lines with explicit type hints.
- Validate all inputs explicitly and raise clear errors instead of failing silently.
- Show the proposed diff and list any behavioral edge cases before I accept.
Explain the risk of each step and how to verify it; do not assume it will run
without review.
```

**What good output looks like:** A narrow diff touching only the intended file(s), zero unrequested packages, and clear verification steps.

**Safety note:** Start on a clean Git branch, review every changed line, and run your test suite yourself.

---

## 4. Draft a `.github/copilot-instructions.md` File

**Use it when:** You want a concise, accurate repository instructions file grounded in the tools already in your project.

```text
Inspect <project_root> read-only (do not edit files yet) and draft a concise
`.github/copilot-instructions.md` file (under 250 words) tailored to this repo.

Include:
1. Project context (language, runtime versions, target OS).
2. Coding and security standards (input validation, no hardcoded secrets, safe
   command execution and parameterized queries).
3. Exact test, lint, and syntax-check commands present in this repository.
4. Files or directories the agent must never modify without explicit approval.

Do not invent frameworks or commands not found in the repo.
Explain the risk of each step and how to verify it; do not assume it will run
without review.
```

**What good output looks like:** An under-250-word Markdown file citing only commands and tools that actually exist in the repo.

**Safety note:** Review instruction files in pull requests like code, and never put credentials, tokens, or internal hostnames inside them.
