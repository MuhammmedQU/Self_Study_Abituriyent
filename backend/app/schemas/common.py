from pydantic import BaseModel


class MessageResponse(BaseModel):
    success: bool = True
    message: str
    data: dict | list | None = None
