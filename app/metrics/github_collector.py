from app.github.client import gh_get
from datetime import datetime

def collect_metrics_from_github(ctx: dict, token: str) -> dict:
    owner, repo = ctx["repo"].split("/")

    # Workflow jobs
    jobs = gh_get(
        f"/repos/{owner}/{repo}/actions/runs/{ctx['run_id']}/jobs",
        token
    )["jobs"]

    total_tasks = len(jobs)
    failed_tasks = sum(1 for j in jobs if j["conclusion"] == "failure")

    # Commits
    commits = gh_get(
        f"/repos/{owner}/{repo}/commits?sha={ctx['branch']}&per_page=20",
        token
    )

    # Repo metadata
    repo_meta = gh_get(f"/repos/{owner}/{repo}", token)

    created = datetime.fromisoformat(repo_meta["created_at"][:-1])
    pushed = datetime.fromisoformat(repo_meta["pushed_at"][:-1])

    return {
        "total_tasks": total_tasks,
        "failed_tasks": failed_tasks,
        "task_failure_rate": failed_tasks / total_tasks if total_tasks else 0.0,
        "commit_count": len(commits),
        "project_age_days": (datetime.utcnow() - created).days,
        "days_since_last_push": (datetime.utcnow() - pushed).days,
        "stars_to_forks_ratio": (
            repo_meta["stargazers_count"] /
            max(repo_meta["forks_count"], 1)
        ),
        "is_production": int(ctx["branch"] in ["main", "master"])
    }
