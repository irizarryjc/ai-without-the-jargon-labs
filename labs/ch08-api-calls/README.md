# Chapter 8 Lab: Talking to Models Directly (API Calls)

Runnable `curl` and Python scripts from Chapter 8 (*Talking to Models Directly: API Calls Explained*) of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

*Format as of November 2026; check the vendor's current API reference.*

## Safety First

- Never hardcode `<your_api_key>` inside any script or commit `.env` files to Git.
- Always set a low monthly spend limit on your vendor billing dashboard before running cloud scripts.
- Practice first against a local Ollama server (`http://localhost:11434/v1`) with zero cloud API key.

## Files in This Lab

- `call_local_ollama.sh`: Calls a local Ollama server via `curl` with no cloud key.
- `call_local_ollama.py`: Calls a local Ollama server via Python 3 standard library (`urllib`, zero extra packages) and prints content, finish reason, and token usage.
- `call_openai_responses.sh`: Calls the OpenAI Responses API (`/v1/responses`) via `curl` reading `OPENAI_API_KEY` from the environment.
- `call_openai_responses.py`: Calls the OpenAI Responses API using the official `openai` Python SDK (`pip install --upgrade openai`).

## Quick Syntax Check (Safe, Does Not Call Any Network)

```bash
bash -n call_local_ollama.sh call_openai_responses.sh
python3 -m py_compile call_local_ollama.py call_openai_responses.py
```

## Running the Local Ollama Lab (No Cloud Key Needed)

```bash
# 1. Confirm Ollama is installed and pick a pulled model tag from `ollama list`
export OLLAMA_MODEL="<model_name>"

# 2. Run the curl version
bash call_local_ollama.sh

# 3. Run the Python version
python3 call_local_ollama.py
```

## Running the Cloud Responses API Example (Optional)

> **Shell history tip:** Avoid leaving live API keys in `~/.bash_history`. On macOS/Linux, load the key silently with `read -s -p "API key: " OPENAI_API_KEY && export OPENAI_API_KEY`, use a secrets manager, or prefix `export` with a leading space in Bash when `HISTCONTROL=ignorespace` is enabled.

```bash
# macOS / Linux (better: use read -s or a secrets manager instead of literal export)
export OPENAI_API_KEY="<your_api_key>"
export OPENAI_MODEL="<model_name>"
bash call_openai_responses.sh
python3 call_openai_responses.py
```

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "<your_api_key>"
$env:OPENAI_MODEL = "<model_name>"
python call_openai_responses.py
```
