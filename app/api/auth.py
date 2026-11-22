from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token
from app.services.user_service import (
    get_user_by_username,
    get_user_by_email,
    create_user,
    authenticate_user
)
from app.services.auth_service import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    if get_user_by_email(db, str(user_data.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    user = create_user(db, user_data)

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(
        db,
        user_data.username,
        user_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
