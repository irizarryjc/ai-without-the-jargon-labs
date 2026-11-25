# Chapter 29 Lab: Repeatable AI Eval Runner (Zero External Dependencies)

This lab accompanies Chapter 29 (*Quality: Evals, Testing, and Observability*) of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

## What Is Inside

- `eval_cases.jsonl`: 10 synthetic IT operations and safety test cases (fictional lab scenarios only, zero real secrets or PII).
- `eval_runner.py`: A pure Python 3 standard-library eval harness that runs deterministic assertions (JSON schema keys, required terms, forbidden destructive verbs, and prompt-injection resistance) against either:
  - `--mode mock` (default): Built-in illustrative baseline responses so you can run the lab offline immediately.
  - `--mode file --responses <path>`: Your own JSONL file of captured model outputs (for comparing Prompt A vs. Prompt B or Model A vs. Model B).
  - `--mode ollama --model <model_name>`: Optional live evaluation against a local Ollama server (`http://localhost:11434/api/generate`), keeping lab data completely offline.

## Quick Start

```bash
python3 eval_runner.py --cases eval_cases.jsonl --mode mock
```

To compare a candidate response file:

```bash
python3 eval_runner.py --cases eval_cases.jsonl --mode file --responses sample_responses.jsonl --json-out eval_report.json
```

## Safety Rules

- Never place real customer data, production hostnames, passwords, or API keys in `eval_cases.jsonl` or output reports.
- Deterministic assertions catch format, keyword, and safety-boundary failures; always pair them with human spot checks for subtle technical accuracy.
