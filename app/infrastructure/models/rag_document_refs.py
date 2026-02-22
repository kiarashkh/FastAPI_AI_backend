from sqlalchemy import Column, Float, ForeignKey, Table
from .base import Base


rag_document_refs = Table(
    "rag_document_refs",
    Base.metadata,
    Column("rag_id", ForeignKey("rag_generations.id"), primary_key=True),
    Column("document_id", ForeignKey("documents.id"), primary_key=True),
    Column("relevance", Float, nullable=False),
)