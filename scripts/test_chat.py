import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to sys.path
backend_path = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(backend_path))

from app.core.ai_agents import get_socratic_response

async def test_chat():
    print("Testing Socratic Chat...")
    topic = "Narrative"
    user_message = "I want to write about a dragon who lives in a library."
    history = []
    
    try:
        response, new_history = await get_socratic_response(history, user_message, topic)
        print(f"\nAI Response: {response}")
        print(f"History length: {len(new_history)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_chat())
