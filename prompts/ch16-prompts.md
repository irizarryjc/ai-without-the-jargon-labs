# Chapter 16 Prompt Toolkit: What Makes an Agent an Agent

Copy-ready prompts from Chapter 16 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Should This Be an Agent, a Workflow, or a Script?

**Use it when:** You want an honest check on whether a recurring task really needs an agent or belongs in a plain script or fixed workflow.

```text
You are a pragmatic senior systems architect helping me pick the simplest reliable
automation pattern for a LAB or internal workflow.
Do NOT recommend an AI agent when a plain script or fixed workflow is safer or cheaper.

Sanitized tasks (no real hostnames or company data):
1. <task_1_description>
2. <task_2_description>
3. <task_3_description>

Return a table with columns:
- Task
- Recommended pattern (Plain Script | Agentic Workflow | Supervised Agent | Keep Manual)
- Why it fits best
- Main failure mode if over-automated
- Minimum permissions and human checkpoint required
```

**What good output looks like:** A concise table that pushes deterministic checks back to scripts and reserves agents for genuinely branching diagnostic or coding work.

---

## 2. Stop-Condition and Guardrail Writer

**Use it when:** A task genuinely needs a bounded agent and you want concrete stop conditions, caps, and escalation rules before running it.

```text
Help me write explicit stop conditions and least-agency guardrails for a bounded
agent running in a LAB environment.

Goal: <short_goal_description>
Lab scope: <os_or_platform_and_lab_scope>
Candidate tools: <list_of_tools>

Provide five concise sections:
1. Objective definition of done.
2. Max loop turns and token or timeout limit.
3. Read-only vs. write boundary (tools to drop or gate behind human approval).
4. Escalation triggers where the agent must stop and ask a human.
5. Lab verification and rollback steps.

Explain the risk of each step and how to verify it; do not assume it will run
without review.
```

**What good output looks like:** Specific numeric caps, a trimmed tool list, and testable stop rules instead of vague safety advice.

**Safety note:** Use lab details only, and enforce caps in host settings, code, or hooks rather than prompt text alone.

---

## 3. Agent Failure-Mode Pre-Mortem

**Use it when:** You want to uncover spinning loops, cost spikes, or prompt-injection risks in a proposed agent design before testing it.

```text
Act as a reliability and security reviewer running a pre-mortem on this LAB agent
design for <fictional_org>:

Workflow and tools (sanitized):
<paste_sanitized_workflow_and_tools>

List the five most likely failure modes covering: spinning loops, goal drift,
false "all clear" summaries, runaway token cost, and indirect prompt injection.
For each failure mode, give:
- How it triggers
- One technical control (not just prompt wording) to prevent it
- A safe lab test to verify the control works.
Explain the risk of each control gap and how to verify it; do not assume it will
run without review.
```

**What good output looks like:** Concrete failure paths tied to your exact tools and a short lab test for each safeguard.

**Safety note:** Never paste real production architecture, endpoints, or credentials into an external chat tool.
