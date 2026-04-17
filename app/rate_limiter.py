import redis
import time
from fastapi import HTTPException
from .config import settings
from fastapi import Depends
from .auth import verify_api_key
r = redis.from_url(settings.REDIS_URL)



def check_rate_limit(user_id: str = Depends(verify_api_key)):
    key = f"rate:{user_id}"
    now = int(time.time())

    pipe = r.pipeline()
    pipe.zadd(key, {now: now})
    pipe.zremrangebyscore(key, 0, now - 60)
    pipe.zcard(key)
    pipe.expire(key, 60)

    _, _, count, _ = pipe.execute()

    if count > settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")