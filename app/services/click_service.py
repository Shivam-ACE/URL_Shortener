from sqlalchemy.orm import Session

from app.db.session import LocalSession
from app.models.click import ClickModel

def record_click(link_id: int, ip_address: str | None, user_agent: str | None, referer: str |None):
    db = LocalSession()
    try:
        click = ClickModel(link_id= link_id, ip_address = ip_address, user_agent = user_agent, referer = referer)
        db.add(click)
        db.commit()
    finally:
        db.close()
        
def get_clicks_for_link(db: Session, link_id: int):
    return (
        db.query(ClickModel)
        .filter(ClickModel.link_id == link_id)
        .order_by(ClickModel.clicked_at.desc())
        .all()
    )