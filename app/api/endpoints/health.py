from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    """Get Ping"""

    return "pong"