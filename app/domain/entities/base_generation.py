from abc import ABC, abstractmethod
from datetime import datetime, timezone
from uuid import uuid4, UUID
from enum import Enum


class GenerationStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class BaseGeneration(ABC):
    """Abstract base class for all generations"""

    def __init__(
        self,
        prompt: str,
        model: str,
        created_at: datetime | None = None,
        gen_id: int | None = None,
        session_id: int | None = None,
        public_id: UUID | None = None,
    ):
        self.gen_id = gen_id                                       # DB primary key
        self.public_id = public_id or uuid4()                      # External ID
        self.session_id = session_id                               # FK to session                                # FK to user
        self.created_at = created_at or datetime.now(timezone.utc) #creation time in DB

        self.prompt = prompt
        self.model = model
        self.status = GenerationStatus.PENDING
        self.error: str | None = None

    @abstractmethod
    def get_output(self) -> any:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    def complete(self):
        self.status = GenerationStatus.COMPLETED

    def fail(self, error: str):
        self.status = GenerationStatus.FAILED
        self.error = error