from pydantic_ai import Agent
import os
from dotenv import load_dotenv
import asyncio
from pathlib import Path

# Load .env from backend folder
base_dir = Path(__file__).resolve().parents[1]
load_dotenv(base_dir / "backend" / ".env")

async def debug_agent():
    agent = Agent('gemini-2.0-flash') # Use a simple model ID
    try:
        result = await agent.run("Hello")
        print("Attributes of Result:", dir(result))
        try:
            print("Output:", result.output)
        except:
            pass
        try:
            print("Data:", result.data)
        except:
            pass
    except Exception as e:
        print("Execution failed:", e)

if __name__ == "__main__":
    asyncio.run(debug_agent())
