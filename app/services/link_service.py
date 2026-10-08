from sqlalchemy.orm import Session

from app.core.base62 import encode_id
from app.models.link import LinkModel
from app.schemas.link import LinkCreate

def create_link(db: Session, data: LinkCreate, user_id: int):
    link = LinkModel(original_url=str(data.original_url), user_id=user_id)
    
    db.add(link)
    db.flush()  ### flush() sends the INSERT and assigns the id, but keeps the transaction open — commit() is what makes it permanent
    
    link.short_code = encode_id(link.id)
    
    db.commit()
    db.refresh(link)
    return link

def get_link_by_code(db: Session, code: str):
    return db.query(LinkModel).filter(LinkModel.short_code == code).first()

def get_link_by_id(db: Session, link_id: int):
    return db.query(LinkModel).filter(LinkModel.id == link_id).first()

def get_links_by_user(db: Session, user_id: int):
    return (
        db.query(LinkModel)
        .filter(LinkModel.user_id == user_id)
        .order_by(LinkModel.created_at.desc())
        .all()
    )
    
def deactivate_link(db: Session, link: LinkModel):
    link.is_active = False
    db.commit()
    db.refresh(link)
    return link