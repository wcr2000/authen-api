from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import schemas, crud, security, models
from src.core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=models.User, status_code=status.HTTP_201_CREATED)
async def register_user(user_create: schemas.UserCreate):
    db_user = crud.get_user_by_username(username=user_create.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    email_user = None # Simplistic check, real app might query DB differently for email
    for _, u in crud.fake_users_db.items():
        if u.email == user_create.email:
            email_user = u
            break
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    created_user = crud.create_user(user_create=user_create)
    # Return User model, not UserInDB (to exclude password)
    return models.User(**created_user.model_dump())


@router.post("/login", response_model=models.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = crud.authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}