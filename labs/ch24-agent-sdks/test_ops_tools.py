"""Unit tests verifying allowlist and clamping guardrails on the Chapter 24 ops tools."""

from __future__ import annotations

import json
import unittest

from ops_tools import MAX_ERROR_LIMIT, check_service_status, get_recent_errors


class OpsToolsGuardrailTests(unittest.TestCase):
    def test_allowlisted_service_returns_status(self) -> None:
        payload = json.loads(check_service_status("lab-orders-db"))
        self.assertEqual(payload["service"], "lab-orders-db")
        self.assertEqual(payload["status"], "degraded")

    def test_unknown_or_injected_service_is_rejected(self) -> None:
        for bad_name in ["prod-billing-db", "lab-orders-db; rm -rf /", "../etc/passwd", ""]:
            payload = json.loads(check_service_status(bad_name))
            self.assertIn("error", payload)
            self.assertIn("not allowlisted", payload["error"])

    def test_error_limit_clamped_between_one_and_max(self) -> None:
        high = json.loads(get_recent_errors("lab-orders-db", limit=500))
        self.assertEqual(high["limit_applied"], MAX_ERROR_LIMIT)

        low = json.loads(get_recent_errors("lab-orders-db", limit=0))
        self.assertEqual(low["limit_applied"], 1)
        self.assertEqual(low["returned"], 1)

    def test_errors_rejected_for_unknown_service(self) -> None:
        payload = json.loads(get_recent_errors("unknown-service", limit=3))
        self.assertIn("error", payload)


if __name__ == "__main__":
    unittest.main()
