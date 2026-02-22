from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class RAGGenerationModel(Base):
    __tablename__ = "rag_generations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(64), unique=True, nullable=False, index=True)

    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)

    prompt = Column(String(2048), nullable=False)
    model = Column(String(64))
    created_at = Column(DateTime(), nullable=False)

    response = Column(String(4096))
    tokens_used = Column(Integer)

    session = relationship("SessionModel", back_populates="rag_generations")

    documents = relationship(
        "DocumentModel",
        secondary="rag_document_refs",
        back_populates="rag_generations"
    )

    chunks = relationship("RAGChunkModel", back_populates="rag")