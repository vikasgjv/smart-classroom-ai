from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from database import Base

class Emotion(Base):
    __tablename__ = "emotions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String)
    emotion = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Attention(Base):
    __tablename__ = "attention"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String)
    attention_score = Column(Float)
    mobile_detected = Column(Boolean, default=False)
    mobile_confidence = Column(Float, default=0.0)
    distraction_level = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)
