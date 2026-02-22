from .base_generation import BaseGeneration
from datetime import datetime
from uuid import UUID


class TextGeneration(BaseGeneration):
    def __init__(
        self,
        prompt: str,
        model: str,
        created_at: datetime | None = None,
        gen_id: int | None = None,
        session_id: int | None = None,
        public_id: UUID | None = None,
    ):
        super().__init__(
            prompt=prompt,
            model=model,
            created_at=created_at,
            gen_id=gen_id,
            session_id=session_id,
            public_id=public_id,
        )

        self.generated_text: str | None = None
        self.tokens_used: int = 0

    def set_result(self, text: str, tokens_used: int):
        self.generated_text = text
        self.tokens_used = tokens_used
        self.complete()

    def get_output(self) -> str | None:
        return self.generated_text

    def get_size(self) -> int:
        return self.tokens_used