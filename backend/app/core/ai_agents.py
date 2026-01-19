import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from dotenv import load_dotenv
from google import genai
from .system_prompt import SYSTEM_PROMPT_WE_DO, SYSTEM_PROMPT_YOU_DO

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_model(model_name: str = 'gemini-2.0-flash'):
    # Ensure key is in environment for pydantic-ai to pick up
    if GOOGLE_API_KEY:
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    else:
        print("CRITICAL: GOOGLE_API_KEY not found!")
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

async def get_socratic_response(history, user_message, topic, prompt=None):
    """Gets a Socratic response for the 'We Do' phase."""
    # Convert simple history dicts to pydantic-ai messages if provided
    formatted_history = []
    if history:
        for msg in history:
            role = msg.get('role')
            content = msg.get('content')
            if role == 'user':
                formatted_history.append(ModelRequest(parts=[UserPromptPart(content=content)]))
            elif role == 'assistant':
                formatted_history.append(ModelResponse(parts=[TextPart(content=content)], timestamp=datetime.now(timezone.utc)))

    # Combine context
    ctx_parts = [f"Topic: {topic}"]
    if prompt:
        ctx_parts.append(f"Prompt: {prompt}")
    ctx_parts.append(f"Student says: {user_message}")
    
    ctx_message = "\n".join(ctx_parts)
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
