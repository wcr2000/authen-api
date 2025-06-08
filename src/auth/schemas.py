from pydantic import BaseModel, EmailStr
from typing import Optional

from .models import UserBase # Import UserBase to avoid repetition

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel): # Not directly used as input model, FastAPI's OAuth2PasswordRequestForm is used
    username: str
    password: str