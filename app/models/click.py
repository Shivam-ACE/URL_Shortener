from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from app.db.base import Base

class ClickModel(Base):
    __tablename__= "clicks"
    
    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey("links.id", ondelete="CASCADE"), nullable=False, index=True)
    clicked_at = Column(DateTime, server_default=func.now())
    ip_address = Column(String)
    user_agent = Column(Text)
    referer = Column(String)