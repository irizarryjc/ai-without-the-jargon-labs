# Chapter 2 Prompt Toolkit: Your First Conversations: Chat Assistants

Copy-ready prompts from Chapter 2 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Email Thread to Action Items

**Use it when:** You are copied late on a sprawling email or chat thread and need decisions, owners, and open questions fast.

```text
Read the sanitized email thread below and extract a clean status summary.
Use ONLY facts explicitly stated in the thread. Do not invent deadlines or owners.
If an action item has no named owner or due date, write "Unassigned" or "TBD."

Output format:
1. Context (2 sentences max)
2. Decisions already agreed (bullets)
3. Action items table with columns: Task | Owner | Due Date | Status
4. Open questions still unresolved (bullets)

Sanitized thread:
<paste_sanitized_thread>
```

**What good output looks like:** A scannable action table with honest "Unassigned" and "TBD" placeholders instead of guessed names or dates.

**Safety note:** Remove customer names, email addresses, ticket numbers, internal URLs, and attachments before pasting into a non-enterprise tool.

---

## 2. Polite, Clear Workplace Reply

**Use it when:** You need to push back on an unrealistic request, clarify scope, or deliver bad news calmly without sounding defensive.

```text
Draft a polite, direct reply to the sanitized message below.
My goal: <your_goal_for_example_delay_nonurgent_change_until_next_window>.
Key constraints I must include:
- <constraint_1>
- <constraint_2>

Tone: professional, calm, collaborative, no corporate fluff, under 150 words.
Give me two versions: one brief (for chat) and one slightly fuller (for email).

Message I am replying to (sanitized):
<paste_sanitized_message>
```

**What good output looks like:** Two grounded, human-sounding drafts that protect your technical boundary while offering a clear next step.

**Safety note:** Strip real employee names and internal incident details; re-read before sending so the message sounds like you.

---

## 3. Two-Document Side-by-Side Comparison

**Use it when:** You are comparing two public vendor docs, release notes, or sanitized draft proposals and want exact differences rather than vague prose.

```text
Compare Document A and Document B below strictly on the facts written in each text.
Do not fill gaps from outside memory. If a topic is missing from one document,
state "Not mentioned."

Focus on these criteria: <criterion_1>, <criterion_2>, <criterion_3>, <criterion_4>.

Output format:
1. A Markdown comparison table (Criterion | Document A | Document B | Key Difference)
2. Top 3 practical implications for an IT practitioner
3. Up to 3 clarifying questions I should verify against vendor documentation

Document A:
<paste_document_a>

Document B:
<paste_document_b>
```

**What good output looks like:** An honest, structured table where missing items say "Not mentioned" and differences point directly to decisions you need to make.

**Safety note:** Only paste public documents or approved internal docs inside an approved enterprise workspace.

---

## 4. Weekly Plan From a Messy Task List

**Use it when:** Monday morning hits with twenty competing tasks and you want a realistic priority order and focus blocks.

```text
Help me organize my upcoming work week from the messy task list below.
Constraints:
- Fixed meetings or maintenance windows: <paste_time_blocks>
- Maximum deep-focus hours per day: <hours_per_day>
- Leave at least 20% buffer time for unplanned incidents or support interrupts.

Group every task into:
1. Must finish this week (high impact or deadline)
2. Should advance (important, flexible timing)
3. Defer, delegate, or clarify (flag what info is missing)

Then propose a simple Monday-to-Friday focus schedule. Do not invent tasks I did not list.

Task list (sanitized, no project codenames or client info):
<paste_task_list>
```

**What good output looks like:** A realistic plan with visible interrupt buffers rather than an overpacked schedule that collapses by Tuesday noon.
