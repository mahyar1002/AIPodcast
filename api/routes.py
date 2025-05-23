from fastapi import APIRouter
from .schema import NextRequest, InitiateRequest, VoiceModel
from .service import initiate_agents, synthesize_speech
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/v1/podcast", tags=["PODCAST_V1"])


@router.post("/initiate")
async def initiate(params: InitiateRequest):
    response = await initiate_agents(params)
    return response


@router.post("/voice")
async def voice(params: VoiceModel):
    audio_stream = await synthesize_speech(params.text, params.voice_name)

    return StreamingResponse(
        audio_stream,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=voice.mp3"}
    )
