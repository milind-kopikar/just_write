from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    grade_level: int = 3

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    grade_level: int
    class Config:
        from_attributes = True

class PromptResponse(BaseModel):
    id: int
    topic: str
    grade_level: int
    prompt_text: str
    assignment_type: str
    class Config:
        from_attributes = True

class LessonContentResponse(BaseModel):
    id: int
    grade_level: int
    topic: str
    phase: str
    video_url: str
    content_html: str
    class Config:
        from_attributes = True

class ScoreUpdate(BaseModel):
    topic: str
    phase: str
    focus: float
    content: float
    organization: float
    style: float
    conventions: float
    feedback: str
