from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.link_service import get_link_by_code
from app.services.click_service import record_click
from app.core.cache import get_cached_link, cache_link

redirect_routes = APIRouter(tags=["Redirect"])

@redirect_routes.get("/{code}")
def redirect_to_original(code: str, request: Request, background_tasks: BackgroundTasks, db: Session= Depends(get_db)):
    # link = get_link_by_code(db, code)
    
    # if link is None or not link.is_active:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found..")
    
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    referer = request.headers.get("referer")
    
    cached = get_cached_link(code)
    
    if cached:
        link_id = cached["id"]
        original_url = cached["original_url"]
    else:
        link = get_link_by_code(db, code)
        
        if link is None or not link.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found..")
        
        link_id = link.id
        original_url = link.original_url
        cache_link(code, link_id, original_url)
            
    background_tasks.add_task(record_click, link_id, ip_address, user_agent, referer)
    
    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)