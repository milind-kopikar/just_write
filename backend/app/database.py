import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load backend/.env
base_dir = Path(__file__).resolve().parents[1]
env_path = base_dir / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# Updated with user-provided credentials
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://milind:Rahul1978!@127.0.0.1:5432/just_write")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"connect_timeout": 10}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
