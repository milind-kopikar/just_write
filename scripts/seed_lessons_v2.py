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

def seed_data():
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Prompt).delete()
        db.query(LessonContent).delete()

        prompts_data = []
        
        # --- GRADE 3 PROMPTS (Repeat/Refine) ---
        for assignment in ["we-do", "you-do"]:
            prefix = "Grade 3 " + ("(Coach)" if assignment == "we-do" else "(Independent)")
            prompts_data.extend([
                {"topic": "Narrative", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: The magic treehouse in your yard."},
                {"topic": "Narrative", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: A day with a talking dragon."},
                {"topic": "Narrative", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Finding a lost treasure map."},
                {"topic": "Narrative", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: The day the gravity turned off."},
                {"topic": "Narrative", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Super Teacher vs. Mega Boredom."},

                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: How to grow a sunflower."},
                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: All about my favorite animal."},
                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: How to make the perfect sandwich."},
                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Why seasons change."},
                {"topic": "Informational", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Fun facts about space."},

                {"topic": "Persuasive", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Why we should have more art class."},
                {"topic": "Persuasive", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Should kids pick their own bedtimes?"},
                {"topic": "Persuasive", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Why reading is the best hobby."},
                {"topic": "Persuasive", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Should we have pets in school?"},
                {"topic": "Persuasive", "grade_level": 3, "assignment_type": assignment, "prompt_text": f"G3 {assignment}: Why recess is important."},
            ])

        # --- GRADE 4 PROMPTS ---
        for assignment in ["we-do", "you-do"]:
            prompts_data.extend([
                {"topic": "Narrative", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Journey through a black hole."},
                {"topic": "Narrative", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The mystery of the missing statue."},
                {"topic": "Narrative", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: A week spent in the 1800s."},
                {"topic": "Narrative", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The invention that changed my life."},
                {"topic": "Narrative", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Island of the giant insects."},

                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The history of video games."},
                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: How a bill becomes a law (simple)."},
                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Amazing architectural wonders."},
                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The importance of ocean conservation."},
                {"topic": "Informational", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: How to code a simple game loop."},

                {"topic": "Persuasive", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Should students have 4-day school weeks?"},
                {"topic": "Persuasive", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Why tablets should replace textbooks."},
                {"topic": "Persuasive", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Should screen time be limited for kids?"},
                {"topic": "Persuasive", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: The value of volunteering in your town."},
                {"topic": "Persuasive", "grade_level": 4, "assignment_type": assignment, "prompt_text": f"G4 {assignment}: Why school uniforms are a good/bad idea."},
            ])

        # --- GRADE 5 PROMPTS ---
        for assignment in ["we-do", "you-do"]:
            prompts_data.extend([
                {"topic": "Narrative", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Trapped in a video game world."},
                {"topic": "Narrative", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The secret life of my neighbors."},
                {"topic": "Narrative", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Exploring an underwater civilization."},
                {"topic": "Narrative", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The day I swapped lives with a CEO."},
                {"topic": "Narrative", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: A suspenseful encounter in the forest."},

                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Leading causes of climate change."},
                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The chemistry of baking a cake."},
                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: How the human brain stores memories."},
                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The impact of AI on our daily lives."},
                {"topic": "Informational", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Famous female scientists in history."},

                {"topic": "Persuasive", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Convincing the city to build a new park."},
                {"topic": "Persuasive", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Is social media harmful to pre-teens?"},
                {"topic": "Persuasive", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Why every student should learn to cook."},
                {"topic": "Persuasive", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: Should zoo captivity be banned?"},
                {"topic": "Persuasive", "grade_level": 5, "assignment_type": assignment, "prompt_text": f"G5 {assignment}: The importance of learning a second language."},
            ])

        for p in prompts_data:
            db.add(Prompt(**p))

        # --- LESSON CONTENT (I DO) ---
        lessons = [
            # Grade 3
            {"grade_level": 3, "topic": "Narrative", "phase": "Pre-writing", "video_url": "ZjOj4plV5lE", 
             "content_html": "<h4>G3 Narrative Planning</h4><p>Let's map out our story with a Beginning, Middle, and End!</p>"},
            {"grade_level": 3, "topic": "Narrative", "phase": "Drafting", "video_url": "xwM-fej8ZY8", 
             "content_html": "<h4>G3 Narrative Drafting</h4><p>Time to use those 'transition words' like First, Next, and Last.</p>"},
            
            # Grade 4
            {"grade_level": 4, "topic": "Narrative", "phase": "Pre-writing", "video_url": "k32GzIDwVfs", 
             "content_html": "<h4>G4 Narrative Planning</h4><p>Focus on a 'Small Moment' and expand it with sensory details.</p>"},
            {"grade_level": 4, "topic": "Persuasive", "phase": "Pre-writing", "video_url": "W_6p349_hS8", 
             "content_html": "<h4>G4 Opinion Planning</h4><p>State your OREO: Opinion, Reason, Example, Opinion.</p>"},
            {"grade_level": 4, "topic": "Informational", "phase": "Pre-writing", "video_url": "0QfXfTf_q_8", 
             "content_html": "<h4>G4 Informational Planning</h4><p>Organize your facts into clear categories with subheadings.</p>"},

            # Grade 5
            {"grade_level": 5, "topic": "Narrative", "phase": "Pre-writing", "video_url": "LmB138C6mX8", 
             "content_html": "<h4>G5 Plot Development</h4><p>Build tension using a 'rising action' leading to a clear climax.</p>"},
            {"grade_level": 5, "topic": "Persuasive", "phase": "Pre-writing", "video_url": "iOsCcs9rU3w", 
             "content_html": "<h4>G5 Persuasive Strategies</h4><p>Use evidence and acknowledge the opposing point of view.</p>"},
            {"grade_level": 5, "topic": "Informational", "phase": "Pre-writing", "video_url": "xP6B6w720_0", 
             "content_html": "<h4>G5 Information Structures</h4><p>Choose between Compare/Contrast, Cause/Effect, or Chronological.</p>"},
        ]

        # Add generic lessons for missing phases to ensure something always shows
        for grade in [3, 4, 5]:
            for topic in ["Narrative", "Informational", "Persuasive"]:
                for phase in ["Pre-writing", "Drafting", "Revising", "Editing", "Publishing"]:
                    # Check if already added
                    exists = any(l["grade_level"] == grade and l["topic"] == topic and l["phase"] == phase for l in lessons)
                    if not exists:
                         lessons.append({
                            "grade_level": grade, "topic": topic, "phase": phase, 
                            "video_url": "dQw4w9WgXcQ", 
                            "content_html": f"<h4>{phase} for {grade}th Grade {topic}</h4><p>Follow the steps in the video to improve your work!</p>"
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
