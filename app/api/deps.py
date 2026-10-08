from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.orm import Session
from redis.exceptions import RedisError

from app.core.config import settings
from app.db.session import get_db
from app.services.user_service import get_user_by_id
from app.models.user import UserModel
from app.core.cache import redis_client

scheme = HTTPBearer(auto_error=False)
exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials..", headers={"WWW-Authenticate": "Bearer"})

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(scheme), db: Session = Depends(get_db)):
    if credentials is None:
        raise exception
    
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except jwt.InvalidTokenError:
        raise exception
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise exception
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise exception
          
    user = get_user_by_id(db, user_id)

    if user is None:
        raise exception
    return user

def rate_limit(max_requests: int, window_seconds: int):
    def dependency(
        request: Request,
        current_user: UserModel = Depends(get_current_user)
    ):
        key = f"limit:{current_user.id}:{request.url.path}"
        
        try:
            pipe = redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, window_seconds, nx=True)
            count, _ = pipe.execute()
        except RedisError:
            return
        
        if count > max_requests:
            ttl = redis_client.ttl(key)
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests, slow down", headers={"Retry-After": str(ttl if ttl > 0 else window_seconds)})
        
    return dependency