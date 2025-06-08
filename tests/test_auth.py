from fastapi.testclient import TestClient
from src.main import app # Assuming your FastAPI app instance is named 'app' in src/main.py
from src.auth import crud, security, models # For direct manipulation if needed
from src.core.config import settings

client = TestClient(app)

# Helper to clear the in-memory DB for tests
def clear_fake_db():
    crud.fake_users_db.clear()

def test_read_main_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Simple Auth API. Visit /docs for API documentation."}

def test_register_user_success():
    clear_fake_db()
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword", "full_name": "Test User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data # Ensure password is not returned
    assert crud.get_user_by_username("testuser") is not None

def test_register_user_duplicate_username():
    clear_fake_db()
    # First registration
    client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test1@example.com", "password": "testpassword"},
    )
    # Attempt to register again with same username
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test2@example.com", "password": "anotherpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_register_user_duplicate_email():
    clear_fake_db()
    # First registration
    client.post(
        "/auth/register",
        json={"username": "testuser1", "email": "test@example.com", "password": "testpassword"},
    )
    # Attempt to register again with same email
    response = client.post(
        "/auth/register",
        json={"username": "testuser2", "email": "test@example.com", "password": "anotherpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success():
    clear_fake_db()
    # Register user first
    client.post(
        "/auth/register",
        json={"username": "loginuser", "email": "login@example.com", "password": "loginpass"},
    )
    # Login
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "loginpass"}, # Form data
        headers={"Content-Type": "application/x-www-form-urlencoded"} # Important for form data
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure_wrong_password():
    clear_fake_db()
    client.post(
        "/auth/register",
        json={"username": "loginuserfail", "email": "loginfail@example.com", "password": "correctpass"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "loginuserfail", "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_failure_user_not_exist():
    clear_fake_db()
    response = client.post(
        "/auth/login",
        data={"username": "nonexistentuser", "password": "anypass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401

def test_get_users_me_success():
    clear_fake_db()
    # Register and login to get token
    client.post(
        "/auth/register",
        json={"username": "me_user", "email": "me@example.com", "password": "mepass", "full_name": "Me Myself"},
    )
    login_response = client.post(
        "/auth/login",
        data={"username": "me_user", "password": "mepass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    access_token = login_response.json()["access_token"]

    # Access protected route
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "me_user"
    assert data["email"] == "me@example.com"
    assert data["full_name"] == "Me Myself"

def test_get_users_me_unauthorized_no_token():
    clear_fake_db()
    response = client.get("/users/me")
    assert response.status_code == 401 # FastAPI's default for missing auth
    assert response.json()["detail"] == "Not authenticated" # Or "Could not validate credentials"

def test_get_users_me_unauthorized_invalid_token():
    clear_fake_db()
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_get_users_me_disabled_user():
    clear_fake_db()
    # Register user and "disable" them (manually for this test)
    user_data = {"username": "disabled_user", "email": "disabled@example.com", "password": "disabledpass"}
    client.post("/auth/register", json=user_data)
    
    # Manually disable user in the fake_db
    db_user = crud.get_user_by_username(user_data["username"])
    if db_user:
        db_user.disabled = True
        crud.fake_users_db[user_data["username"]] = db_user # Update in DB

    # Login to get token for the now disabled user
    login_response = client.post(
        "/auth/login",
        data={"username": user_data["username"], "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200 # Login still works
    access_token = login_response.json()["access_token"]

    # Attempt to access protected route
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Inactive user"