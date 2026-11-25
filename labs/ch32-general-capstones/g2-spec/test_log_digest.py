#!/usr/bin/env python3
"""Unit tests for Capstone G2 starter_log_digest.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from starter_log_digest import normalize_error_line, summarize_lines


class TestLogDigest(unittest.TestCase):
    def test_normalize_strips_iso_timestamp(self) -> None:
        line = "2026-11-24T04:12:00Z [ERROR] lab-db-01 archive_command failed"
        self.assertEqual(
            normalize_error_line(line),
            "[ERROR] lab-db-01 archive_command failed",
        )

    def test_summarize_counts_and_top_errors(self) -> None:
        sample = [
            "2026-11-24T04:00:00Z [INFO] Backup started",
            "2026-11-24T04:01:00Z [WARN] Disk at 78 percent",
            "2026-11-24T04:02:00Z [ERROR] Timeout reaching lab-api-01",
            "2026-11-24T04:03:00Z [ERROR] Timeout reaching lab-api-01",
            "2026-11-24T04:04:00Z [ERROR] Auth token expired",
            "",
            "Unformatted diagnostic note",
        ]
        result = summarize_lines(sample, top_n=1)
        self.assertEqual(result["total_lines"], 6)
        self.assertEqual(result["counts"], {"ERROR": 3, "WARN": 1, "INFO": 1, "OTHER": 1})
        self.assertEqual(
            result["top_errors"],
            [{"message": "[ERROR] Timeout reaching lab-api-01", "count": 2}],
        )

    def test_invalid_top_raises(self) -> None:
        with self.assertRaises(ValueError):
            summarize_lines([], top_n=0)

    def test_cli_json_output(self) -> None:
        script = Path(__file__).parent / "starter_log_digest.py"
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "sample.log"
            log_path.write_text("2026-11-24T05:00:00Z [ERROR] sample failure\n", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(script), "--file", str(log_path), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            parsed = json.loads(proc.stdout)
            self.assertEqual(parsed["counts"]["ERROR"], 1)


if __name__ == "__main__":
    unittest.main()
