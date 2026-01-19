from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..core.ai_agents import get_socratic_response, evaluate_writing
from .auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
    topic: str
    prompt: Optional[str] = None

class EvaluateRequest(BaseModel):
    text: str
    topic: str
    prompt: Optional[str] = None
    project_id: Optional[int] = None

@router.get("/prompts", response_model=List[schemas.PromptResponse])
def get_prompts(
    topic: str, 
    assignment_type: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    prompts = db.query(models.Prompt).filter(
        models.Prompt.topic == topic,
        models.Prompt.assignment_type == assignment_type,
        models.Prompt.grade_level == current_user.grade_level
    ).all()
    return prompts

@router.get("/lesson", response_model=schemas.LessonContentResponse)
def get_lesson(
    topic: str,
    phase: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    lesson = db.query(models.LessonContent).filter(
        models.LessonContent.grade_level == current_user.grade_level,
        models.LessonContent.topic == topic,
        models.LessonContent.phase == phase
    ).first()
    
    if not lesson:
        # Fallback to Grade 3 if specific grade lesson not found
        lesson = db.query(models.LessonContent).filter(
            models.LessonContent.grade_level == 3,
            models.LessonContent.topic == topic,
            models.LessonContent.phase == phase
        ).first()
        
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
        
    return lesson

@router.post("/chat")
async def chat(req: ChatRequest):
    try:
        print(f"Chat request for topic: {req.topic}")
        # Only pass history up to the last 10 messages to keep it efficient
        history = req.history[-10:] if req.history else []
        response, _ = await get_socratic_response(history, req.message, req.topic, req.prompt)
        return {"response": response}
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Chat Error: {str(e)}")
        print(error_trace)
        # Detect common API key / permission errors from GenAI and return a helpful status
        msg = str(e)
        if 'reported as leaked' in msg.lower():
            raise HTTPException(status_code=503, detail="AI service unavailable: invalid or revoked API key. Rotate your GOOGLE_API_KEY and try again.")
        
        if '429' in msg or 'resource exhausted' in msg.lower():
            raise HTTPException(status_code=429, detail="The AI is currently busy (Rate Limit). Please wait 30-60 seconds and try again.")
            
        raise HTTPException(status_code=500, detail=f"Internal error: {msg}")

@router.post("/evaluate")
async def evaluate(req: EvaluateRequest, db: Session = Depends(get_db)):
    try:
        print(f"Evaluating work for topic: {req.topic}")
        evaluation_raw = await evaluate_writing(req.text, req.topic, req.prompt)

        # Try to parse JSON from the response
        import json
        import re

        # Find JSON in backticks
        match = re.search(r'```json\s*(.*?)\s*```', evaluation_raw, re.DOTALL)
        if not match:
             match = re.search(r'```\s*(.*?)\s*```', evaluation_raw, re.DOTALL)
             
        if match:
            evaluation_json = json.loads(match.group(1))
            return evaluation_json
        else:
            # Fallback if AI didn't return JSON
            return {"raw_text": evaluation_raw}

    except Exception as e:
        import traceback
        print(f"Evaluation Error: {str(e)}")
        print(traceback.format_exc())
        msg = str(e)
        if 'reported as leaked' in msg.lower():
            # Return 503 so frontend can inform the developer/admin to rotate keys
            raise HTTPException(status_code=503, detail="AI service unavailable: invalid or revoked API key. Rotate your GOOGLE_API_KEY and try again.")
        
        if '429' in msg or 'resource exhausted' in msg.lower():
            raise HTTPException(status_code=429, detail="Google API quota reached. Please wait a minute before trying again.")

        raise HTTPException(status_code=500, detail="Internal error evaluating writing")

@router.get("/report-card")
async def get_report_card(user_id: int = 1):
    # For demo, return dummy data as requested
    return {
        "student_name": "Demo Student",
        "scores": [
            {"metric": "Focus", "score": 3.5},
            {"metric": "Content", "score": 3.0},
            {"metric": "Organization", "score": 2.5},
            {"metric": "Style", "score": 3.2},
            {"metric": "Conventions", "score": 2.8}
        ],
        "progress": [
            {"phase": "Pre-writing", "status": "Completed"},
            {"phase": "Drafting", "status": "In Progress"},
            {"phase": "Revising", "status": "Locked"},
            {"phase": "Editing", "status": "Locked"},
            {"phase": "Publishing", "status": "Locked"}
        ]
    }
