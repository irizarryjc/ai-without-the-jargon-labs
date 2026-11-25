# Chapter 11 Prompt Toolkit: AI-Native Editors

Copy-ready prompts from Chapter 11 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Plan, Then Implement (Two-Step Gate)

**Use it when:** You are starting a multi-file change in Cursor, Antigravity, Devin Desktop, or Kiro and want a reviewable design before a single file is modified.

```text
Inspect <project_root> (read-only) and propose an implementation plan for:
<feature_or_fix_description>

Do NOT create or edit any files yet. Output:
1. Files to create or modify (exact paths).
2. Key design decisions and edge cases handled.
3. Exact commands to test and verify the change in this lab environment.
4. Any assumptions or open questions I should answer before you start coding.
Wait for my explicit approval before making edits.
```

**What good output looks like:** A crisp, bounded list of files, explicit edge cases, and concrete test commands with zero premature code edits.

**Safety note:** Review the file list carefully to ensure no configuration, credential, or out-of-scope production files are included before approving.

---

## 2. Show Me the Diff Before Applying

**Use it when:** You want tight control over a sensitive refactor (such as changing input validation, file handling, or SQL query templates) inside an AI-native editor.

```text
Prepare the changes needed in <file_path> to accomplish <goal>.
Before applying edits directly to disk (or immediately after proposing a draft
in diff review):
1. Show a concise summary of every hunk you plan to change and why.
2. Confirm that no external packages or public CLI flags are altered.
3. Explain the risk of each step and how to verify it; do not assume it will
   run without review.
```

**What good output looks like:** A hunk-by-hunk rationale that makes reviewing the visual diff fast and flags any subtle behavior change up front.

**Safety note:** Never batch-accept diffs blindly; inspect every deleted and modified line and run tests locally after accepting.

---

## 3. Kiro-Style Requirements From a One-Line Idea

**Use it when:** You have a rough one-sentence idea for an internal utility or script and want structured requirements and acceptance criteria (usable in Kiro or any AI editor).

```text
Turn this rough lab utility idea into a concise specification (under 400 words)
using three sections: Requirements, Design, and Tasks.

Idea: <one_line_idea>
Target runtime: <language_and_version> on <target_os>

Rules:
- Write 4 to 6 testable acceptance criteria (WHEN <condition>, THE script SHALL
  <expected_behavior>).
- Keep all inputs and outputs strictly for lab/synthetic data.
- Include explicit error-handling requirements for invalid inputs and missing files.
- Do not write implementation code yet; wait for my review of the spec.
```

**What good output looks like:** Clear, testable acceptance criteria you can immediately turn into unit tests before the agent writes implementation code.

**Safety note:** Confirm the spec includes least-privilege boundaries (read-only defaults, input validation, no live production endpoints) before moving to code.

---

## 4. Compare Two Approaches Before Committing

**Use it when:** You want to evaluate two architectural options (for example, in parallel Git worktrees or planning artifacts) before investing in full implementation.

```text
I need to solve <problem_description> inside a LAB repository at <project_root>.
Do NOT edit files yet. Compare two concrete approaches:
- Option A: <approach_a_summary>
- Option B: <approach_b_summary>

Provide a short comparison table covering:
1. Implementation complexity and files touched.
2. Failure modes and rollback difficulty.
3. Maintenance burden for an operations team six months from now.
4. Your recommendation and what assumption would flip your recommendation.
Explain the risk of each step and how to verify it; do not assume any change
will run without review.
```

**What good output looks like:** An honest trade-off table that surfaces operational maintenance costs and rollback risks rather than pushing the fancier pattern by default.

**Safety note:** Keep all scenario details synthetic or redacted; verify any claimed library or OS behavior against official documentation.
