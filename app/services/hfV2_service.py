import httpx
from .llm_interface import LLMInterface
from app.domain.entities.generation import Generation
from huggingface_hub import AsyncInferenceClient



class HuggingFaceServiceV2(LLMInterface):
    def __init__(self, api_token: str, model: str = "deepseek-ai/DeepSeek-R1:fastest"):
        self.api_token = api_token
        self.model = model
        self.client = AsyncInferenceClient(model=model, token=api_token)

    async def generate(self, prompt: str, max_tokens: int = 400) -> Generation:

        messages = [
            {
                "role" : "system",
                "content" : "Answer concisely."
            },
            {
                "role" : "user",
                "content" : prompt
            }
        ]

        try:
            result = await self.client.chat_completion(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temprature=0.7
            )

            text = result.choices[0].message.content

            token_estimate = len(prompt.split()) + len(text.split())

            return Generation(
                prompt=prompt,
                response=text,
                tokens_used=token_estimate,
                model=self.model
            )

        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"HuggingFace request failed: {e.response.status_code} {e.response.text}"
            ) from e

        except httpx.RequestError as e:
            raise RuntimeError(
                f"Network error while calling HuggingFace: {str(e)}"
            ) from e

    async def get_model_name(self) -> str:
        return f"hf-{self.model}"
    
