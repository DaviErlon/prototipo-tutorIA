import uuid

from app.databases.chroma import get_collection
from app.schemas.models import Chunk

def criar_chunk(chunk: Chunk):
    collection = get_collection("chunks")

    chunk_id = str(uuid.uuid4())

    collection.add(
        ids=[chunk_id],
        documents=[chunk.content]
    )

    return {
        "id": chunk_id,
        "content": chunk.content
    }


def buscar_chunks_semelhantes(texto: str, limit: int = 6):
    collection = get_collection("chunks")

    resultado = collection.query(
        query_texts=[texto],
        n_results=limit
    )

    chunks = []

    for i in range(len(resultado["ids"][0])):
        chunks.append({
            "id": resultado["ids"][0][i],
            "content": resultado["documents"][0][i],
            "distance": resultado["distances"][0][i]
        })

    return chunks


def deletar_chunk(chunk_id: str):
    collection = get_collection("chunks")

    collection.delete(
        ids=[chunk_id]
    )


def listar_chunks(page: int = 1, limit: int = 6):
    collection = get_collection("chunks")

    inicio = (page - 1) * limit

    resultado = collection.get(
        limit=limit,
        offset=inicio,
        include=["documents"]
    )

    total = collection.count()

    chunks = []

    for i in range(len(resultado["ids"])):
        chunks.append({
            "id": resultado["ids"][i],
            "content": resultado["documents"][i]
        })

    return {
        "data": chunks,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "has_next": inicio + limit < total
        }
    }