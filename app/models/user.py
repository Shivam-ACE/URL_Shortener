from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base

class UserModel(Base):
    __tablename__= "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())