from pydantic import BaseModel, Field


class GuestModel(BaseModel):
    name: str
    comapny: str
    characteristics: str


class HostModel(BaseModel):
    name: str
    topic: str


class InitiateRequest(BaseModel):
    host: HostModel
    guests: list[GuestModel] = Field(default_factory=list)



class NextRequest(BaseModel):
    session_id: str
