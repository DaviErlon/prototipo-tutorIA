from fastapi import APIRouter
from app.schemas.models import Chunk
from app.services.chunk_service import (
    criar_chunk,
    listar_chunks,
    deletar_chunk,
    buscar_chunks_semelhantes
)

chunks_router = APIRouter(
    prefix="/api/chunks"
)

# pesquisa inteligente de chunks
# criar chunks
# deletar chunks

@chunks_router.get("/")
def listar_chunks_route(key: str | None = None, page: int = 1, limit: int = 6):
    if key is not None:
        return buscar_chunks_semelhantes(key, limit)
    else:
        return listar_chunks(page, limit)


@chunks_router.post("/")
def criar_chunk_route(chunk: Chunk):
    return criar_chunk(chunk)


@chunks_router.delete("/{id}")
def deletar_chunk_route(id: str):
    return deletar_chunk(id)