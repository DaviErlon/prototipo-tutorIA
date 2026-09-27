from fastapi import APIRouter, HTTPException

from app.schemas.models import Prompt
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

@chat_router.post("/")
def criar_chat_route():
    chat_id = criar_chat()

    return {
        "id": chat_id
    }


@chat_router.post("/{id}")
def promt_route(id: int, prompt: Prompt):

    # executar aqui a logica de RAG
    # busca mensagens no lite e
    # referencias no chroma
    # e dps chama o ollama hihi
    
    mensagem_id = criar_mensagem(
        chat_id=id,
        content=prompt.content,
        role="user"
    )

    return {
        "id": mensagem_id
    }


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