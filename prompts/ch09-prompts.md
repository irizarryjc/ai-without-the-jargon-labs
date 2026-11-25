# Chapter 9 Prompt Toolkit: Running AI on Your Own Machine

Copy-ready prompts from Chapter 9 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Local Model Sizing Advisor for My Hardware

**Use it when:** You want a practical shortlist of open-weight model sizes and quantization levels that will run comfortably on your specific laptop or workstation.

```text
Recommend 3 practical open-weight model options I can run locally via Ollama
or LM Studio on my machine.

My hardware specs:
- OS and CPU: <os_and_cpu>
- System RAM: <total_ram_gb> GB
- GPU and VRAM (or Apple Silicon unified memory): <gpu_and_vram_or_none>
- Primary offline tasks: <for_example_log_summaries_bash_help_doc_qa>

Constraints:
- Leave comfortable RAM headroom for my OS and browser.
- For each option, specify recommended parameter size (for example 7B or 14B),
  typical quantization (such as Q4_K_M), rough memory footprint, and expected
  speed trade-offs.
- Remind me to verify exact model tags and licenses on ollama.com or the official
  model card rather than guessing exact tag strings.
```

**What good output looks like:** Realistic size tiers tailored to your actual VRAM/RAM ceiling instead of suggesting a 70B model for a 16 GB laptop.

---

## 2. Compact Offline Document Q&A (Sized for Local Models)

**Use it when:** You are working offline with a smaller 7B to 14B local model and want focused, grounded answers without overflowing its context window.

```text
Answer ONLY from the short reference excerpt below. Keep your answer under
120 words. If the answer is not in the excerpt, reply: "Not in excerpt."

Question: <your_question>

Excerpt:
<paste_short_sanitized_excerpt>
```

**What good output looks like:** Short, tight, faithful replies that stay well inside a local model's smaller context budget.

---

## 3. Local Code or Script Explainer

**Use it when:** You want to inspect an unfamiliar Bash, Python, PowerShell, or SQL script completely offline on your workstation.

```text
Explain the lab script below in plain English for an IT practitioner.
Output format:
1. One-sentence summary of what the script does.
2. Line-by-line (or block-by-block) explanation of key commands and flags.
3. Up to 3 safety risks or assumptions I should verify before running it in a lab.
Explain the risk of each step and how to verify it; do not assume it will run without review.

Script (sanitized, lab only):
<paste_script>
```

**What good output looks like:** Clear block-by-block breakdown flagging dangerous flags, missing error checks, or hardcoded paths without sending your script over the internet.

**Safety note:** Smaller local models can miss subtle syntax bugs; always double-check flags with `--help` or `man` and test inside a disposable lab.
