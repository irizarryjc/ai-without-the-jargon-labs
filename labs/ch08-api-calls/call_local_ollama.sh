#!/usr/bin/env bash
# Format as of November 2026; check Ollama OpenAI-compatibility docs.
# Lab script: calls a local Ollama server (http://localhost:11434/v1) with no cloud API key.
set -euo pipefail

MODEL="${OLLAMA_MODEL:-<model_name>}"
BASE_URL="${OLLAMA_BASE_URL:-http://localhost:11434/v1}"

if [[ "${MODEL}" == "<model_name>" ]]; then
  echo "Set OLLAMA_MODEL to a model tag from 'ollama list' first." >&2
  echo "Example: export OLLAMA_MODEL=\"gemma4:e2b\"" >&2
  exit 1
fi

payload="$(cat <<EOF
{
  "model": "${MODEL}",
  "temperature": 0.2,
  "messages": [
    {"role": "system", "content": "Answer in two crisp sentences."},
    {"role": "user", "content": "Why should IT engineers keep API keys in environment variables?"}
  ]
}
EOF
)"

curl -sS --max-time 60 "${BASE_URL}/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ollama" \
  -d "${payload}" | python3 -m json.tool
