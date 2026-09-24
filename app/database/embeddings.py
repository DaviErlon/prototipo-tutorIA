from chromadb import EmbeddingFunction
from ollama import embed


class OllamaEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: list[str]) -> list[list[float]]:
        resposta = embed(
            model="nomic-embed-text",
            input=input
        )

        return resposta["embeddings"]

# from chromadb import EmbeddingFunction
# from sentence_transformers import SentenceTransformer
# 
# 
# class BERTEmbeddingFunction(EmbeddingFunction):
#     def __init__(self):
#         self.model = SentenceTransformer(
#             "sentence-transformers/all-MiniLM-L6-v2"
#         )
# 
#     def __call__(self, input: list[str]) -> list[list[float]]:
#         embeddings = self.model.encode(input)
# 
#         return embeddings.tolist()
