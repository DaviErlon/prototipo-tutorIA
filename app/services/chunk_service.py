from app.databases.postgres import get_connection
from app.schemas.models import Chunk

# gerar_embedding(texto) -> list[float] com 768 dimensões (tem que bater com VECTOR(768)).
# No Chroma isso era feito automaticamente pela collection; agora é responsabilidade do código.
from app.services.embedding_service import gerar_embedding

# Pressupostos:
# - get_connection() retorna uma conexão psycopg 3 com row_factory=dict_row
# - Chunk possui: content, document, page e type ('text', ou outros valores de type_doc)

def _to_pgvector(embedding: list[float]) -> str:
    # Formato textual aceito pelo pgvector: '[0.1,0.2,...]'
    return "[" + ",".join(str(float(x)) for x in embedding) + "]"


def criar_chunk(chunk: Chunk):
    embedding = _to_pgvector(gerar_embedding(chunk.content))

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO chunks (content, document, page, type, vector_embedding)
            VALUES (%s, %s, %s, %s::type_doc, %s::vector)
            RETURNING id, content
            """,
            (chunk.content, chunk.document, chunk.page, chunk.type, embedding)
        )

        row = cursor.fetchone()
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {
        "id": row["id"],
        "content": row["content"]
    }


def buscar_chunks_semelhantes(texto: str, limit: int = 6):
    embedding = _to_pgvector(gerar_embedding(texto))

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                content,
                vector_embedding <=> %s::vector AS distance
            FROM chunks
            ORDER BY vector_embedding <=> %s::vector
            LIMIT %s
            """,
            (embedding, embedding, limit)
        ).fetchall()
    finally:
        connection.close()

    return [
        {
            "id": row["id"],
            "content": row["content"],
            "distance": row["distance"]
        }
        for row in rows
    ]


def deletar_chunk(chunk_id: int):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM chunks
            WHERE id = %s
            """,
            (chunk_id,)
        )

        deletado = cursor.rowcount > 0
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return deletado


def listar_chunks(page: int = 1, limit: int = 6):
    inicio = (page - 1) * limit

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT id, content
            FROM chunks
            ORDER BY id
            LIMIT %s OFFSET %s
            """,
            (limit, inicio)
        ).fetchall()

        total = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM chunks
            """
        ).fetchone()["total"]
    finally:
        connection.close()

    return {
        "data": [dict(row) for row in rows],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "has_next": inicio + limit < total
        }
    }