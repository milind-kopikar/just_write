import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load backend/.env
base_dir = Path(__file__).resolve().parent
env_path = base_dir / '.env'
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Testing connection to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        print("Successfully connected to the database!")
        result = conn.execute("SELECT 1")
        print(f"Query Result: {result.fetchone()}")
except Exception as e:
    print(f"FAILED to connect: {e}")
