from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, rate_limit

from app.db.session import get_db

from app.models.user import UserModel
from app.models.link import LinkModel

from app.schemas.link import LinkCreate, LinkResponse
from app.schemas.click import LinkStatsResponse

from app.services.link_service import create_link, get_link_by_id, get_links_by_user, deactivate_link
from app.services.click_service import get_clicks_for_link

from app.core.cache import delete_cached_link

link_routes = APIRouter(prefix="/links", tags=["Links"])

@link_routes.post("/", response_model=LinkResponse, status_code= status.HTTP_201_CREATED, dependencies=[Depends(rate_limit(10, 60))])
def shorten_link(data: LinkCreate, db: Session= Depends(get_db), current_user: UserModel= Depends(get_current_user)):
    return create_link(db, data, current_user.id)

@link_routes.get("/{link_id}/stats", response_model=LinkStatsResponse)
def link_stats(link_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    link = get_link_by_id(db, link_id)
    
    if link is None or link.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found..")
    
    clicks = get_clicks_for_link(db, link.id)
    
    return LinkStatsResponse(
        link_id=link.id,
        short_code=link.short_code,
        original_url=link.original_url,
        total_clicks=len(clicks),
        clicks=clicks
        )
    
@link_routes.get("/", response_model=list[LinkResponse])
def get_links(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return get_links_by_user(db, current_user.id)

@link_routes.patch("/{link_id}/deactivate", response_model=LinkResponse)
def deactivate_my_link(link_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    link = get_link_by_id(db, link_id)
    
    if link is None or link.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found..")
    
    updated = deactivate_link(db, link)
    delete_cached_link(link.short_code)
    return updated