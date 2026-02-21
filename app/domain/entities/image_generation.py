from .base_generation import BaseGeneration
from enum import Enum
from datetime import datetime
from uuid import UUID


class ImageFormat(Enum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"


class ImageGeneration(BaseGeneration):
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

        self.image_url: str | None = None
        self.image_data: bytes | None = None   # optional raw storage
        self.format: ImageFormat | None = None
        self.width: int | None = None
        self.height: int | None = None

    def set_result(
        self,
        image_url: str,
        format: ImageFormat,
        width: int,
        height: int,
        image_data: bytes | None = None,
    ):
        self.image_url = image_url
        self.image_data = image_data
        self.format = format
        self.width = width
        self.height = height
        self.complete()

    def get_output(self) -> dict:
        return {
            "url": self.image_url,
            "format": self.format.value if self.format else None,
            "dimensions": f"{self.width}x{self.height}" if self.width and self.height else None,
        }

    def get_size(self) -> int:
        # Rough estimate (RGB bytes)
        if self.width and self.height:
            return self.width * self.height * 3
        return 0