from fastapi import FastAPI,HTTPException
from app.schemas import PipelineMetrics, RiskResponse
from inference.model import DeploymentRiskModel
from app.metrics.collector import collect_pipeline_metrics
from app.metrics.schema import PipelineContext
from fastapi import Header
from app.metrics.github_collector import collect_metrics_from_github
import logging

app =FastAPI(
    title = "Deployment Gate- Risk Predicition API",
    description="Predicts deployment failure risk using CI/CD pipeline metrics",
    version="1.0.0"
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try: 
    risk_model = DeploymentRiskModel()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.exception("Model loading failed")
    raise RuntimeError("Failed to load deployment risk mdoel") from e

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/predict", response_model=RiskResponse)
def predict_risk(
    context: PipelineContext,
    authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")

        metrics = collect_metrics_from_github(
            context.model_dump(),
            token
        )

        risk_score = risk_model.predict_risk(metrics)

        decision = (
            "BLOCK" if risk_score >= 0.8
            else "WARN" if risk_score >= 0.6
            else "ALLOW"
        )

        return {
            "risk_score": round(risk_score, 4),
            "decision": decision
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to evaluate deployment risk"
        )
