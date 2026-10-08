import json

import redis
from redis.exceptions import RedisError

from app.core.config import settings

redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)

CACHE_TTL_SECONDS = 3600


def _cache_key(code: str):
    return f"link:{code}"


def get_cached_link(code: str):
    try:
        raw = redis_client.get(_cache_key(code))
    except RedisError:
        return None

    if raw is None:
        return None

    try:
        return json.loads(raw)
    except ValueError:
        return None


def cache_link(code: str, link_id: int, original_url: str) -> None:
    payload = json.dumps({"id": link_id, "original_url": original_url})
    try:
        redis_client.setex(_cache_key(code), CACHE_TTL_SECONDS, payload)
    except RedisError:
        pass


def delete_cached_link(code: str) -> None:
    try:
        redis_client.delete(_cache_key(code))
    except RedisError:
        pass
