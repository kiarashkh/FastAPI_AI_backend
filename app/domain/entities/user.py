from .session import Session

from typing import List
from uuid import uuid4, UUID

class User:
    def __init__(self, name:str, password:str, user_id:int | None = None, public_id:UUID | None = None):
        self.name = name
        self.password = password
        self.user_id = user_id
        self.public_id = public_id or uuid4()