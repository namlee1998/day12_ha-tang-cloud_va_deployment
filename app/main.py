from fastapi import FastAPI, Depends, HTTPException
import redis
import json
from pydantic import BaseModel

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget

app = FastAPI()

r = redis.from_url(settings.REDIS_URL)


class AskRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "ok"}
    
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    try:
        r.ping()
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="Redis not ready")


@app.post("/ask")
def ask(
    req: AskRequest,
    user_id: str = Depends(verify_api_key),
    _rate_limit: None = Depends(check_rate_limit),
    _budget: None = Depends(check_budget)
):
    try:
        question = req.question

        # 1. Get history
        key = f"history:{user_id}"
        history = r.lrange(key, 0, -1)
        history = [json.loads(h) for h in history]

        # 2. Fake LLM call
        answer = f"Echo: {question}"

        # 3. Save conversation
        r.rpush(key, json.dumps({"q": question, "a": answer}))
        r.expire(key, 86400)  # TTL 1 day

        # 4. Return response
        return {
            "answer": answer,
            "history_length": len(history) + 1
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
