import json
from pathlib import Path
from app.databases.chroma import get_collection


def script():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    JSON_PATH = BASE_DIR / "chunks.json"

    print(f"Lendo: {JSON_PATH}")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"{len(chunks)} chunks carregados.")

    collection = get_collection("chunks")

    collection.upsert(
        ids=[c["id"] for c in chunks],
        documents=[c["document"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )

    print(f"Upsert OK. Total na coleção: {collection.count()}")


if __name__ == "__main__":
    script()