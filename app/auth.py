from fastapi import Header, HTTPException
from .config import settings


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return "user1"   # hoặc map từ key → user_id