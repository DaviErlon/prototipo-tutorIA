from ollama import embed

def gerar_embedding(texto: str) -> list[float]:
    resposta = embed(
        model="nomic-embed-text",
        input=texto
    )

    return resposta["embeddings"][0]