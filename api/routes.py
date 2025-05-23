from fastapi import APIRouter
from .schema import NextRequest
from .service import initiate_agents

router = APIRouter(prefix="/v1/podcast", tags=["PODCAST_V1"])


@router.get("/initiate")
async def initiate():
    response = await initiate_agents()
    return response


@router.post("/next")
async def next(params: NextRequest):
    print(params.session_id)
    return "speech text"
