from app.database.chroma import get_collection

def criar_card(card_id: str, titulo: str, conteudo: str):
    collection = get_collection("cards")

    collection.add(
        ids=[card_id],
        documents=[conteudo],
        metadatas=[
            {
                "titulo": titulo
            }
        ]
    )

def buscar_cards_semelhantes(texto: str, quantidade: int = 5):
    collection = get_collection("cards")

    resultado = collection.query(
        query_texts=[texto],
        n_results=quantidade
    )

    cards = []

    for i in range(len(resultado["ids"][0])):
        cards.append({
            "id": resultado["ids"][0][i],
            "titulo": resultado["metadatas"][0][i]["titulo"],
            "conteudo": resultado["documents"][0][i],
            "distancia": resultado["distances"][0][i]
        })

    return cards


def remover_card(card_id: str):
    collection = get_collection("cards")

    collection.delete(ids=[card_id])


def listar_cards(pagina: int = 1, quantidade: int = 20):
    collection = get_collection("cards")

    inicio = (pagina - 1) * quantidade

    resultado = collection.get(
        limit=quantidade,
        offset=inicio,
        include=["documents", "metadatas"]
    )

    total = collection.count()

    cards = []

    for i in range(len(resultado["ids"])):
        cards.append({
            "id": resultado["ids"][i],
            "titulo": resultado["metadatas"][i]["titulo"],
            "conteudo": resultado["documents"][i]
        })

    return {
        "data": cards,
        "pagination": {
            "page": pagina,
            "limit": quantidade,
            "total": total,
            "has_next": inicio + quantidade < total
        }
    }