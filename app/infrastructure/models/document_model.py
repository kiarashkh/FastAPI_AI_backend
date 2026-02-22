from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from .base import Base
from .document_tags import document_tags


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(64), unique=True, nullable=False, index=True)

    tags = relationship(
        "TagModel",
        secondary=document_tags,
        back_populates="documents"
    )