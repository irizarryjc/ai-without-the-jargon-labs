#!/usr/bin/env python3
"""Call a local Ollama OpenAI-compatible API using Python's standard library.

Format as of November 2026; check Ollama OpenAI-compatibility docs.
Runs locally against http://localhost:11434/v1 with no cloud API key.
"""

import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    model = os.environ.get("OLLAMA_MODEL", "<model_name>")
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1").rstrip("/")

    if model == "<model_name>":
        print(
            "Set OLLAMA_MODEL to a model tag shown by `ollama list` first.",
            file=sys.stderr,
        )
        return 1

    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": "Answer in two crisp sentences."},
            {
                "role": "user",
                "content": "Why should IT engineers keep API keys in environment variables?",
            },
        ],
    }

    req = urllib.request.Request(
        url=f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer ollama",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        print(f"Could not reach local Ollama server at {base_url}: {exc}", file=sys.stderr)
        return 1

    choice = data.get("choices", [{}])[0]
    content = choice.get("message", {}).get("content", "")
    finish_reason = choice.get("finish_reason", "unknown")
    usage = data.get("usage", {})

    print("Reply:")
    print(content.strip())
    print(f"\nFinish reason: {finish_reason}")
    print(f"Token usage:   {json.dumps(usage)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
