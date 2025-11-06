# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router  # import the auth routes

app = FastAPI(
    title="Healthcare API",
    description="Authentication and user management for healthcare app",
    version="1.0.0"
)

app = FastAPI()

# ✅ Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- Allow all domains
    allow_credentials=True,
    allow_methods=["*"],  # <-- Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # <-- Allow all headers
)

app.include_router(auth_router)

# ✅ simple test route
@app.get("/")
def root():
    return {"message": "Welcome to the Healthcare API!"}
