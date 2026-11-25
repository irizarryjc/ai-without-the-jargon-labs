# Chapter 14 Prompt Toolkit: Context Engineering: Rules Files, AGENTS.md, and Memory

Copy-ready prompts from Chapter 14 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Draft a Vendor-Neutral `AGENTS.md`

**Use it when:** You are onboarding a repository to AI coding tools and want a clean, cross-vendor `AGENTS.md` grounded strictly in what actually exists in the project.

```text
Inspect <project_root> in READ-ONLY mode (do not edit files yet) and draft a
vendor-neutral `AGENTS.md` file (under 220 words) that works across coding agents.

Include:
1. Project Overview (runtime versions, languages, lab/target environment).
2. Always-On Rules (5 to 7 concrete, verifiable engineering and safety constraints).
3. Exact Verification Commands (test, lint, and syntax commands found in this repo).
4. Restricted paths the agent must never modify without explicit approval.

Do not invent tools, frameworks, or commands not present in the repository.
Explain the risk of each rule and how to verify compliance; do not assume any
file will be applied without review.
```

**What good output looks like:** A crisp, under-220-word Markdown file using real repo commands and clear safety boundaries, with zero generic filler.

**Safety note:** Review every line before committing and confirm zero credentials, internal IPs, or proprietary customer names appear anywhere in the file.

---

## 2. Shrink Bloated Instructions to Under 200 Words

**Use it when:** Your `AGENTS.md`, `CLAUDE.md`, or Copilot instructions file has grown past a page and agents have started ignoring important constraints.

```text
Condense the rules file below to under 200 words without losing any hard
security boundary, build/test command, or forbidden action.

Current rules (sanitized):
<paste_sanitized_rules>

Output:
1. The tightened rules file in clean Markdown bullets.
2. A short list of verbose or redundant lines you removed.
3. Any specialized rules that should move out of always-on instructions into a
   glob-scoped rule file (with suggested glob patterns) or an Agent Skill.
```

**What good output looks like:** A sharper, shorter root rules file plus concrete suggestions for splitting SQL, shell, or frontend rules into conditional files.

**Safety note:** Check the "removed lines" list carefully to ensure no critical security or rollback constraint was accidentally dropped.

---

## 3. Find Contradictions in My Rules Files

**Use it when:** Your repository has accumulated multiple instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`) and agents behave inconsistently.

```text
Read the following rules files from <project_root> without modifying anything:
<paste_or_reference_sanitized_rules_files>

Audit them for:
1. Direct contradictions (conflicting test commands, style rules, or package managers).
2. Duplicated rules that will drift across tools.
3. Ambiguous wording ("handle gracefully", "be fast") that should become concrete checks.
4. Missing safety boundaries (input validation, secret handling, read-only defaults).

Recommend a single-source-of-truth layout centered on `AGENTS.md` plus minimal
tool-specific shims. Explain the risk of each change and how to verify it; do
not assume it will run without review.
```

**What good output looks like:** A concise audit pinpointing exact conflicting lines and a clean consolidation plan so every tool enforces the same rules.

**Safety note:** Never paste rules files containing sensitive internal hostnames or URLs into consumer chat tools; sanitize first.

---

## 4. Monthly Agent Memory Cleanup Audit

**Use it when:** You export or review your assistant or coding agent's saved memory entries and want to prune stale or risky items cleanly.

```text
Review this sanitized list of saved agent memory entries:
<paste_sanitized_memory_entries>

Classify each item into one of four buckets:
1. KEEP: Still accurate, genuinely useful personal preference.
2. DELETE: Outdated version, one-off workaround, or contradicted by current workflows.
3. MOVE TO GIT: Team or project rule that belongs in `AGENTS.md` instead of personal memory.
4. REMOVE IMMEDIATELY (SECURITY): Contains anything resembling a credential,
   internal host, IP address, customer identifier, or sensitive path.

Provide a short justification for each classification.
```

**What good output looks like:** A clean triage list that takes two minutes to apply and prevents outdated memories from silently breaking future prompts.

**Safety note:** Strip any real secrets or identifiers *before* pasting into a prompt, and delete sensitive items directly inside your tool's memory settings first.
