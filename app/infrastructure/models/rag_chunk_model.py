from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base



class RAGChunkModel(Base):
    __tablename__ = "rag_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rag_id = Column(Integer, ForeignKey("rag_generations.id"), nullable=False)

    content = Column(String)
    rank = Column(Integer)   # order sent to LLM
    score = Column(Float)    # similarity score

    rag = relationship("RAGGenerationModel", back_populates="chunks")