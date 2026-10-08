from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from app.db.base import Base

class LinkModel(Base):
    __tablename__="links"
    
    id = Column(Integer, primary_key=True)
    original_url = Column(Text, nullable=False) ##text since urls can be long
    short_code = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)