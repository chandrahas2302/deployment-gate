import os
import subprocess
from datetime import datetime
from pathlib import Path

def _run(cmd: str) -> str:
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except Exception:
        return ""

def collect_pipeline_metrics(context: dict) -> dict:
    """
    Collect CI/CD metrics inside API.
    Expects pipeline context from client (branch, is_production, etc.)
    """

    branch = context.get("branch", "")
    is_production = int(branch in ["main", "master"])

    # ---------- Git-based metrics ----------
    first_commit = _run("git rev-list --max-parents=0 HEAD")
    first_date = _run(f"git show -s --format=%ci {first_commit}")

    project_age_days = (
        (datetime.utcnow() - datetime.fromisoformat(first_date[:19])).days
        if first_date else 0
    )

    last_date = _run("git show -s --format=%ci HEAD")
    days_since_last_push = (
        (datetime.utcnow() - datetime.fromisoformat(last_date[:19])).days
        if last_date else 0
    )

    diff = _run("git diff --shortstat HEAD~1")

    avg_file_churn = 0
    if diff:
        try:
            avg_file_churn = int(diff.split()[3]) + int(diff.split()[5])
        except Exception:
            pass

    # ---------- Repo structure metrics ----------
    build_tool_count = int(Path("requirements.txt").exists())

    # ---------- Final payload ----------
    return {
        "total_tasks": context.get("total_tasks", 0),
        "failed_tasks": context.get("failed_tasks", 0),
        "stage_count": context.get("stage_count", 1),
        "task_failure_rate": context.get("task_failure_rate", 0.0),
        "is_production": is_production,
        "project_age_days": project_age_days,
        "days_since_last_push": days_since_last_push,
        "stars_to_forks_ratio": context.get("stars_to_forks_ratio", 1.0),
        "build_tool_count": build_tool_count,
        "uses_legacy_build": context.get("uses_legacy_build", 0),
        "uses_multiple_ides": context.get("uses_multiple_ides", 0),
        "uses_ci_and_submodules": context.get("uses_ci_and_submodules", 0),
        "avg_file_churn": avg_file_churn,
        "new_file_ratio": context.get("new_file_ratio", 0.1),
        "dependency_error_rate": context.get("dependency_error_rate", 0.0),
        "compiler_error_rate": context.get("compiler_error_rate", 0.0),
    }
