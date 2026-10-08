from fastapi import APIRouter, Depends, status, HTTPException
from app.services import user_service
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.models.user import UserModel

auth_routes = APIRouter(prefix="/auth", tags=["Auth"])

@auth_routes.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(body: UserCreate, db: Session= Depends(get_db)):
    new_user = user_service.register_user(db, body)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists..")

    return new_user

@auth_routes.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(body: UserCreate, db: Session= Depends(get_db)):
    user = user_service.authenticate_user(db, body.email, body.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials..")
    
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@auth_routes.get("/me", response_model=UserResponse)
def me(user: UserModel= Depends(get_current_user)):
    return user