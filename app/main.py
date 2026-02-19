from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import health, generate
from app.infrastructure.llm.model import LLMModel
from app.services.llm_service import LLMService






@asynccontextmanager
async def lifespan(app:FastAPI):
    # STARTUP: Load Model once
    # global llm_model, llm_service
    print("Loading LLM Model")

    model = LLMModel()
    model.load()

    app.state.llm_service = LLMService(model)

    print("Model loaded!")

    yield #App is running here

    #SHUTDOWN: Cleanup
    print("Shutting down...")
    llm_model = None
    llm_service = None

### WARNING!!!
# This part if for running model localy which should be done with care 
# since it will download 7 GB of model and on cpu it will take a lot of time

# app = FastAPI(title="LLM Backend", lifespan=lifespan, version="0.1.0")


app = FastAPI(title="LLM Backend", version="0.1.0")


# Base.metadata.create_all(bind=engine)



app.include_router(health.router, prefix="/api/v1")
app.include_router(generate.router, prefix="/api/v1")