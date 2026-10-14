from pydantic import BaseModel

class Prompt(BaseModel):
    content: str

class Chunk(BaseModel):
    content: str

class Message(BaseModel):
    id: int
    content: str
    role: str
    sent_at: str
    chat_id: int