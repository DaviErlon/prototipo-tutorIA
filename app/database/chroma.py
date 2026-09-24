import chromadb
from app.database.embeddings import OllamaEmbeddingFunction

client = chromadb.PersistentClient(path="./chroma_data")

embedding_function = OllamaEmbeddingFunction()

def get_collection(name: str = "default"):
    return client.get_or_create_collection(
        name=name,
        embedding_function=embedding_function
    )