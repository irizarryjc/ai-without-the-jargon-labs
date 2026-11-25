#!/usr/bin/env bash
# Format as of November 2026; check the vendor's API reference:
# https://platform.openai.com/docs/api-reference/responses
# Never hardcode API keys; always load from environment variables.
set -euo pipefail

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "Error: OPENAI_API_KEY is not set. Run: export OPENAI_API_KEY=\"<your_api_key>\"" >&2
  exit 1
fi

MODEL="${OPENAI_MODEL:-<model_name>}"
if [[ "${MODEL}" == "<model_name>" ]]; then
  echo "Error: Set OPENAI_MODEL to a valid model ID from the vendor's API reference." >&2
  exit 1
fi

payload="$(cat <<EOF
{
  "model": "${MODEL}",
  "instructions": "You are a concise Linux sysadmin. Answer in 2 sentences.",
  "input": "What does bash -n check before running a shell script?",
  "max_output_tokens": 150
}
EOF
)"

curl -sS --max-time 30 https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -d "${payload}" | python3 -m json.tool
