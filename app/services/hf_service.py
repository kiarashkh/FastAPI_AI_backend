import httpx
from .llm_interface import LLMInterface
from app.domain.entities.generation import Generation


class HuggingFaceService(LLMInterface):
    def __init__(self, api_token: str, model: str = "deepseek-ai/DeepSeek-R1:fastest"):
        self.api_token = api_token
        self.model = model
        self.base_url = "https://router.huggingface.co/v1/chat/completions"
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(60.0, connect=10.0)
        )

    async def generate(self, prompt: str, max_tokens: int = 400) -> Generation:

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Answer concisely."
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        try:
            response = await self.client.post(
                self.base_url,
                headers=headers,
                json=payload
            )

            response.raise_for_status()
            data = response.json()

            text = data["choices"][0]["message"]["content"].strip()

            token_estimate = len(prompt.split()) + len(text.split())

            return Generation(
                prompt=prompt,
                response=text,
                tokens_used=token_estimate
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

    async def close(self):
        await self.client.aclose()