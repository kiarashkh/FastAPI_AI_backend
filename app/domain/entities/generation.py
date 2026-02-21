from datetime import datetime


class Generation:
    def __init__(self, prompt: str, response: str, tokens_used:int, model:str):
        self.prompt = prompt
        self.response = response
        self.created_at = datetime.now()
        self.model = model
        self.status = "completed"
        self.tokens_used = tokens_used
        
    def is_valid(self) -> bool:
        return len(self.response) > 0