# deployment gate 
Traditional CI/CD pipelines rely on static checks (tests, linting, coverage).
This project introduces an intelligent risk layer that evaluates deployment risk dynamically based on historical failures, pipeline structure, and repository health.

Outcome:
Deployments are automatically ALLOWED, WARNED, or BLOCKED before reaching production.

🏗️ Architecture
GitHub Push / Manual Trigger
        ↓
GitHub Actions (CI)
        ↓
Deployment Gate API (FastAPI + Auth)
        ↓
Metrics Collection
   ├── GitHub Repository Metrics
   └── CI / Pipeline Metrics
        ↓
ML Risk Prediction Model
        ↓
Decision Engine
(ALLOW / WARN / BLOCK)
        ↓
Deployment Continues or Stops

🧰 Tech Stack
🔹 CI / DevOps

GitHub Actions – CI execution & deployment gating

Git – Version control (rebase-based workflow)

Render – Cloud hosting & auto-deployments

🔹 Backend

FastAPI – REST API framework

Uvicorn – ASGI server

Pydantic – Strict schema validation

🔹 Machine Learning

scikit-learn – Deployment risk model

joblib – Model serialization

pandas / NumPy – Feature processing

🔹 Security

API Key Authentication – Secures Deployment Gate API

GitHub Personal Access Token (PAT) – Authenticated GitHub API access (rate-limit safe)

🔐 Security Model

API protected using Bearer API Key

Secrets managed via:

GitHub Actions Secrets

Render Environment Variables

Fail-closed CI design

API failure → ❌ deployment blocked

Schema validation failure → ❌ blocked

Unauthorized request → ❌ blocked

📥 Input Schema (from CI)

GitHub Actions sends pipeline context to the API:

{
  "repo": "owner/repository",
  "branch": "main",
  "run_id": "123456789",
  "sha": "commit_sha"
}


Validated strictly using Pydantic.

📊 Metrics Collected
🔹 GitHub Repository Metrics

Workflow job count

Failed jobs

Commit history

Project age

Days since last push

Stars-to-forks ratio

Production branch detection

🔹 CI / Pipeline Metrics

Stage count

Build tool detection

File churn

Legacy build usage

Dependency error rate

Compiler error rate

CI structure heuristics

Metrics from both sources are merged before ML inference.

🧠 Machine Learning Model

Trained on historical CI/CD and repository signals

Outputs a risk probability (0–1)

Feature alignment strictly enforced

Defensive checks prevent inference on missing features

🚦 Decision Logic
Risk ≥ 0.8  → BLOCK
Risk ≥ 0.6  → WARN
Risk < 0.6  → ALLOW


Decision is enforced directly in CI.

⚙️ GitHub Actions Integration

Workflow location:

.github/workflows/ci.yml


Responsibilities:

Trigger on push or manual run

Call Deployment Gate API

Parse risk decision

Fail pipeline automatically if decision = BLOCK

🚀 Deployment
Backend (Render)

Auto-deployed on GitHub push

Environment variables:

DEPLOYMENT_GATE_API_KEY (required)

GITHUB_TOKEN (recommended)

CI Pipeline

Uses GitHub Actions

Secrets injected securely at runtime

🧪 Health Check
GET /health


Response:

{ "status": "ok" }

📦 Example API Response
{
  "risk_score": 0.34,
  "decision": "ALLOW"
}

🛡️ Failure Handling
Scenario	Result
Invalid schema	❌ Blocked
Missing auth	❌ Blocked
GitHub API rate limit	❌ Blocked
Feature mismatch	❌ Blocked
API failure	❌ Blocked

No unsafe deployment can bypass the gate.
