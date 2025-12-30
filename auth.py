import os
from fastapi import Header, HTTPException

API_KEY = os.getenv("DEPLOYMENT_GATE_API_KEY")

def verify_api_key(authorization: str = Header(...)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API key")
