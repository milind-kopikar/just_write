"""
startup.py — runs before uvicorn on every Railway deploy.

Tasks:
  1. Ensure all DB tables exist.
  2. Seed lesson content and prompts if the DB is empty.
  3. Fetch and store YouTube transcripts for any video that doesn't have one yet.

Everything here is idempotent: it checks before writing, so re-deploying is safe.
"""

import sys
import os
from pathlib import Path

# Make sure both the backend package and the scripts folder are importable.
backend_dir = Path(__file__).resolve().parent          # .../backend
project_dir = backend_dir.parent                       # .../just_write
scripts_dir = project_dir / "scripts"

sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(scripts_dir))

from app.database import SessionLocal, engine
from app.models import Base, LessonContent, VideoTranscript


def ensure_tables():
    print("[startup] Creating / verifying database tables...")
    Base.metadata.create_all(bind=engine)
    print("[startup] Tables OK.")


def seed_if_empty(db):
    count = db.query(LessonContent).count()
    if count > 0:
        print(f"[startup] Lesson content already seeded ({count} rows). Skipping seed.")
        return

    print("[startup] lesson_contents table is empty — running seed...")
    from seed_lessons_v2 import seed_data
    seed_data()
    print("[startup] Seed complete.")


def fetch_missing_transcripts(db):
    from seed_lessons_v2 import CURATED_VIDEOS
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

    unique_ids: set[str] = set()
    for topics in CURATED_VIDEOS.values():
        unique_ids.update(topics.values())

    missing = [
        vid for vid in unique_ids
        if not db.query(VideoTranscript).filter_by(video_id=vid).first()
    ]

    if not missing:
        print(f"[startup] All {len(unique_ids)} transcripts already in database. Skipping fetch.")
        return

    print(f"[startup] Fetching {len(missing)} missing transcript(s)...")
    api = YouTubeTranscriptApi()

    for vid in missing:
        try:
            segments = api.fetch(vid)
            text = " ".join(seg.text for seg in segments)
            db.add(VideoTranscript(video_id=vid, transcript_text=text))
            db.commit()
            print(f"[startup]   Saved transcript for {vid} ({len(text.split())} words).")
        except (NoTranscriptFound, TranscriptsDisabled):
            print(f"[startup]   No transcript available for {vid} — skipping.")
        except Exception as e:
            print(f"[startup]   Error fetching {vid}: {e}")

    print("[startup] Transcript fetch complete.")


def main():
    ensure_tables()
    db = SessionLocal()
    try:
        seed_if_empty(db)
        fetch_missing_transcripts(db)
    finally:
        db.close()
    print("[startup] All startup tasks done. Handing off to uvicorn.")


if __name__ == "__main__":
    main()
