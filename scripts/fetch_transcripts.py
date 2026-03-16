"""
fetch_transcripts.py
--------------------
Downloads YouTube transcripts for every curated video and stores them in the
video_transcripts table. Run this once after seeding lessons, and again any
time new videos are added to CURATED_VIDEOS in seed_lessons_v2.py.

Usage (from the project root):
    pip install youtube-transcript-api   # already in requirements.txt
    python scripts/fetch_transcripts.py
"""

import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(backend_dir))

from app.database import SessionLocal, engine
from app.models import VideoTranscript, Base
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# ---------------------------------------------------------------------------
# Import the same CURATED_VIDEOS dict so this script stays in sync
# with seed_lessons_v2.py automatically.
# ---------------------------------------------------------------------------
sys.path.append(str(Path(__file__).resolve().parent))
from seed_lessons_v2 import CURATED_VIDEOS

Base.metadata.create_all(bind=engine)


def fetch_transcript(video_id: str) -> str | None:
    """Return the full transcript text for a YouTube video ID, or None."""
    try:
        segments = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(seg["text"] for seg in segments)
    except (NoTranscriptFound, TranscriptsDisabled):
        print(f"  [SKIP] No transcript available for {video_id}")
        return None
    except Exception as e:
        print(f"  [ERROR] {video_id}: {e}")
        return None


def run():
    db = SessionLocal()
    try:
        # Collect all unique video IDs across grades and topics
        unique_ids: set[str] = set()
        for topics in CURATED_VIDEOS.values():
            unique_ids.update(topics.values())

        print(f"Found {len(unique_ids)} unique video IDs to process.\n")

        saved = 0
        skipped = 0
        failed = 0

        for video_id in sorted(unique_ids):
            existing = db.query(VideoTranscript).filter_by(video_id=video_id).first()
            if existing:
                print(f"  [EXISTS] {video_id} — already in database, skipping.")
                skipped += 1
                continue

            print(f"  [FETCH]  {video_id} ...")
            text = fetch_transcript(video_id)

            if text:
                db.add(VideoTranscript(video_id=video_id, transcript_text=text))
                db.commit()
                word_count = len(text.split())
                print(f"           Saved ({word_count} words).")
                saved += 1
            else:
                failed += 1

        print(f"\nDone. Saved: {saved}  |  Skipped (already existed): {skipped}  |  Failed/no transcript: {failed}")
    except Exception as e:
        db.rollback()
        print(f"Fatal error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()
