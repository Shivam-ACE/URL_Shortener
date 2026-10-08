from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

from app.models.click import ClickModel
from app.models.link import LinkModel
from app.models.user import UserModel

from app.api.auth import auth_routes
from app.api.links import link_routes
from app.api.redirect import redirect_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener", version="1.0.0")

app.include_router(auth_routes)
app.include_router(link_routes)
app.include_router(redirect_routes)

@app.get("/health")
def health():
    return {"Status": "200 OK"}