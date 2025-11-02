# main.py
from fastapi import FastAPI
from auth.router import router as auth_router  # import the auth routes

app = FastAPI(
    title="Healthcare API",
    description="Authentication and user management for healthcare app",
    version="1.0.0"
)

app.include_router(auth_router)

# ✅ simple test route
@app.get("/")
def root():
    return {"message": "Welcome to the Healthcare API!"}
