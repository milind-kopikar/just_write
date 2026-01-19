from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from the backend directory
base_dir = Path(__file__).resolve().parents[1]
env_path = base_dir / '.env'
load_dotenv(env_path)

from .database import engine, Base
from .api import auth, tutor

# Create tables
try:
    print(f"Connecting to database at: {os.getenv('DATABASE_URL')}")
    Base.metadata.create_all(bind=engine)
    print("Database tables verified/created.")
except Exception as e:
    print(f"Warning: creating tables failed with error: {e}")

app = FastAPI(title="Just Write AI Tutor API")

# Configure CORS
# We'll be extremely permissive for local development to get past these Windows network quirks
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://0.0.0.0:3000",
]

# Check .env for any additional origins
env_origins = os.getenv("ALLOWED_ORIGINS", "")
if env_origins:
    extra = [o.strip() for o in env_origins.split(",") if o.strip()]
    for o in extra:
        if o not in allowed_origins:
            allowed_origins.append(o)

print(f"--- CORS CONFIGURATION ---")
print(f"Allowed Origins: {allowed_origins}")
print(f"--------------------------")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    origin = request.headers.get("origin")
    print(f"Incoming {request.method} request to {request.url.path} from origin: {origin}")
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to Just Write AI Tutor API"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tutor.router, prefix="/tutor", tags=["tutor"])
