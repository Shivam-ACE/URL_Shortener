from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.models.user import UserModel
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: EmailStr):
    user = db.query(UserModel).filter(UserModel.email==email).first()
    return user

def get_user_by_id(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id==user_id).first()
    return user
    
def register_user(db: Session, body: UserCreate):
    
    if get_user_by_email(db, body.email):
        return None

    hash_pass = hash_password(body.password)
    
    new_user = UserModel(email= body.email, hashed_password= hash_pass)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def authenticate_user(db: Session, email: EmailStr, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user