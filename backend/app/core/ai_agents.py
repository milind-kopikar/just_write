import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from dotenv import load_dotenv
from google import genai
from .system_prompt import SYSTEM_PROMPT_WE_DO, SYSTEM_PROMPT_YOU_DO

# Load environment variables from the parent directory's .env file
# This ensures it works regardless of whether the CWD is the project root or the backend folder
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(env_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_model(model_name: str = 'gemini-2.5-flash-lite'):
    # Ensure key is in environment for pydantic-ai to pick up
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    elif not os.environ.get("GOOGLE_API_KEY"):
        print("CRITICAL: GOOGLE_API_KEY not found in environment or .env file!")
    return GoogleModel(model_name)

# Agent for "We Do" phase (Socratic Chat)
we_do_agent = Agent(
    model=get_model(),
    system_prompt=SYSTEM_PROMPT_WE_DO,
)

# Agent for "You Do" phase (Evaluation)
evaluation_agent = Agent(
    model=get_model(),
    system_prompt=SYSTEM_PROMPT_YOU_DO,
)

from pydantic_ai.messages import ModelRequest, ModelResponse, TextPart, UserPromptPart
from datetime import datetime, timezone

async def get_socratic_response(history, user_message, topic, prompt=None, transcript=None):
    """Gets a Socratic response for the 'We Do' phase.

    If a transcript is provided it is injected as lesson context so the AI
    coach can base its exercises and questions on what the student just watched.
    """
    # Convert simple history dicts to pydantic-ai messages if provided
    formatted_history = []
    if history:
        # Pydantic-AI/Gemini often expect history to start with a User message.
        # If the first message is from the assistant (like a greeting), we can
        # either skip it or treat it as a response to a 'fake' user prompt.
        # Here, we skip leading assistant messages to ensure valid alternating history.
        start_idx = 0
        while start_idx < len(history) and history[start_idx].get('role') == 'assistant':
            start_idx += 1

        for i in range(start_idx, len(history)):
            msg = history[i]
            role = msg.get('role')
            content = msg.get('content')
            if role == 'user':
                formatted_history.append(ModelRequest(parts=[UserPromptPart(content=content)]))
            elif role == 'assistant':
                # ModelResponse needs at least one part and a timestamp
                formatted_history.append(ModelResponse(parts=[TextPart(content=content)], timestamp=datetime.now(timezone.utc)))

    # Combined context for the current user message
    ctx_parts = [f"Topic: {topic}"]
    if transcript:
        # Trim to ~3000 words to stay within context limits
        words = transcript.split()
        trimmed = " ".join(words[:3000])
        ctx_parts.append(
            f"Lesson Transcript (from the I-Do video the student just watched — "
            f"use this to craft exercises and questions based on what was taught):\n{trimmed}"
        )
    if prompt:
        ctx_parts.append(f"Writing Prompt: {prompt}")
    ctx_parts.append(f"Student says: {user_message}")

    ctx_message = "\n\n".join(ctx_parts)
    result = await we_do_agent.run(ctx_message, message_history=formatted_history)
    return result.output, result.new_messages()

async def evaluate_writing(text, topic, prompt=None):
    """Evaluates the student's writing using the PSSA rubric."""
    ctx_message = f"Topic: {topic}\n"
    if prompt:
        ctx_message += f"Specific Prompt: {prompt}\n"
    ctx_message += f"Student's Work:\n{text}"
    result = await evaluation_agent.run(ctx_message)
    return result.output
