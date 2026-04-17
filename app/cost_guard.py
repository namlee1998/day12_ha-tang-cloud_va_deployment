import redis
from fastapi import HTTPException
from datetime import datetime
from .config import settings
from fastapi import Depends
from .auth import verify_api_key

r = redis.from_url(settings.REDIS_URL)


def check_budget(user_id: str = Depends(verify_api_key)):
    month = datetime.utcnow().strftime("%Y-%m")
    key = f"cost:{user_id}:{month}"

    cost = r.get(key)
    cost = float(cost) if cost else 0.0

    if cost > settings.MONTHLY_BUDGET_USD:
        raise HTTPException(status_code=402, detail="Budget exceeded")

    # giả lập mỗi request = $0.01
    r.incrbyfloat(key, 0.01)