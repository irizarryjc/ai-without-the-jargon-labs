# Chapter 24 Lab: Read-Only Ops Assistant in Two Agent SDKs

Lab code for Chapter 24 (*Building Your Own Agents with SDKs*) of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

Verified as of late 2026 (November). Check each SDK's official documentation for package updates.

## Files in This Folder

- `ops_tools.py`: Shared, strictly read-only Python tools (`check_service_status`, `get_recent_errors`) backed by synthetic Northwind Parts lab fixtures, with Python-enforced service allowlists and line-count clamping.
- `ops_agent_openai.py`: Implementation using the **OpenAI Agents SDK** (`pip install openai-agents`).
- `ops_agent_adk.py`: Identical assistant implemented using **Google ADK** (`pip install google-adk`).
- `test_ops_tools.py`: Standard-library unit tests proving the allowlist and clamping guardrails work offline.
- `requirements.txt`: Optional SDK packages.

## Quick Start (Offline Guardrail Verification, No API Key Required)

1. Run the unit tests:

```bash
$ python3 -m unittest test_ops_tools.py -v
```

2. Run either agent in `--dry-run` mode to inspect the local tool payloads:

```bash
$ python3 ops_agent_openai.py --dry-run
$ python3 ops_agent_adk.py --dry-run
```

## Running Against a Live Lab Model API

Use a dedicated virtual environment and export your lab key and chosen model name via environment variables (never hardcode secrets in scripts):

### Option A: OpenAI Agents SDK

```bash
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install openai-agents
$ export OPENAI_API_KEY="<your_api_key>"
$ export OPS_MODEL="<model_name>"
$ python3 ops_agent_openai.py
```

### Option B: Google ADK

```bash
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install google-adk
$ export GOOGLE_API_KEY="<your_api_key>"
$ export OPS_MODEL="<model_name>"
$ python3 ops_agent_adk.py
```

## Safety Reminder

- This lab uses synthetic fixture data only and executes zero shell or database write commands.
- Always enforce allowlists, row limits, and turn caps (`max_turns`) in deterministic Python code, never in prompt instructions alone.
