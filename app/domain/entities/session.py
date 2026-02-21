from datetime import datetime, timezone
from uuid import UUID, uuid4


class Session:
    def __init__(
        self,
        created_at: datetime | None = None,
        session_id: int | None = None,
        public_id: UUID | None = None,
        user_id: int | None = None,
    ):
        self.session_id = session_id              # DB PK
        self.public_id = public_id or uuid4()     # External reference
        self.user_id = user_id                    # FK (nullable for guests)
        self.created_at = created_at or datetime.now(timezone.utc)