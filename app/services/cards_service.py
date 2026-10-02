import uuid

from app.databases.chroma import get_collection
from app.schemas.models import Card


def criar_card(card: Card):
    collection = get_collection("cards")

    card_id = str(uuid.uuid4())

    collection.add(
        ids=[card_id],
        documents=[card.content],
        metadatas=[
            {
                "title": card.title
            }
        ]
    )

    return {
        "id": card_id,
        "title": card.title,
        "content": card.content
    }

def buscar_cards_semelhantes(texto: str, limit: int = 6):
    collection = get_collection("cards")

    resultado = collection.query(
        query_texts=[texto],
        n_results=limit
    )

    cards = []

    for i in range(len(resultado["ids"][0])):

        cards.append({
            "id": resultado["ids"][0][i],
            "title": resultado["metadatas"][0][i]["title"],
            "content": resultado["documents"][0][i],
            "distance": resultado["distances"][0][i]
        })

    return cards


def deletar_card(card_id: str):
    collection = get_collection("cards")

    collection.delete(
        ids=[card_id]
    )

def listar_cards(page: int = 1, limit: int = 6):
    collection = get_collection("cards")

    inicio = (page - 1) * limit

    resultado = collection.get(
        limit=limit,
        offset=inicio,
        include=["documents", "metadatas"]
    )

    total = collection.count()

    cards = []

    for i in range(len(resultado["ids"])):
        cards.append({
            "id": resultado["ids"][i],
            "title": resultado["metadatas"][i]["title"],
            "content": resultado["documents"][i]
        })

    return {
        "data": cards,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "has_next": inicio + limit < total
        }
    }