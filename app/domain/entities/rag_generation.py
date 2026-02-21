from .text_generation import TextGeneration
from typing import List
from datetime import datetime
from uuid import UUID

from .document import Document


# class DocumentRef:
#     """Join entity between RAGGeneration and Document"""

#     def __init__(self, doc_id: int, relevance: float):
#         self.doc_id = doc_id
#         self.relevance = relevance


class RAGGeneration(TextGeneration):
    def __init__(
        self,
        prompt: str,
        model: str,
        created_at: datetime | None = None,
        gen_id: int | None = None,
        session_id: int | None = None,
        public_id: UUID | None = None,
        user_id: int | None = None,
    ):
        super().__init__(
            prompt=prompt,
            model=model,
            created_at=created_at,
            gen_id=gen_id,
            session_id=session_id,
            public_id=public_id,
            user_id=user_id,
        )

        self.documents_used: List[Document] = []
        self.context_chunks: List[str] = []

    def add_document(self, doc_id: int, relevance: float):
        self.documents_used.append(Document(doc_id, relevance))

    def set_result(
        self,
        text: str,
        tokens_used: int,
        context_chunks: List[str] | None = None,
    ):
        super().set_result(text, tokens_used)
        self.context_chunks = context_chunks or []

    def get_sources(self) -> List[dict]:
        return [
            {
                "doc_id": d.doc_id,
                "relevance": d.relevance,
            }
            for d in self.documents_used
        ]