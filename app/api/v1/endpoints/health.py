from fastapi import APIRouter, HTTPException
from ....core.constants import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "service is running"}

