from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Optional: For Frontend integration

from src.routers import auth_routes, users_routes
# from src.db.database import create_db_and_tables # Uncomment if using SQLite and want to create tables on startup

app = FastAPI(
    title="Simple Auth API",
    description="A basic Authentication API using FastAPI and JWT.",
    version="0.1.0"
)

# Optional: Add CORS middleware if you plan to call this API from a frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     # allow_origins=["http://localhost:3000"], # Or specify your frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# @app.on_event("startup")
# def on_startup():
#     # Create database tables if they don't exist (only for DBs like SQLite)
#     # create_db_and_tables() # Uncomment if using SQLite
#     pass


app.include_router(auth_routes.router)
app.include_router(users_routes.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Simple Auth API. Visit /docs for API documentation."}

# To run the app (from the root directory simple-auth-api-python/):
# uvicorn src.main:app --reload