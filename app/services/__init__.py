import os

from .llm_interface import LLMInterface
from .hf_service import HuggingFaceService
from .local_llm_service import LocalLLMService

def create_llm_service(service_type:str = None) -> LLMInterface:
    """Factory function to create the appropriate LLM service"""
    if service_type is None:
        service_type = os.getenv("LLM_SERVICE_TYPE", "huggingface")
    if service_type == "huggingface":
        token = os.getenv("HUGGINGFACE_TOKEN")
        if not token:
            raise ValueError("HUGGINGFACE_TOKEN environment variable required")
        return HuggingFaceService(api_token=token)
    elif service_type == "local":
        return LocalLLMService()
    else:
        raise ValueError(f"UNknown service type: {service_type}")
    