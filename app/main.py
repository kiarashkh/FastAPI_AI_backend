import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import health, generate


from app.services import create_llm_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Choose based on environment variable or config
    service_type = os.getenv("LLM_SERVICE", "huggingface")  # or "local"
    
    print(f"Creating LLM service: {service_type}")
    llm_service = create_llm_service(service_type)
    
    app.state.llm_service = llm_service
    yield

    print("Shutting down...")



app = FastAPI(title="LLM Backend", version="0.1.0", lifespan=lifespan)


# Base.metadata.create_all(bind=engine)



app.include_router(health.router, prefix="/api/v1")
app.include_router(generate.router, prefix="/api/v1")