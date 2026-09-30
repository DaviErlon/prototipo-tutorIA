from fastapi import APIRouter
from app.schemas.models import Card
from app.services.cards_service import (
    criar_card,
    listar_cards,
    deletar_card,
    buscar_cards_semelhantes
)

cards_router = APIRouter(
    prefix="/api/cards"
)

# pesquisa inteligente de cards
# criar cards
# deletar cards

@cards_router.get("/")
def listar_cards_route(key: str | None = None, page: int = 1, limit: int = 15):
    if key is not None:
        return buscar_cards_semelhantes(key, limit)
    else:
        return listar_cards(page, limit)
    
@cards_router.post("/")
def criar_card_route(card: Card):
    criar_card(card)


@cards_router.delete("/{id}")
def deletar_card_route(id: str):
    deletar_card(id)
