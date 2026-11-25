#!/usr/bin/env python3
"""Chapter 19 lab (Option B): MCP server implementation of check_replication_lag.

# Format as of November 2026; check current official Python MCP SDK docs.

Exposes the exact same read-only replication-lag check over MCP (stdio) so multiple
hosts (Claude Code, VS Code + Copilot, Cursor, Google Antigravity, Codex CLI, n8n)
can share one server without rewriting integrations.

Install the official Python MCP SDK before running as an MCP server (pinned as of
November 2026; check PyPI for newer security releases and re-pin):
    pip install "mcp[cli]==2.3.0"

Run --self-test to verify the read-only handler locally without the MCP SDK installed.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from native_repl_lag import check_replication_lag

# CRITICAL for stdio MCP servers: route all logs to stderr, never stdout.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [mcp-repl-server] %(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp-repl-server")

DEFAULT_DB_PATH = Path(os.environ.get("REPL_LAB_DB", "repl_lab.db"))


def build_mcp_server(db_path: Path = DEFAULT_DB_PATH) -> Any:
    """Wrap the shared read-only replication-lag check in the official Python MCP SDK (v2 or v1)."""
    try:
        from mcp.server import MCPServer as _ServerClass  # Official Python MCP SDK v2+
    except ImportError:
        from mcp.server.fastmcp import FastMCP as _ServerClass  # Official Python MCP SDK v1.x

    server = _ServerClass("northwind-repl-lag-readonly")

    @server.tool()
    def get_replication_lag(replica_name: str, warn_threshold_seconds: int = 30) -> str:
        """Check read-only replication lag in seconds for one approved Northwind Parts LAB replica.

        Allowed replica_name values: orders-ro-east, orders-ro-west, analytics-dg-01.
        Read-only; cannot restart replication, fail over, or modify database state.
        """
        result = check_replication_lag(
            db_path=db_path,
            replica_name=replica_name,
            warn_threshold_seconds=warn_threshold_seconds,
        )
        logger.info("audit mode=mcp tool=get_replication_lag replica=%r ok=%s", replica_name, result.get("ok"))
        return json.dumps(result)

    return server


# Module-level export so `mcp dev mcp_repl_lag_server.py` discovers the server automatically,
# while guarded so `--self-test` still runs without the `mcp` package installed.
try:
    mcp = build_mcp_server()
except ImportError:
    mcp = None


def main() -> None:
    parser = argparse.ArgumentParser(description="Chapter 19 MCP check_replication_lag server.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH, help="Path to repl_lab.db.")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Verify the underlying read-only check locally without starting stdio transport.",
    )
    args = parser.parse_args()

    if args.self_test:
        print(json.dumps(check_replication_lag(args.db, "orders-ro-east", 30), indent=2))
        print(json.dumps(check_replication_lag(args.db, "analytics-dg-01", 30), indent=2))
        print(json.dumps(check_replication_lag(args.db, "unknown-node", 30), indent=2))
        return

    mcp = build_mcp_server(db_path=args.db)
    logger.info("Starting northwind-repl-lag-readonly MCP server on stdio (db=%s)", args.db.resolve())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
