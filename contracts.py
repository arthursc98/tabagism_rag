from pydantic import BaseModel


class Request(BaseModel):
    conversation_id: str
    text: str
