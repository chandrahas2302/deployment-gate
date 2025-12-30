import requests
from typing import Optional

GITHUB_API = "https://api.github.com"

def gh_get(url: str, token: Optional[str] = None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    r = requests.get(
        f"{GITHUB_API}{url}",
        headers=headers,
        timeout=15
    )
    r.raise_for_status()
    return r.json()
