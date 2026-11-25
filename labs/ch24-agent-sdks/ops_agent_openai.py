"""Read-only Ops Assistant built with the OpenAI Agents SDK (Python).

Format as of November 2026; check https://developers.openai.com/api/docs/guides/agents/sdk
Install: pip install openai-agents
Env vars: OPENAI_API_KEY=<your_api_key>, OPS_MODEL=<model_name>
"""

from __future__ import annotations

import argparse
import os
import sys

from ops_tools import OPS_AGENT_INSTRUCTIONS, check_service_status, get_recent_errors


def run_dry(service: str, limit: int) -> None:
    """Verify tool allowlisting and output formatting without calling an external API."""
    print("=== OpenAI Agents SDK Dry-Run (Local Tools Only) ===")
    print(check_service_status(service))
    print(get_recent_errors(service, limit=limit))


def run_agent(prompt: str) -> str:
    """Run the read-only ops assistant using the OpenAI Agents SDK."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export your lab key or run with --dry-run."
        )
    model_name = os.environ.get("OPS_MODEL")
    if not model_name:
        raise RuntimeError(
            "OPS_MODEL is not set. Export your chosen model name (e.g. export OPS_MODEL=<model_name>)."
        )

    from agents import Agent, Runner, function_tool

    # Wrap our validated, read-only Python functions as SDK tools.
    status_tool = function_tool(check_service_status)
    errors_tool = function_tool(get_recent_errors)

    ops_agent = Agent(
        name="Northwind Lab Ops Assistant",
        model=model_name,
        instructions=OPS_AGENT_INSTRUCTIONS,
        tools=[status_tool, errors_tool],
    )

    result = Runner.run_sync(ops_agent, prompt, max_turns=4)
    return str(result.final_output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only lab ops assistant (OpenAI Agents SDK)")
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
        output = run_agent(args.prompt)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
