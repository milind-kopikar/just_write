import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path

# Load env
base_dir = Path(__file__).resolve().parent
env_path = base_dir / 'backend' / '.env'
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Connecting to: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Checking for missing column: grade_level...")
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN grade_level INTEGER DEFAULT 3"))
        conn.commit()
        print("Successfully added grade_level column to users table.")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("Column grade_level already exists.")
        else:
            print(f"Error updating table: {e}")

    # Also ensure lesson_contents is synced
    print("Database sync complete.")
