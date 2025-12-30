import logging
import os
from fastapi import FastAPI, HTTPException, Depends

from app.schemas import RiskResponse
from app.metrics.schema import PipelineContext
from app.metrics.github_collector import collect_metrics_from_github
from inference.model import DeploymentRiskModel
from auth import verify_api_key

app = FastAPI(
    title="Deployment Gate - Risk Prediction API",
    description="Predicts deployment failure risk using CI/CD pipeline metrics",
    version="1.0.0",
)

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Load ML Model ----------
try:
    risk_model = DeploymentRiskModel()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.exception("Model loading failed")
    raise RuntimeError("Failed to load deployment risk model") from e


# ---------- Health Check ----------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Prediction Endpoint ----------
@app.post("/predict", response_model=RiskResponse)
def predict_risk(
    context: PipelineContext,
    _: None = Depends(verify_api_key),  # API authorization only
):
    try:
        # Optional GitHub token (can be None)
        github_token = os.getenv("GITHUB_TOKEN")

        metrics = collect_metrics_from_github(
            context.model_dump(),
            token=github_token
        )

      


        risk_score = risk_model.predict_risk(metrics)

        decision = (
            "BLOCK" if risk_score >= 0.8
            else "WARN" if risk_score >= 0.6
            else "ALLOW"
        )

        return {
            "risk_score": round(float(risk_score), 4),
            "decision": decision,
        }

    except Exception as e:
        logger.exception("Risk evaluation failed")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
