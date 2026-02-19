from app.infrastructure.llm.model import LLMModel
from app.domain.entities.generation import Generation

class LLMService:
    def __init__(self, model: LLMModel):
        self.model = model
        
    
    async def generate(self, prompt:str, max_tokens:int = 100):
        # TODO: Application logic (logging, metrics, etc.)
        
        result, num_tokens_used = self.model.generate(prompt, max_tokens)

        # Create domain entity

        generation = Generation(prompt=prompt, response=result, tokens_used=num_tokens_used)

        return generation