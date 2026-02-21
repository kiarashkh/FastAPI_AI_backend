from typing import List
from datetime import datetime
from uuid import UUID, uuid4


class Document:
    def __init__(
        self,
        doc_id: int | None,
        filename: str,
        text: str,
        header: str | None,
        tags: List[str] | None,
        public_id: UUID | None = None,
        user_id: int | None = None,
    ):
        self.doc_id = doc_id          # DB PK
        self.public_id = public_id or uuid4()
        self.file_name = filename
        self.text = text
        self.header = header
        self.tags = tags or []
        self.user_id = user_id
