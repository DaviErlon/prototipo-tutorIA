import json
from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "chunks.json"
DB_PATH = BASE_DIR / "chroma_data"
COLLECTION_NAME = "chunks"

from chromadb import EmbeddingFunction
from ollama import embed


class OllamaEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: list[str]) -> list[list[float]]:
        resposta = embed(
            model="nomic-embed-text",
            input=input
        )

        return resposta["embeddings"]
    
def main():
    print(f"Lendo: {JSON_PATH}")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"{len(chunks)} chunks carregados.")

    client = chromadb.PersistentClient(path=str(DB_PATH))

    # Apaga a coleção antiga (que estava com dimensão 768)
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Coleção '{COLLECTION_NAME}' antiga removida.")
    except Exception:
        pass

    embedding_function = OllamaEmbeddingFunction()

    # Cria de novo, agora com o embedding padrão do Chroma (384 dims)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"},
    )

    collection.upsert(
        ids=[c["id"] for c in chunks],
        documents=[c["document"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )

    print(f"Upsert OK. Total na coleção: {collection.count()}")


if __name__ == "__main__":
    main()