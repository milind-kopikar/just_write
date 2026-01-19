import sqlalchemy
from sqlalchemy import create_engine
import os
from pathlib import Path
from dotenv import load_dotenv

# Explicitly load backend/.env
base_dir = Path(__file__).resolve().parents[0] # assuming run from project root
env_path = base_dir / 'backend' / '.env'
if env_path.exists():
    load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://milind:Rahul1978!@localhost:5432/just_write")

print(f"Testing connection to: {DATABASE_URL}")
try:
    engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 5})
    with engine.connect() as conn:
        print("Successfully connected to the database!")
except Exception as e:
    print(f"Database connection failed: {e}")
