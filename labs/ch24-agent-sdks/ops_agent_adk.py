"""Read-only Ops Assistant built with Google ADK (Agent Development Kit, Python).

Format as of November 2026; check https://adk.dev
Install: pip install google-adk
Env vars: GOOGLE_API_KEY=<your_api_key>, OPS_MODEL=<model_name>
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys

from ops_tools import OPS_AGENT_INSTRUCTIONS, check_service_status, get_recent_errors

APP_NAME = "northwind_lab_ops_app"
USER_ID = "lab_engineer"
SESSION_ID = "lab_session_001"


def run_dry(service: str, limit: int) -> None:
    """Verify tool allowlisting and output formatting without calling an external API."""
    print("=== Google ADK Dry-Run (Local Tools Only) ===")
    print(check_service_status(service))
    print(get_recent_errors(service, limit=limit))


async def run_agent(prompt: str) -> str:
    """Run the identical read-only ops assistant using Google ADK."""
    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Export your lab key or run with --dry-run."
        )
    model_name = os.environ.get("OPS_MODEL")
    if not model_name:
        raise RuntimeError(
            "OPS_MODEL is not set. Export your chosen model name (e.g. export OPS_MODEL=<model_name>)."
        )

    from google.adk.agents import Agent
    from google.adk.agents.run_config import RunConfig
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    # ADK inspects Python type hints and docstrings directly to build tool schemas.
    ops_agent = Agent(
        name="northwind_lab_ops_assistant",
        model=model_name,
        description="Read-only IT operations triage assistant for Northwind Parts lab.",
        instruction=OPS_AGENT_INSTRUCTIONS,
        tools=[check_service_status, get_recent_errors],
    )

    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=ops_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt)],
    )

    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
        run_config=RunConfig(max_llm_calls=4),
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = "".join(
                part.text for part in event.content.parts if getattr(part, "text", None)
            )
    return final_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only lab ops assistant (Google ADK)")
    parser.add_argument(
        "--prompt",
        default="Check the health of lab-orders-db and summarize its last 3 errors.",
        help="Read-only triage question for the lab agent.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Execute the underlying read-only Python tools locally without calling an LLM API.",
    )
    parser.add_argument("--service", default="lab-orders-db", help="Service name for --dry-run.")
    parser.add_argument("--limit", type=int, default=3, help="Error limit for --dry-run.")
    args = parser.parse_args()

    if args.dry_run:
        run_dry(args.service, args.limit)
        return 0

    try:
        output = asyncio.run(run_agent(args.prompt))
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
