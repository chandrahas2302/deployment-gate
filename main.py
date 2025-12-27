from fastapi import FastAPI,HTTPException
from app.schemas import PipelineMetrics, RiskResponse
from inference.model import DeploymentRiskModel
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
def predict_risk(metrics: PipelineMetrics):
    try:
        risk_score = risk_model.predict_risk(metrics.model_dump())

        decision = (
            "BLOCK" if risk_score >= 0.8
            else "WARN" if risk_score >= 0.6
            else "ALLOW"
        )

        logger.info(
            f"Prediction completed | risk_score={risk_score:.4f} | decision={decision}"
        )

        return RiskResponse(
            risk_score=round(risk_score, 4),
            decision=decision
        )

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction"
        )
