"""Starter pytest suite for Chapter 10 (Try It Now).

Run from this directory with:
    pytest -v
"""

from backup_manifest import BackupJob, build_backup_job, format_job_summary


def test_build_backup_job_happy_path() -> None:
    """Valid lab input produces a normalized BackupJob."""
    raw = {
        "host_label": "lab-db-01",
        "retention_days": 14,
        "compression": "ZSTD",
        "target_dir": "/var/backups/lab-db-01",
    }
    job = build_backup_job(raw)
    assert job == BackupJob(
        host_label="lab-db-01",
        retention_days=14,
        compression="zstd",
        target_dir="/var/backups/lab-db-01",
    )


def test_format_job_summary_contains_expected_fields() -> None:
    """Summary string formats all four backup job fields cleanly."""
    job = BackupJob(
        host_label="lab-web-02",
        retention_days=7,
        compression="gzip",
        target_dir="/var/backups/lab-web-02",
    )
    summary = format_job_summary(job)
    assert summary == (
        "host=lab-web-02 retention=7d compression=gzip "
        "target=/var/backups/lab-web-02"
    )
