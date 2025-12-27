import joblib
import pandas as pd 
from pathlib import Path 
from typing import Dict
import logging

logger = logging.getLogger(__name__)
MODEL_PATH = Path("model/deployment_gate_model.joblib")

class DeploymentRiskModel:
    def __init__(self):
        bundle = joblib.load(MODEL_PATH)
        self.model= bundle["model"]
        self.features = bundle["features"]
    
    def predict_risk(self, metrics: Dict[str, float]) -> float:
        """
        Input: pipeline metrics dict
        Output: risk score (0-1)
        """
        X = pd.DataFrame([metrics])
        logger.error(f"Incoming keys: {list(X.columns)}")
        logger.error(f"Expected features: {self.features}")

        # Ensure correct feature order
        X = X[self.features]

        risk_score: float = float(self.model.predict_proba(X)[0][1])
        return risk_score
        