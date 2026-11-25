# Chapter 5 Prompt Toolkit: Under the Hood, Gently

Copy-ready prompts from Chapter 5 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Token & Context Budget Estimator

**Use it when:** You want a quick sanity check on how heavy a draft prompt, log slice, or document is before pasting it into an API script or long chat thread.

```text
Inspect the sanitized text block below and give me a rough context-budget estimate.
1. Estimate the approximate word count and approximate token count (explain your
   rule of thumb, noting that exact counts depend on each vendor's tokenizer).
2. Identify the three largest sources of filler, repetition, or noisy formatting.
3. Show how I could trim at least 30% of the length without losing technical facts.

Sanitized text:
<paste_sanitized_text>
```

**What good output looks like:** A realistic rough range (not fake precision to the single token) paired with concrete advice on cutting repeated timestamps or boilerplate headers.

---

## 2. Fast Model vs. Reasoning Model Head-to-Head Test

**Use it when:** You want to test whether a recurring work task genuinely needs an expensive reasoning model or if a cheaper fast model handles it just as reliably.

```text
Solve the technical problem below concisely.
1. State your final answer or recommendation in the first two sentences.
2. List the exact assumptions and step-by-step checks that support your answer.
3. Highlight the single edge case most likely to break this recommendation.
Keep the total response under 220 words.

Problem (lab or fictional scenario):
<paste_problem>
```

**What good output looks like:** Run this exact prompt on both a fast model and a reasoning model in separate fresh chats; compare accuracy on the edge case against latency and credit use.

---

## 3. Strict Word-Budget Summarizer

**Use it when:** You need to compress a long public doc or sanitized incident thread so it fits cleanly onto a smaller context desk (or into an executive status update).

```text
Summarize the sanitized text below to fit strictly under <max_words> words.
Rules:
- Preserve exact numbers, dates, error codes, and concrete decisions.
- Cut background filler, greetings, and repeated points.
- Do not invent any fact not present in the source text.
- End with a 1-line "Excluded details" note listing what you left out to hit the budget.

Source text:
<paste_sanitized_text>
```

**What good output looks like:** A dense, accurate summary honoring `<max_words>` plus an honest note showing what got trimmed so you never miss a dropped caveat.

---

## 4. Context-Lean Log Filter Helper

**Use it when:** You have a massive lab log file and want a safe local command to trim it down to only the relevant time window and error lines *before* asking an AI to explain it.

```text
Role: Act as a senior Linux sysadmin.
Goal: Give me a read-only command pipeline to filter a large lab log file (<log_file>)
down to a compact excerpt I can review safely.
Context:
- Log type: <log_type_for_example_nginx_or_postgresql_or_syslog>
- Time window or error keyword: <time_window_or_keyword>
- Target output size: under 100 lines.

Constraints:
- Strictly read-only commands (grep, awk, sed, tail, head); never modify <log_file>.
- Include a second step showing how to strip IP addresses or usernames locally before
  sharing the excerpt.
- Explain the risk of each step and how to verify it; do not assume it will run without review.
```

**What good output looks like:** A clean, read-only shell pipeline with a clear explanation of each flag so you shrink 50,000 lines into 60 sanitized lines before touching any AI tool.

**Safety note:** Test filter and redaction commands on a copy of a lab log first and visually inspect the output file before pasting it anywhere.
