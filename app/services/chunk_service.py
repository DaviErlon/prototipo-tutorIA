from app.databases.postgres import get_connection
from app.schemas.models import Chunk
from app.services.embedding_service import gerar_embedding

RRF_K = 60

def _to_pgvector(embedding: list[float]) -> str:
    # Formato textual aceito pelo pgvector: '[0.1,0.2,...]'
    return "[" + ",".join(str(float(x)) for x in embedding) + "]"


def criar_chunk(chunk: Chunk):
    embedding = _to_pgvector(gerar_embedding(chunk.content))

    connection = get_connection()

    try:
        # O índice BM25 é atualizado automaticamente na mesma transação.
        cursor = connection.execute(
            """
            INSERT INTO chunks (content, document, page, type, vector_embedding)
            VALUES (%s, %s, %s, %s::type_doc, %s::vector)
            RETURNING id, content
            """,
            (chunk.content, chunk.document, chunk.page, chunk.type, embedding),
        )

        row = cursor.fetchone()
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {"id": row["id"], "content": row["content"]}


def buscar_chunks_semelhantes(
    texto: str,
    limit: int = 6,
    candidatos: int = 16,
    peso_semantico: float = 1.0,
    peso_textual: float = 1.0,
):
    """
    Busca híbrida: combina busca vetorial (pgvector) e busca lexical BM25
    (pg_search / ParadeDB) usando Reciprocal Rank Fusion (RRF).

    - candidatos: quantos resultados cada busca traz antes de fundir.
    - peso_semantico / peso_textual: ajustam a influência de cada busca.
    """
    embedding = _to_pgvector(gerar_embedding(texto))

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            WITH semantica AS (
                SELECT
                    id,
                    ROW_NUMBER() OVER (
                        ORDER BY vector_embedding <=> %(embedding)s::vector
                    ) AS rank
                FROM chunks
                ORDER BY vector_embedding <=> %(embedding)s::vector
                LIMIT %(candidatos)s
            ),
            textual AS (
                SELECT
                    id,
                    ROW_NUMBER() OVER (ORDER BY pdb.score(id) DESC) AS rank
                FROM chunks
                WHERE content ||| %(texto)s::text
                ORDER BY pdb.score(id) DESC
                LIMIT %(candidatos)s
            )
            SELECT
                c.id,
                c.content,
                c.document,
                c.page,
                c.vector_embedding <=> %(embedding)s::vector AS distance,
                s.rank AS rank_semantico,
                t.rank AS rank_textual,
                COALESCE(%(peso_semantico)s / (%(rrf_k)s + s.rank), 0)
                + COALESCE(%(peso_textual)s / (%(rrf_k)s + t.rank), 0) AS score
            FROM semantica s
            FULL OUTER JOIN textual t ON t.id = s.id
            JOIN chunks c ON c.id = COALESCE(s.id, t.id)
            ORDER BY score DESC
            LIMIT %(limit)s
            """,
            {
                "embedding": embedding,
                "texto": texto,
                "candidatos": candidatos,
                "peso_semantico": peso_semantico,
                "peso_textual": peso_textual,
                "rrf_k": RRF_K,
                "limit": limit,
            },
        ).fetchall()
    finally:
        connection.close()

    return [
        {
            "id": row["id"],
            "content": row["content"],
            "document": row["document"],
            "page": row["page"],
            "distance": row["distance"],
            "score": float(row["score"]),
            "rank_semantico": row["rank_semantico"],
            "rank_textual": row["rank_textual"],
        }
        for row in rows
    ]


def deletar_chunk(chunk_id: int):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM chunks WHERE id = %s",
            (chunk_id,),
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
            (limit, inicio),
        ).fetchall()

        total = connection.execute(
            "SELECT COUNT(*) AS total FROM chunks"
        ).fetchone()["total"]
    finally:
        connection.close()

    return {
        "data": [dict(row) for row in rows],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "has_next": inicio + limit < total,
        },
    }