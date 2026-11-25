# Chapter 33 Prompt Toolkit: Capstones, DBA and Sysadmin Track (Safely)

Copy-ready prompts from Chapter 33 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety Check:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Lab SQL Execution-Plan Tuner

**Use it when:** You have captured a slow query's DDL, anonymized table stats, and `EXPLAIN` plan from a lab database and want ranked, verifiable tuning options.

```text
You are a senior <database_engine> DBA helping me tune a read-only query in a LAB database.
Here is the sanitized DDL, table skew/stats, and execution plan (zero production rows):
<paste_ddl_stats_and_plan>

1. Explain in plain English where time and I/O are going.
2. Propose up to 3 changes ranked from lowest to highest risk (note write/lock impact).
3. For each change, give the exact verification query and exact rollback statement.
Explain the risk of each step and how to verify it; do not assume any change will run
without review.
```

**What good output looks like:** Clear bottleneck explanation tied to actual plan lines, sensible composite index order, and clean verification plus rollback commands.

**Safety note:** Use lab or masked-clone metadata only; never paste production customer values or run `EXPLAIN ANALYZE` on unrolled-back write queries.

---

## 2. Structured Operations Runbook Writer

**Use it when:** You want to turn messy troubleshooting notes into a clean, repeatable runbook or `SKILL.md` procedure for an on-call team.

```text
Turn the sanitized troubleshooting notes below into a step-by-step read-only operations
runbook for <system_or_db_engine> (suitable for a team wiki or SKILL.md):
<paste_sanitized_notes>

Include these exact sections:
1. Pre-checks (verify target host and read-only role).
2. Read-only diagnostic steps (one action per step with expected healthy output).
3. Escalation thresholds (when to page the lead).
4. Explicit "Forbidden actions" list (no unapproved restarts, DDL, or deletes).
5. Rollback notes.
Explain the risk of each step and how to verify it; do not assume any command will run
without review.
```

**What good output looks like:** A calm, scannable runbook an on-call engineer can follow at 3:00 AM without guessing thresholds or accidentally triggering writes.

**Safety note:** Test every diagnostic command in a lab host before publishing the runbook to your team.

---

## 3. Redacted Alert-Log Triage Summarizer

**Use it when:** You have pre-filtered and redacted a noisy alert log and want a fast root-cause hypothesis and draft ticket with zero auto-remediation.

```text
Summarize the redacted lab log excerpt below for an on-call ticket draft.
Do NOT suggest restarting services, deleting files, or editing production configs.

Redacted log excerpt:
<paste_redacted_logs>

Return:
1. Grouped error counts and timestamps.
2. Most likely correlated cause (strictly grounded in the lines provided; say "unknown"
   if evidence is missing).
3. First 2 safe read-only checks to confirm the cause.
4. Draft ticket title and 3-sentence summary marked "Human review required."
```

**What good output looks like:** Accurate grouping that connects related errors (such as disk pressure causing archive failures) without inventing causes or risky fixes.

**Safety note:** Strip all real hostnames, internal IPs, passwords, and customer IDs locally before pasting log lines.

---

## 4. On-Call Script Documentation Generator

**Use it when:** You wrote or inherited an operations Bash or Python script and want crisp documentation for the next on-call engineer.

```text
Document the sanitized lab operations script below for a busy on-call engineer who has
never seen it before:
<paste_sanitized_script>

Produce clean Markdown with:
1. Plain-English purpose (2 sentences).
2. Inputs, environment variables (placeholders only), and read-only vs write behavior.
3. Exact dry-run or verification command and expected exit codes.
4. Common failure modes and safe rollback steps.
Do not invent flags or side effects that are not present in the code.
```

**What good output looks like:** Honest, faithful documentation that highlights exact side effects, exit codes, and prerequisites without fluff.

**Safety note:** Remove any hardcoded internal URLs, secrets, or proprietary hostnames before pasting scripts.

---

## 5. Migration & Config Diff Change Reviewer

**Use it when:** You want a thorough pre-CAB peer review of a SQL migration script or infrastructure config diff before scheduling a maintenance window.

```text
Act as a cautious senior DBA and sysadmin reviewing this LAB migration or config diff
for <database_engine_or_platform>:
<paste_sanitized_diff>

Audit strictly for:
1. Table/metadata locking duration and concurrency impact.
2. Irreversible data-loss risks (DROP, TRUNCATE, destructive type changes).
3. Missing indexes on foreign keys or unbatched bulk UPDATE/DELETE statements.
4. Missing pre-checks, post-checks, or tested rollback SQL.

End with a "Human Sign-Off Required" gate checklist. Explain the risk of each finding
and how to verify it in a lab clone; do not assume any change will run without review.
```

**What good output looks like:** Line-by-line risk findings ranked by severity, concrete expand-contract alternatives, and an explicit human sign-off gate.

**Safety note:** Never treat a clean AI review as permission to skip lab-clone testing or formal change approval.
