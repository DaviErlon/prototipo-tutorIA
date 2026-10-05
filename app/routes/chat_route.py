from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.models import Prompt
from app.services.ollama_service import send_to_llm, stream_and_save
from app.services.chat_service import (
    criar_chat,
    criar_mensagem,
    listar_chats,
    listar_mensagens,
    deletar_chat
)

chat_router = APIRouter(
    prefix="/api/chat"
)

# criar chat
# mandar mensagem para um chat
# listar chats
# buscar mensagens de um chat especifico
# deletar chat

@chat_router.post("/")
def criar_chat_route():
    chat_id = criar_chat()

    return {
        "id": chat_id
    }


@chat_router.post("/{id}")
def promt_route(id: int, prompt: Prompt):
    return send_to_llm(prompt.content, id)

@chat_router.post("/chats/{chat_id}/stream")
def prompt_stream(chat_id: int, prompt: Prompt):
    return StreamingResponse(
        stream_and_save(prompt.content, chat_id),
        media_type="text/plain; charset=utf-8"
    )


@chat_router.get("/")
def listar_chats_route():
    return listar_chats()


@chat_router.get("/{id}")
def mensagens_chat_route(id: int):
    return listar_mensagens(id)


@chat_router.delete("/{id}")
def deletar_chat_route(id: int):
    deletado = deletar_chat(id)

    if not deletado:
        raise HTTPException(
            status_code=404,
            detail="Chat não encontrado"
        )

    return {
        "message": "Chat deletado"
    }

