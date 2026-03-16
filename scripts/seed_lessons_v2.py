import sys
import os
from sqlalchemy.orm import Session
from pathlib import Path

# Add the backend directory to sys.path
backend_dir = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(backend_dir))

from app.database import SessionLocal, engine
from app.models import Prompt, LessonContent, Base

# Create tables
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# Curated video IDs for the "I Do" section.
# These are the ONLY way to update videos — there is no API endpoint for it.
# Each video ID maps to: youtube.com/watch?v=<id>
# To add or change a video, update this dict and re-run this script.
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


def seed_data():
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Prompt).delete()
        db.query(LessonContent).delete()

        prompts_data = []

        # --- GRADE 3 PROMPTS ---
        for assignment in ["we-do", "you-do"]:
            prompts_data.extend([
                {"topic": "Narrative",     "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: The magic treehouse in your yard."},
                {"topic": "Narrative",     "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: A day with a talking dragon."},
                {"topic": "Narrative",     "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Finding a lost treasure map."},
                {"topic": "Narrative",     "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: The day the gravity turned off."},
                {"topic": "Narrative",     "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Super Teacher vs. Mega Boredom."},

                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: How to grow a sunflower."},
                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: All about my favorite animal."},
                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: How to make the perfect sandwich."},
                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Why seasons change."},
                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Fun facts about space."},

                {"topic": "Persuasive",    "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Why we should have more art class."},
                {"topic": "Persuasive",    "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Should kids pick their own bedtimes?"},
                {"topic": "Persuasive",    "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Why reading is the best hobby."},
                {"topic": "Persuasive",    "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Should we have pets in school?"},
                {"topic": "Persuasive",    "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Why recess is important."},
            ])

        # --- GRADE 4 PROMPTS ---
        for assignment in ["we-do", "you-do"]:
            prompts_data.extend([
                {"topic": "Narrative",     "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Journey through a black hole."},
                {"topic": "Narrative",     "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The mystery of the missing statue."},
                {"topic": "Narrative",     "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: A week spent in the 1800s."},
                {"topic": "Narrative",     "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The invention that changed my life."},
                {"topic": "Narrative",     "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Island of the giant insects."},

                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The history of video games."},
                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: How a bill becomes a law."},
                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Amazing architectural wonders."},
                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The importance of ocean conservation."},
                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: How weather patterns form."},

                {"topic": "Persuasive",    "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Should students have 4-day school weeks?"},
                {"topic": "Persuasive",    "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Why tablets should replace textbooks."},
                {"topic": "Persuasive",    "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Should screen time be limited for kids?"},
                {"topic": "Persuasive",    "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The value of volunteering in your town."},
                {"topic": "Persuasive",    "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Why school uniforms are a good idea."},
            ])

        # --- GRADE 5 PROMPTS ---
        for assignment in ["we-do", "you-do"]:
            prompts_data.extend([
                {"topic": "Narrative",     "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Trapped in a video game world."},
                {"topic": "Narrative",     "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The secret life of my neighbors."},
                {"topic": "Narrative",     "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Exploring an underwater civilization."},
                {"topic": "Narrative",     "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The day I swapped lives with a scientist."},
                {"topic": "Narrative",     "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: A suspenseful encounter in the forest."},

                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Leading causes of climate change."},
                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The chemistry of baking a cake."},
                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: How the human brain stores memories."},
                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The impact of technology on daily life."},
                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Famous scientists who changed history."},

                {"topic": "Persuasive",    "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Convincing the city to build a new park."},
                {"topic": "Persuasive",    "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Is social media harmful to pre-teens?"},
                {"topic": "Persuasive",    "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Why every student should learn to cook."},
                {"topic": "Persuasive",    "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Should zoo captivity be banned?"},
                {"topic": "Persuasive",    "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The importance of learning a second language."},
            ])

        # --- GRADE 6 PROMPTS ---
        for assignment in ["we-do", "you-do"]:
            prompts_data.extend([
                {"topic": "Narrative",     "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: A mysterious letter arrives at midnight."},
                {"topic": "Narrative",     "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: The last human on Earth."},
                {"topic": "Narrative",     "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: Waking up with the ability to hear thoughts."},
                {"topic": "Narrative",     "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: A road trip that goes terribly wrong — then right."},
                {"topic": "Narrative",     "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: The discovery hidden beneath the old school."},

                {"topic": "Informational", "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: How volcanoes form and erupt."},
                {"topic": "Informational", "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: The civil rights movement: key events."},
                {"topic": "Informational", "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: How the internet changed communication."},
                {"topic": "Informational", "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: The human digestive system explained."},
                {"topic": "Informational", "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: Renewable vs. non-renewable energy sources."},

                {"topic": "Persuasive",    "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: Should junk food be banned in schools?"},
                {"topic": "Persuasive",    "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: Why community service should be required."},
                {"topic": "Persuasive",    "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: Should students grade their teachers?"},
                {"topic": "Persuasive",    "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: Is homework beneficial or harmful?"},
                {"topic": "Persuasive",    "grade_level": 6, "assignment_type": assignment, "prompt_text": f"G6 {assignment}: Why public libraries matter more than ever."},
            ])

        # --- GRADE 7 PROMPTS ---
        for assignment in ["we-do", "you-do"]:
            prompts_data.extend([
                {"topic": "Narrative",     "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: A conversation that changed everything."},
                {"topic": "Narrative",     "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: The summer I learned what courage means."},
                {"topic": "Narrative",     "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: Two strangers. One broken-down train. Six hours."},
                {"topic": "Narrative",     "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: The moment I realized I was wrong."},
                {"topic": "Narrative",     "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: Life in a world where lying is impossible."},

                {"topic": "Informational", "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: Causes and effects of World War I."},
                {"topic": "Informational", "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: How vaccines work in the human body."},
                {"topic": "Informational", "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: The economics of supply and demand."},
                {"topic": "Informational", "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: The psychology of habits and how to change them."},
                {"topic": "Informational", "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: Ocean pollution: sources, effects, and solutions."},

                {"topic": "Persuasive",    "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: Should the voting age be lowered to 16?"},
                {"topic": "Persuasive",    "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: Are standardized tests a fair measure of intelligence?"},
                {"topic": "Persuasive",    "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: Should athletes be held to higher moral standards?"},
                {"topic": "Persuasive",    "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: Is year-round school a good idea?"},
                {"topic": "Persuasive",    "grade_level": 7, "assignment_type": assignment, "prompt_text": f"G7 {assignment}: Should cell phones be allowed in classrooms?"},
            ])

        # --- GRADE 8 PROMPTS ---
        for assignment in ["we-do", "you-do"]:
            prompts_data.extend([
                {"topic": "Narrative",     "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: The night the city lost all its power."},
                {"topic": "Narrative",     "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: A letter written to my future self."},
                {"topic": "Narrative",     "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: The day I stopped caring what people thought."},
                {"topic": "Narrative",     "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: Two rivals forced to work together."},
                {"topic": "Narrative",     "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: The last performance before everything changed."},

                {"topic": "Informational", "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: The causes and legacy of the American Civil War."},
                {"topic": "Informational", "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: How genetic engineering works."},
                {"topic": "Informational", "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: The role of propaganda in modern media."},
                {"topic": "Informational", "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: How the stock market functions."},
                {"topic": "Informational", "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: The science and ethics of artificial intelligence."},

                {"topic": "Persuasive",    "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: Should the death penalty be abolished?"},
                {"topic": "Persuasive",    "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: Is social media doing more harm than good?"},
                {"topic": "Persuasive",    "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: Should colleges consider grades or potential?"},
                {"topic": "Persuasive",    "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: Should the minimum wage be raised nationally?"},
                {"topic": "Persuasive",    "grade_level": 8, "assignment_type": assignment, "prompt_text": f"G8 {assignment}: Is it ethical to use animals in scientific research?"},
            ])

        for p in prompts_data:
            db.add(Prompt(**p))

        # --- LESSON CONTENT (I DO) ---
        # Build one lesson per (grade, topic, phase) using CURATED_VIDEOS.
        # The same curated video is shown for every writing phase of a topic —
        # this is intentional so students always see the correct instructional
        # video regardless of which phase tab they are on.
        lessons = []
        for grade, topics in CURATED_VIDEOS.items():
            for topic, video_id in topics.items():
                phase_html = LESSON_HTML.get(topic, {})
                for phase in PHASES:
                    content = phase_html.get(
                        phase,
                        f"<h4>{phase} for Grade {grade} {topic}</h4>"
                        f"<p>Watch the video above, then follow your teacher's instructions.</p>"
                    )
                    lessons.append({
                        "grade_level": grade,
                        "topic": topic,
                        "phase": phase,
                        "video_url": video_id,
                        "content_html": content,
                    })

        for l in lessons:
            db.add(LessonContent(**l))

        db.commit()
        print(f"Successfully seeded {len(prompts_data)} prompts and {len(lessons)} lessons.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
