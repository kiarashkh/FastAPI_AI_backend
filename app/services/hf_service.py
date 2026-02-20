import httpx

# TODO: change url names to const
# from app.core.constants import
from .llm_interface import LLMInterface
from app.domain.entities.generation import Generation


class HuggingFaceService(LLMInterface):
    def __init__(self, api_token: str, model: str = "HuggingFaceH4/zephyr-7b-beta"):
        self.api_token = api_token
        self.model = model
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(60.0, connect=10.0)
        )

    async def generate(self, prompt: str, max_tokens: int = 100) -> tuple[str, int]:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "return_full_text": False,
                "temperature": 0.7,
                "do_sample": True
            }
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

            # Raise proper HTTP error if HF fails
            response.raise_for_status()

            data = response.json()

            # HF sometimes returns dict with "error"
            if isinstance(data, dict) and "error" in data:
                raise RuntimeError(f"HuggingFace API error: {data['error']}")

            # Normal generation response
            if isinstance(data, list) and len(data) > 0:
                text = data[0].get("generated_text", "").strip()
            else:
                text = str(data)

            # simple token estimate (kept same structure you wanted)
            token_estimate = len(prompt.split()) + len(text.split())

            generation = Generation(prompt=prompt, response=text, tokens_used=token_estimate)

            return generation

        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"HuggingFace request failed: {e.response.status_code} {e.response.text}"
            ) from e

        except httpx.RequestError as e:
            raise RuntimeError(f"Network error while calling HuggingFace: {str(e)}") from e

    async def get_model_name(self) -> str:
        return f"hf-{self.model}"
    # TODO: refactor main so it closes the connection
    async def close(self):
        await self.client.aclose()