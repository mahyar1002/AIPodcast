from fastapi import APIRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from .schema import NextRequest

router = APIRouter(prefix="/v1/podcast", tags=["PODCAST_V1"])
parser = StrOutputParser()


@router.get("/initiate")
async def initiate():
    return "session_id"


@router.post("/next")
async def next(params: NextRequest):
    print(params.session_id)
    return "speech text"
