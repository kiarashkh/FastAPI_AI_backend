from app.infrastructure.llm.model import LLMModel
from app.services.llm_interface import LLMInterface
from app.domain.entities.generation import Generation
from app.core.constants import GENERATE_TEXT_MODEL_NAME


from .llm_interface import LLMInterface
from app.infrastructure.llm.model import LLMModel

class LocalLLMService(LLMInterface):
    def __init__(self, model_name: str = GENERATE_TEXT_MODEL_NAME):
        self.model = LLMModel(model_name)
        self.model.load()
    
    async def generate(self, prompt: str, max_tokens: int = 400) -> tuple[str, int]:
        # Run CPU-bound operation in thread pool
        import asyncio
        result, tokens = await asyncio.to_thread(
            self.model.generate, prompt, max_tokens
        )
        generation = Generation(prompt=prompt, response=result, tokens_used=tokens, model=self.model)

        return generation
    
    async def get_model_name(self) -> str:
        return f"local-{self.model.model_name}"
