from datetime import datetime

from pydantic import BaseModel, ConfigDict

class ClickResponse(BaseModel):
    id: int
    link_id: int
    clicked_at: datetime
    ip_address: str | None = None
    user_agent: str | None = None
    referer: str | None = None
    
    model_config = ConfigDict(from_attributes=True)
    
class LinkStatsResponse(BaseModel):
    link_id: int
    short_code: str
    original_url: str
    total_clicks: int
    clicks: list[ClickResponse]