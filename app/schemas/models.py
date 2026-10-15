from pydantic import BaseModel

class Prompt(BaseModel):
    content: str

class Chunk(BaseModel):
    content: str
    document: str = ""
    page: int = 1
    type: str = "text"

class Message(BaseModel):
    id: int
    content: str
    role: str
    sent_at: str
    chat_id: int