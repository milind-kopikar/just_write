from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    grade_level = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)  # Narrative, Informational, Persuasive
    grade_level = Column(Integer, default=3)
    prompt_text = Column(Text)
    assignment_type = Column(String)  # "we-do" or "you-do"

class LessonContent(Base):
    __tablename__ = "lesson_contents"
    id = Column(Integer, primary_key=True, index=True)
    grade_level = Column(Integer)
    topic = Column(String)
    phase = Column(String)
    video_url = Column(String)
    content_html = Column(Text)

class StudentScore(Base):
    __tablename__ = "student_scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String)  # Narrative, Informational, Persuasive
    phase = Column(String)  # Pre-writing, Drafting, Revising, Editing, Publishing
    
    # PSSA Anchors (1-4 score)
    focus = Column(Float, default=0.0)
    content = Column(Float, default=0.0)
    organization = Column(Float, default=0.0)
    style = Column(Float, default=0.0)
    conventions = Column(Float, default=0.0)
    
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User")

class WritingProject(Base):
    __tablename__ = "writing_projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String)
    phase = Column(String, default="Pre-writing")
    content = Column(Text, default="")
    history = Column(JSON, default=[]) # To store chat history if needed
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    user = relationship("User")
