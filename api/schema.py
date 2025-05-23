from pydantic import BaseModel, Field


class GuestModel(BaseModel):
    name: str
    company: str
    characteristics: str


class HostModel(BaseModel):
    name: str
    topic: str


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
