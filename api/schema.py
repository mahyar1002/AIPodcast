from pydantic import BaseModel, Field

class NextRequest(BaseModel):
    session_id: str