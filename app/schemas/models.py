from pydantic import BaseModel, Field

class Prompt(BaseModel):
    content: str

class Card(BaseModel):
    title: str
    content: str

class Message(BaseModel):
    id: int
    content: str
    role: str
    sent_at: str
    chat_id: int