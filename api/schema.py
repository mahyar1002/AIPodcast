from pydantic import BaseModel, Field
from typing import Literal


class GuestModel(BaseModel):
    name: str
    voice_name: str
    company: str
    characteristics: str


class HostModel(BaseModel):
    name: str
    topic: str
    voice_name: str


class InitiateRequest(BaseModel):
    host: HostModel
    guests: list[GuestModel] = Field(
        default_factory=list,
        min_length=2,
        max_length=2,
        description="Must contain exactly 2 guests"
    )


class NextRequest(BaseModel):
    session_id: str

class VoiceModel(BaseModel):
    voice_name: str
    text: str