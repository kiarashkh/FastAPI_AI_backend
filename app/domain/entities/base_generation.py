from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4, UUID

class BaseGeneration(ABC):
    """Abstract base class for all generations"""
    ### TODO: ADD SESSION ID TO THIS
    def __init__(self, prompt: str, model: str, gen_id:int = None, session_id:int = None, public_id:UUID = uuid4(), user_id: str = None):
        self.gen_id = gen_id
        self.public_id = public_id
        self.session_id = session_id
        self.prompt = prompt
        self.model = model
        self.user_id = user_id
        self.created_at = datetime.now()
        self.status = "pending"
    
    @abstractmethod
    def get_output(self) -> any:
        """Each generation type returns its output differently"""
        pass
    
    @abstractmethod
    def get_size(self) -> int:
        """Get size in bytes or tokens"""
        pass
    
    def complete(self):
        self.status = "completed"
    
    def fail(self, error: str):
        self.status = "failed"
        self.error = error