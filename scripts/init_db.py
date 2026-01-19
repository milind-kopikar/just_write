import os
import sys
from pathlib import Path

# Add the backend directory to sys.path so we can import from app
backend_path = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(backend_path))

from app.database import engine, Base
from app.models import User, StudentScore, WritingProject

def init_db():
    print("Connecting to database and creating tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Successfully created all tables!")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
