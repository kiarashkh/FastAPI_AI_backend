from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from uuid import uuid4, UUID
from datetime import datetime

from ....core.constants import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, GENERATE_TEXT_MODEL_NAME
from app.services.llm_interface import LLMInterface
from app.api.dependencies import get_llm_service


router = APIRouter()

max_gen_req_index = 0
max_gen_res_index = 0

class GenerateResponseBase(BaseModel):
    generated_text : str = Field(..., min_length=2, max_length= 512, description='response of model')
    model_used : str = Field(..., max_length=64, description="model used to generate text")
    tokens_used : int = Field(..., description="number of tokens used")


class GenerateResponseCreate(GenerateResponseBase):
    pass

class GenerateResponse(GenerateResponseBase):
    generated_response_id : UUID = Field(default_factory=uuid4, description="id of the generation response")
    created_at: datetime = Field(default_factory=datetime.now, description="date the Response was made")


class GenerateRequestBase(BaseModel):
    prompt : str = Field(..., min_length=2, max_length= 512, description='Prompt of Generate Request')
    max_tokens : int = Field(default=100, description="max number of tokens")
    temperature : float = Field(default=0.7, description="temprature for model generation")


class GenerateRequestCreate(GenerateRequestBase):
    pass

class GenerateRequest(GenerateRequestBase):
    generated_request_id : UUID = Field(default_factory=uuid4, description="id of the generation request")
    created_at: datetime = Field(default_factory=datetime.now, description="date generate request made")

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(
    request : GenerateRequestCreate,
    llm_service: LLMInterface = Depends(get_llm_service)
    ):
    try:
        ###logic of creating the GenerateRequest and adding it for the user
        result = await llm_service.generate(
            prompt=request.prompt, max_tokens=request.max_tokens
        )


        # TODO: change Generated model name to what the model is actually using in runtime
        return GenerateResponse(
            generated_text=result.response,
            model_used=GENERATE_TEXT_MODEL_NAME,
            tokens_used=result.tokens_used,
            # TODO: link ID of generated response to Generate_request and save both
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
