# Chapter 30 Prompt Toolkit: Cost Control

Copy-ready prompts from Chapter 30 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety Check:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Monthly Token Cost Estimator

**Use it when:** You want a clear cost breakdown before scheduling an AI script or n8n workflow.

```text
Estimate the monthly API cost for this planned LAB workflow using ONLY the rates I
supply below (do NOT invent vendor prices):
- Runs per month: <runs_per_month>
- Static prefix tokens/run: <static_tokens>
- Dynamic input tokens/run: <dynamic_tokens>
- Output tokens/run: <output_tokens>
- Rates I checked today: <input_rate_per_1m> input, <output_rate_per_1m> output,
  <cached_read_rate_per_1m> cached read

Show step-by-step arithmetic for:
1. Uncached monthly cost.
2. Cached monthly cost (assuming 90% cache hit on the static prefix).
3. Top 3 safe ways to trim tokens without losing accuracy.
```

**What good output looks like:** Transparent arithmetic you can double-check on a calculator plus concrete token-trimming suggestions.

**Safety note:** Check prices on the vendor's live pricing page and verify all arithmetic yourself (LLMs can still slip on math without tools).

---

## 2. Token-Diet Prompt Rewriter

**Use it when:** A system prompt or `AGENTS.md` has grown bloated and burns excess tokens every turn.

```text
Shorten the sanitized system prompt or rules file below by at least 40 percent WITHOUT
dropping any safety rules, JSON schema constraints, or stop conditions:

<paste_current_prompt>

Return:
1. The tightened prompt with static rules at the top (cache-friendly).
2. A brief changelog of what was condensed.
3. Which eval cases I should re-run to confirm zero regressions.
```

**What good output looks like:** A crisp, cache-friendly prompt preserving every safety constraint alongside concrete regression checks.

**Safety note:** Always run your Chapter 29 eval suite before replacing the original prompt.

---

## 3. Routed Model Architecture Advisor

**Use it when:** A multi-step workflow currently uses one flagship model everywhere and you want a cheaper routed design.

```text
Review this multi-step LAB workflow and recommend a cost-effective tier split
(deterministic code, local Ollama, fast small API, or reasoning API; do not hard-code
model version numbers):

Workflow steps (sanitized):
<list_workflow_steps_and_volume>

Output a table with: Step name, Recommended tier, Trade-off rationale, and Eval check
to prove quality holds. Explain the risk of each change and how to verify it; do not
assume any change will run without review.
```

**What good output looks like:** A balanced plan pushing filtering to deterministic code, routine parsing to fast/local models, and reserving reasoning models for hard decisions.

**Safety note:** Never downgrade safety-review steps without verifying 100 percent pass rates on safety evals.
