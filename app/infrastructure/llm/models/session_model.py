from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(64), unique=True, nullable=False, index=True)

    user_id = Column(String(64), ForeignKey("users.id"), nullable=False)

    # Relationships
    uploaded_docs = relationship(
        "DocumentModel",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    rag_generations = relationship(
        "RAGGenerationModel",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    text_generations = relationship(
        "TextGenerationModel",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    image_generations = relationship(
        "ImageGenerationModel",
        back_populates="session",
        cascade="all, delete-orphan"
    )