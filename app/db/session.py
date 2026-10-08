from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(url= settings.DATABASE_URL)

LocalSession = sessionmaker(bind= engine)

def get_db():
    session = LocalSession()
    
    try:
        yield session
    
    finally:
        session.close()