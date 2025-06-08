from typing import Annotated
from fastapi import APIRouter, Depends

from src.auth import models, security

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=models.User)
async def read_users_me(
    current_user: Annotated[models.User, Depends(security.get_current_active_user)]
):
    """
    Get current authenticated user's details.
    Requires authentication.
    """
    return current_user