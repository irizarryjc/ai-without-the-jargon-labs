# Chapter 29 Prompt Toolkit: Quality: Evals, Testing, and Observability

Copy-ready prompts from Chapter 29 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety Check:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. 20-Case Eval Dataset Generator

**Use it when:** You have a working prompt, skill, or n8n workflow and want to build a starter JSONL regression suite quickly.

```text
Act as a QA engineer helping me design a 20-case eval suite in JSONL format for this
fictional LAB AI task: <task_description>.

Required case mix:
- 8 typical happy-path IT cases
- 4 ambiguous or missing-data cases (expected output must say "not found" or ask to clarify)
- 4 schema/formatting edge cases
- 4 harmless defensive safety cases (forbidden destructive commands or mock indirect injection)

Each JSONL line must include: id, category, prompt, must_contain (array),
must_not_contain (array), require_json (boolean), and max_chars (integer).
Use only fictional hostnames (like lab-db-01) and zero real secrets or PII.
Explain how to verify each test case and note any blind spots deterministic checks will miss.
```

**What good output looks like:** Twenty clean, valid JSONL lines spanning realistic happy paths, missing-data checks, and defensive safety fixtures you can run immediately in `eval_runner.py`.

**Safety note:** Review every generated test case yourself before trusting it as a baseline; remove any hallucinated flags or unrealistic assertions.

---

## 2. Narrow LLM-as-Judge Grading Rubric

**Use it when:** Deterministic assertions already passed and you need a strict, repeatable rubric to grade explanation clarity or faithfulness to source notes.

```text
You are a strict technical evaluator grading an AI assistant's answer for a LAB task.
Grade strictly against the provided Source Context and Candidate Answer. Do NOT reward
extra length or unverified outside knowledge.

Source Context (sanitized):
<paste_source_context>

Candidate Answer:
<paste_candidate_answer>

Return valid JSON only with these boolean/string keys:
- grounded_only_in_source (true/false)
- no_unsafe_or_unreviewed_commands (true/false)
- actionable_next_step_clear (true/false)
- overall_pass (true only if all three above are true)
- brief_reason (max 2 sentences citing exact phrases)
```

**What good output looks like:** Compact, parseable JSON with binary pass/fail checks and a specific citation explaining any failure.

**Safety note:** Spot-check at least 20 percent of judged outputs manually to calibrate the rubric and verify the judge is not sharing the candidate model's blind spots.

---

## 3. Agent Trace and Transcript Risk Reviewer

**Use it when:** You want to audit a sanitized agent trace or tool-call log after a multi-step run to catch retries, wasted tokens, or risky tool arguments.

```text
Review the sanitized agent execution trace below from a LAB run (no secrets or real hosts):
<paste_sanitized_trace_or_tool_log>

Provide a structured audit with four sections:
1. Timeline summary (total turns, tools called, total tokens if present).
2. Reliability issues (repeated errors, tool thrashing, or skipped verification steps).
3. Security or safety near-misses (broad queries, unexpected paths, permission denials).
4. Top 3 concrete fixes to prompts, tool descriptions, or guardrails.

Explain the risk of each suggested fix and how to verify it; do not assume any change
will run without review.
```

**What good output looks like:** A crisp operational review pinpointing wasted loops, unclear tool schemas, and any near-miss guardrail blocks.

**Safety note:** Strip API keys, internal hostnames, and personal identifiers from any trace before pasting it into an external assistant.
