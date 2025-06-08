from typing import Optional, Dict
from . import models, schemas, security

# In-memory "database"
# For a real application, replace this with a proper database (e.g., PostgreSQL, MySQL, SQLite)
# The key is the username, and the value is a UserInDB object.
fake_users_db: Dict[str, models.UserInDB] = {}


def get_user_by_username(username: str) -> Optional[models.UserInDB]:
    if username in fake_users_db:
        return fake_users_db[username]
    return None

def create_user(user_create: schemas.UserCreate) -> models.UserInDB:
    hashed_password = security.get_password_hash(user_create.password)
    user_in_db = models.UserInDB(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        disabled=user_create.disabled if user_create.disabled is not None else False,
        hashed_password=hashed_password,
    )
    fake_users_db[user_in_db.username] = user_in_db
    return user_in_db

def authenticate_user(username: str, password: str) -> Optional[models.UserInDB]:
    user = get_user_by_username(username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user