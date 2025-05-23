from fastapi import APIRouter
from .schema import NextRequest, InitiateRequest
from .service import initiate_agents

router = APIRouter(prefix="/v1/podcast", tags=["PODCAST_V1"])


@router.post("/initiate")
async def initiate(params: InitiateRequest):
    response = await initiate_agents(params)
    return response


@router.post("/next")
async def next(params: NextRequest):
    print(params.session_id)
    return "speech text"
