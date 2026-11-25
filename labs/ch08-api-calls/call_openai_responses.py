#!/usr/bin/env python3
"""Call the OpenAI Responses API using the official openai Python SDK.

Format as of November 2026; check the vendor's API reference:
https://platform.openai.com/docs/api-reference/responses

Install SDK: pip install --upgrade openai
Set env vars before running:
  export OPENAI_API_KEY="<your_api_key>"
  export OPENAI_MODEL="<model_name>"
"""

import os
import sys


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: Set OPENAI_API_KEY in your environment first.", file=sys.stderr)
        return 1

    model = os.environ.get("OPENAI_MODEL", "<model_name>")
    if model == "<model_name>":
        print("Error: Set OPENAI_MODEL to a valid model ID from the vendor's docs.", file=sys.stderr)
        return 1

    try:
        from openai import OpenAI
    except ImportError:
        print("Install the official SDK first: pip install --upgrade openai", file=sys.stderr)
        return 1

    client = OpenAI(timeout=30.0)
    response = client.responses.create(
        model=model,
        instructions="You are a concise Linux sysadmin. Answer in 2 sentences.",
        input="What does bash -n check before running a shell script?",
        max_output_tokens=150,
    )

    print("Reply:")
    print(response.output_text)
    print(f"\nStatus: {getattr(response, 'status', 'unknown')}")
    print(f"Usage:  {getattr(response, 'usage', None)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
