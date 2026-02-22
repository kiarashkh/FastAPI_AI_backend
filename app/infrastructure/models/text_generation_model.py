from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class TextGenerationModel(Base):
    __tablename__ = "text_generations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(64), unique=True, nullable=False, index=True)

    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)

    model = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    prompt = Column(String(2048), nullable=False)

    status = Column(String(32), nullable=False, default="pending", index=True)
    error = Column(String(256), nullable=True)

    response = Column(String(4096), nullable=True)
    tokens_used = Column(Integer, nullable=True)

    session = relationship("SessionModel", back_populates="text_generations")