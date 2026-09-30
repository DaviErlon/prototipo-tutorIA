from app.config.settings import OLLAMA_URL, MODEL
import requests

# definir hiper parâmetros da llm

# historico: list[message], cards: list[card]
# gerar o prompt padrao (engenharia de prompt)

def send_to_llm(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]