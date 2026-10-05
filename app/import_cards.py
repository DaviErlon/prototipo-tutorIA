import json
import os
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CARDS_FILE = PROJECT_ROOT / "data" / "cards.json"


def load_cards() -> list[dict[str, str]]:
    with CARDS_FILE.open(encoding="utf-8") as cards_file:
        cards: Any = json.load(cards_file)

    if not isinstance(cards, list):
        raise ValueError(f"{CARDS_FILE} deve conter uma lista de cards.")

    validated_cards: list[dict[str, str]] = []
    seen_ids: set[str] = set()

    for index, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            raise ValueError(f"Card {index} deve ser um objeto JSON.")

        card_id = card.get("id")
        title = card.get("title")
        content = card.get("content")
        if not all(isinstance(value, str) and value.strip() for value in (card_id, title, content)):
            raise ValueError(
                f"Card {index} precisa ter id, title e content como textos não vazios."
            )
        if card_id in seen_ids:
            raise ValueError(f"ID duplicado no arquivo: {card_id}")

        seen_ids.add(card_id)
        validated_cards.append(
            {
                "id": card_id,
                "title": title,
                "content": content,
            }
        )

    return validated_cards


def main() -> None:
    os.chdir(PROJECT_ROOT)
    cards = load_cards()

    from app.databases.chroma import get_collection
    from app.services.cards_service import formatar_documento_card

    collection = get_collection("cards")
    collection.upsert(
        ids=[f"json:{card['id']}" for card in cards],
        documents=[
            formatar_documento_card(card["title"], card["content"])
            for card in cards
        ],
        metadatas=[{"title": card["title"]} for card in cards],
    )

    print(f"Importados/atualizados {len(cards)} cards de {CARDS_FILE}.")
    print(f"Total de cards na coleção: {collection.count()}.")


if __name__ == "__main__":
    main()
