import sys
import os
from sqlalchemy.orm import Session
from pathlib import Path

# Add the backend directory to sys.path so we can import app modules
backend_dir = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(backend_dir))

from app.database import SessionLocal, engine
from app.models import Prompt, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_prompts():
    db = SessionLocal()
    try:
        # Clear existing prompts to avoid duplicates on re-run
        db.query(Prompt).delete()

        prompts_data = [
            # Narrative - We Do
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "The Magic Backpack: You find a backpack that can talk. What happens on your first day of school together?"},
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "The Lost Puppy: You find a puppy in the park with no collar. Describe how you help it find its way home."},
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "A Day at the Moon: You wake up and notice you are in a house on the moon. What does your morning look like?"},
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "The Time-Travel Tree: You climb a tree in your backyard and end up in the land of dinosaurs."},
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "Superpower Surprise: You wake up and realize you can fly. What do you do first?"},
            # Narrative - You Do
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "The Secret Door: You find a small door hidden behind a bookshelf in your room. Where does it lead?"},
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "The Talking Cat: Your cat suddenly starts talking to you and asks for a favor."},
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "The Underwater Adventure: You can suddenly breathe underwater. Describe your trip to the bottom of the ocean."},
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "The Best Birthday Ever: Write a story about a birthday party that had a giant surprise."},
            {"topic": "Narrative", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "Robot Best Friend: You build a robot out of boxes, and it comes to life."},

            # Informational - We Do
            {"topic": "Informational", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "How to Make a Peanut Butter and Jelly Sandwich: Explain the steps clearly so a friend can follow them."},
            {"topic": "Informational", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "Living in the Arctic: Describe what it is like for animals like polar bears to live in the cold."},
            {"topic": "Informational", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "The Life Cycle of a Butterfly: Explain how a caterpillar turns into a butterfly."},
            {"topic": "Informational", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "Why Recycling Matters: Explain why it is important for kids to recycle plastic and paper."},
            {"topic": "Informational", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "My Favorite Sport: Pick a sport and explain the basic rules and why people like it."},
            # Informational - You Do
            {"topic": "Informational", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "How to Care for a Pet: Choose an animal and explain what they need to be happy and healthy."},
            {"topic": "Informational", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "The Importance of Bees: Explain why bees are important for our gardens and food."},
            {"topic": "Informational", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "How a Plant Grows: Describe the things a seed needs to grow into a flower."},
            {"topic": "Informational", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "My School Day: Describe what a typical day at school looks like for a third grader."},
            {"topic": "Informational", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "All About Planets: Pick one planet in our solar system and share three interesting facts about it."},

            # Persuasive - We Do
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "Should Students Have Homework? Write a letter to your teacher explaining why or why not."},
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "The Best Pet: Persuade your parents that a dog (or another animal) is the best pet for your family."},
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "More Recess Time: Convince your principal that 3rd graders need 10 more minutes of recess."},
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "Favorite School Lunch: Persuade the cafeteria to serve your favorite meal every Friday."},
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "we-do", "prompt_text": "Why We Should Plant More Trees: Convince your neighbors to plant a tree in their yard."},
            # Persuasive - You Do
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "Books vs. Movies: Persuade a friend that reading the book is better than watching the movie."},
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "Should Kids Have Cell Phones? Give reasons why a 3rd grader should or should not have a phone."},
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "The Best Superhero: Convince your class that your favorite superhero is the strongest and bravest."},
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "Bedtime Rules: Persuade your parents to let you stay up 30 minutes later on weekends."},
            {"topic": "Persuasive", "grade_level": 3, "assignment_type": "you-do", "prompt_text": "Classroom Pet: Convince your teacher that your class should get a hamster or a turtle."},
        ]

        for p_data in prompts_data:
            prompt = Prompt(**p_data)
            db.add(prompt)
        
        db.commit()
        print(f"Successfully seeded {len(prompts_data)} prompts.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding prompts: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_prompts()
