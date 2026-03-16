"""
startup.py — runs before uvicorn on every Railway deploy.

Tasks:
  1. Ensure all DB tables exist.
  2. Seed lesson content and prompts if the DB is empty.
  3. Fetch and store YouTube transcripts for any video that doesn't have one yet.

Everything here is idempotent: it checks before writing, so re-deploying is safe.
Self-contained: no imports from the scripts/ folder (not available on Railway).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal, engine
from app.models import Base, LessonContent, Prompt, VideoTranscript

# ---------------------------------------------------------------------------
# Curated videos — keep in sync with scripts/seed_lessons_v2.py
# ---------------------------------------------------------------------------
CURATED_VIDEOS = {
    3: {
        "Narrative":     "v3etaclybPE",
        "Informational": "DN4d76QP_MA",
        "Persuasive":    "7kYtkqfXMOg",
    },
    4: {
        "Narrative":     "N038mVBgHt8",
        "Informational": "68m897M7_6M",
        "Persuasive":    "X6QQqIXXL_0",
        "TDA":           "B-fSL1VAyIc",
    },
    5: {
        "Narrative":     "jVzAEodKF4A",
        "Informational": "_vpK58yS4xc",
        "Persuasive":    "L615As9olNg",
        "TDA":           "B-fSL1VAyIc",
    },
    6: {
        "Narrative":     "vsEjBrc4zEk",
        "Informational": "IdEs_lPWhcc",
        "Persuasive":    "zvmtwQIosdI",
        "TDA":           "B-fSL1VAyIc",
    },
    7: {
        "Narrative":     "Mq--Db6S09I",
        "Informational": "DNUZMv7LNIo",
        "Persuasive":    "ntNN1uReAKQ",
        "TDA":           "B-fSL1VAyIc",
    },
    8: {
        "Narrative":     "K5jcaIVifOY",
        "Informational": "kz5XZh_2Ko8",
        "Persuasive":    "hAv84OjHVGM",
        "TDA":           "B-fSL1VAyIc",
    },
}

PHASES = ["Pre-writing", "Drafting", "Revising", "Editing", "Publishing"]

LESSON_HTML = {
    "Narrative": {
        "Pre-writing":  "<h4>Narrative Planning</h4><p>Map out your story with a Beginning, Middle, and End. Think about your characters, setting, and the problem they need to solve.</p>",
        "Drafting":     "<h4>Narrative Drafting</h4><p>Use transition words like <em>First</em>, <em>Next</em>, and <em>Finally</em> to connect your story events. Show, don't tell!</p>",
        "Revising":     "<h4>Narrative Revising</h4><p>Read your draft aloud. Add sensory details, strong verbs, and dialogue to make your story come alive.</p>",
        "Editing":      "<h4>Narrative Editing</h4><p>Check every sentence for correct capitalization, punctuation, and spelling. Make sure each paragraph stays on topic.</p>",
        "Publishing":   "<h4>Narrative Publishing</h4><p>Write or type your final copy neatly. Add a title and an illustration if you like!</p>",
    },
    "Informational": {
        "Pre-writing":  "<h4>Informational Planning</h4><p>Choose a topic you know well. Organize your facts into clear categories — each category will become a paragraph.</p>",
        "Drafting":     "<h4>Informational Drafting</h4><p>Start with a hook and a clear topic sentence. Support each main idea with at least two facts or examples.</p>",
        "Revising":     "<h4>Informational Revising</h4><p>Check that every detail relates to your main topic. Add transition phrases like <em>In addition</em> and <em>For example</em>.</p>",
        "Editing":      "<h4>Informational Editing</h4><p>Verify that names, dates, and facts are accurate. Correct any grammar or spelling errors.</p>",
        "Publishing":   "<h4>Informational Publishing</h4><p>Write your final draft with a strong introduction and conclusion. Consider adding subheadings or a diagram.</p>",
    },
    "Persuasive": {
        "Pre-writing":  "<h4>Persuasive Planning</h4><p>State your opinion clearly. List at least three reasons that support it, and think about what someone who disagrees might say.</p>",
        "Drafting":     "<h4>Persuasive Drafting</h4><p>Open with a strong hook and your opinion statement. Use facts, statistics, or examples to back up each reason.</p>",
        "Revising":     "<h4>Persuasive Revising</h4><p>Address the opposing view and explain why your side is stronger. Make your conclusion a call to action.</p>",
        "Editing":      "<h4>Persuasive Editing</h4><p>Read each sentence carefully. Fix run-ons and fragments. Make sure your tone stays respectful and confident.</p>",
        "Publishing":   "<h4>Persuasive Publishing</h4><p>Prepare your final copy. Consider sharing it with your class — good persuasive writing deserves an audience!</p>",
    },
    "TDA": {
        "Pre-writing":  "<h4>TDA Planning</h4><p>Read the passage carefully. Identify the key claim or question, then highlight evidence from the text that supports your answer.</p>",
        "Drafting":     "<h4>TDA Drafting</h4><p>Begin with a clear claim that directly answers the prompt. Use direct quotes or paraphrased evidence from the text.</p>",
        "Revising":     "<h4>TDA Revising</h4><p>Make sure every piece of evidence is explained and linked back to your claim. Avoid bringing in outside information.</p>",
        "Editing":      "<h4>TDA Editing</h4><p>Check that all quotations are properly formatted. Fix any grammar, spelling, or punctuation errors.</p>",
        "Publishing":   "<h4>TDA Publishing</h4><p>Write your final response. Make sure your introduction, body, and conclusion are clearly organized.</p>",
    },
}

PROMPTS_DATA = []
for _grade, _topics_map, _topic_list in [
    (3, {}, ["Narrative", "Informational", "Persuasive"]),
    (4, {}, ["Narrative", "Informational", "Persuasive"]),
    (5, {}, ["Narrative", "Informational", "Persuasive"]),
    (6, {}, ["Narrative", "Informational", "Persuasive"]),
    (7, {}, ["Narrative", "Informational", "Persuasive"]),
    (8, {}, ["Narrative", "Informational", "Persuasive"]),
]:
    pass  # built inline below

_GRADE_PROMPTS = {
    3: {
        "Narrative":     ["The magic treehouse in your yard.", "A day with a talking dragon.", "Finding a lost treasure map.", "The day the gravity turned off.", "Super Teacher vs. Mega Boredom."],
        "Informational": ["How to grow a sunflower.", "All about my favorite animal.", "How to make the perfect sandwich.", "Why seasons change.", "Fun facts about space."],
        "Persuasive":    ["Why we should have more art class.", "Should kids pick their own bedtimes?", "Why reading is the best hobby.", "Should we have pets in school?", "Why recess is important."],
    },
    4: {
        "Narrative":     ["Journey through a black hole.", "The mystery of the missing statue.", "A week spent in the 1800s.", "The invention that changed my life.", "Island of the giant insects."],
        "Informational": ["The history of video games.", "How a bill becomes a law.", "Amazing architectural wonders.", "The importance of ocean conservation.", "How weather patterns form."],
        "Persuasive":    ["Should students have 4-day school weeks?", "Why tablets should replace textbooks.", "Should screen time be limited for kids?", "The value of volunteering in your town.", "Why school uniforms are a good idea."],
    },
    5: {
        "Narrative":     ["Trapped in a video game world.", "The secret life of my neighbors.", "Exploring an underwater civilization.", "The day I swapped lives with a scientist.", "A suspenseful encounter in the forest."],
        "Informational": ["Leading causes of climate change.", "The chemistry of baking a cake.", "How the human brain stores memories.", "The impact of technology on daily life.", "Famous scientists who changed history."],
        "Persuasive":    ["Convincing the city to build a new park.", "Is social media harmful to pre-teens?", "Why every student should learn to cook.", "Should zoo captivity be banned?", "The importance of learning a second language."],
    },
    6: {
        "Narrative":     ["A mysterious letter arrives at midnight.", "The last human on Earth.", "Waking up with the ability to hear thoughts.", "A road trip that goes terribly wrong — then right.", "The discovery hidden beneath the old school."],
        "Informational": ["How volcanoes form and erupt.", "The civil rights movement: key events.", "How the internet changed communication.", "The human digestive system explained.", "Renewable vs. non-renewable energy sources."],
        "Persuasive":    ["Should junk food be banned in schools?", "Why community service should be required.", "Should students grade their teachers?", "Is homework beneficial or harmful?", "Why public libraries matter more than ever."],
    },
    7: {
        "Narrative":     ["A conversation that changed everything.", "The summer I learned what courage means.", "Two strangers. One broken-down train. Six hours.", "The moment I realized I was wrong.", "Life in a world where lying is impossible."],
        "Informational": ["Causes and effects of World War I.", "How vaccines work in the human body.", "The economics of supply and demand.", "The psychology of habits and how to change them.", "Ocean pollution: sources, effects, and solutions."],
        "Persuasive":    ["Should the voting age be lowered to 16?", "Are standardized tests a fair measure of intelligence?", "Should athletes be held to higher moral standards?", "Is year-round school a good idea?", "Should cell phones be allowed in classrooms?"],
    },
    8: {
        "Narrative":     ["The night the city lost all its power.", "A letter written to my future self.", "The day I stopped caring what people thought.", "Two rivals forced to work together.", "The last performance before everything changed."],
        "Informational": ["The causes and legacy of the American Civil War.", "How genetic engineering works.", "The role of propaganda in modern media.", "How the stock market functions.", "The science and ethics of artificial intelligence."],
        "Persuasive":    ["Should the death penalty be abolished?", "Is social media doing more harm than good?", "Should colleges consider grades or potential?", "Should the minimum wage be raised nationally?", "Is it ethical to use animals in scientific research?"],
    },
}


# ---------------------------------------------------------------------------

def ensure_tables():
    print("[startup] Creating / verifying database tables...")
    Base.metadata.create_all(bind=engine)
    print("[startup] Tables OK.")


def seed_if_empty(db):
    count = db.query(LessonContent).count()
    if count > 0:
        print(f"[startup] Lesson content already seeded ({count} rows). Skipping seed.")
        return

    print("[startup] lesson_contents table is empty — seeding...")

    # Prompts
    for grade, topics in _GRADE_PROMPTS.items():
        for topic, prompts in topics.items():
            for assignment in ["we-do", "you-do"]:
                for text in prompts:
                    db.add(Prompt(
                        topic=topic,
                        grade_level=grade,
                        assignment_type=assignment,
                        prompt_text=f"G{grade} {assignment}: {text}",
                    ))

    # Lesson content
    for grade, topics in CURATED_VIDEOS.items():
        for topic, video_id in topics.items():
            phase_html = LESSON_HTML.get(topic, {})
            for phase in PHASES:
                content = phase_html.get(
                    phase,
                    f"<h4>{phase} for Grade {grade} {topic}</h4>"
                    f"<p>Watch the video above, then follow your teacher's instructions.</p>"
                )
                db.add(LessonContent(
                    grade_level=grade,
                    topic=topic,
                    phase=phase,
                    video_url=video_id,
                    content_html=content,
                ))

    db.commit()
    print("[startup] Seed complete.")


def fetch_missing_transcripts(db):
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
