# Simple Authentication API (Python/FastAPI)

## Project Overview
This project provides a basic Authentication API (Register, Login, Protected Route) using JSON Web Tokens (JWTs). It's designed to demonstrate understanding of product integration layers, specifically API creation and authentication mechanisms, which are crucial for integrating AI models into SaaS environments or other applications.

## Features
- User registration (with password hashing).
- User login (returning a JWT).
- JWT generation and validation for securing endpoints.
- A protected endpoint (`/users/me`) that requires authentication.
- In-memory "database" (Python dictionary) for simplicity.

## Technologies Used
- Python 3.8+
- FastAPI: Modern, fast (high-performance) web framework for building APIs.
- Pydantic: Data validation and settings management using Python type annotations.
- passlib: For secure password hashing (using bcrypt).
- python-jose: For encoding, decoding, and verifying JWTs.
- python-dotenv: For managing environment variables.
- Uvicorn: ASGI server for running FastAPI applications.

## Setup Instructions
1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd simple-auth-api-python
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    Copy the `.env.example` file to a new file named `.env`:
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file and **change the `SECRET_KEY`** to a strong, unique secret.
    ```
    SECRET_KEY="your-very-strong-and-unique-secret-key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

## How to Run
Ensure your virtual environment is activated and you are in the `simple-auth-api-python` root directory.
Run the FastAPI application using Uvicorn:
```bash
uvicorn src.main:app --reload