"""Lab starter script for Chapter 10 (Try It Now).

Parses a backup-retention specification for a fictional lab environment
(Northwind Parts). Input validation is intentionally minimal so you can use
VS Code and GitHub Copilot Agent mode to add validation and unit tests while
reviewing every diff before accepting.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

ALLOWED_FORMATS = ("gzip", "zstd", "none")


@dataclass
class BackupJob:
    """Represents a single lab backup retention job."""

    host_label: str
    retention_days: int
    compression: str
    target_dir: str


def build_backup_job(raw: Dict[str, Any]) -> BackupJob:
    """Create a BackupJob from a raw dictionary.

    Starter version: intentionally skips validation for empty labels,
    out-of-range retention days, unknown compression values, and unsafe
    relative or traversal paths.
    """
    return BackupJob(
        host_label=str(raw["host_label"]),
        retention_days=int(raw["retention_days"]),
        compression=str(raw["compression"]).lower(),
        target_dir=str(raw["target_dir"]),
    )


def format_job_summary(job: BackupJob) -> str:
    """Return a one-line summary for a lab backup manifest."""
    return (
        f"host={job.host_label} "
        f"retention={job.retention_days}d "
        f"compression={job.compression} "
        f"target={job.target_dir}"
    )


if __name__ == "__main__":
    sample_entry = {
        "host_label": "lab-db-01",
        "retention_days": 14,
        "compression": "zstd",
        "target_dir": "/var/backups/lab-db-01",
    }
    job = build_backup_job(sample_entry)
    print(format_job_summary(job))
