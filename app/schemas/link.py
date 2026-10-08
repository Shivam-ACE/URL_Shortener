from pydantic import BaseModel, HttpUrl
from datetime import datetime

class LinkCreate(BaseModel):
    original_url: HttpUrl

class LinkResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    user_id: int
    is_active: bool
    created_at: datetime