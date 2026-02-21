from abc import ABC, abstractmethod
from app.domain.entities.generation import Generation


class LLMInterface(ABC):
    """"Abstract interface for any LLM service"""

    @abstractmethod
    async def generate(self, prompt:str, max_tokens:int = 400) -> Generation:
        """"
        Generate text from prompt
        returns: (generated_text, token_count)
        """

        pass

    @abstractmethod
    async def get_model_name(self) -> str:
        """returns the model name being used"""
        pass
