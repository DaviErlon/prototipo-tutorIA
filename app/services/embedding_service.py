import httpx
from ollama import Client
from app.config.settings import OLLAMA_HOST

_client = Client(
    host=OLLAMA_HOST,
    timeout=httpx.Timeout(120.0, connect=5.0),
)

def gerar_embedding(texto: str) -> list[float]:
    resposta = _client.embed(
        model="nomic-embed-text",
        input=texto
    )

    return resposta["embeddings"][0]