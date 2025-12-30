import requests

GITHUB_API = "https://api.github.com"

def gh_get(url, token):
    r = requests.get(
        f"{GITHUB_API}{url}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        },
        timeout=15
    )
    r.raise_for_status()
    return r.json()
