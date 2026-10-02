import requests
import json

from app.config.settings import OLLAMA_URL, MODEL
from app.services.cards_service import buscar_cards_semelhantes
from app.services.chat_service import listar_mensagens, criar_mensagem

# definir hiper parâmetros da llm

# historico: list[message], cards: list[card]
# gerar o prompt padrao (engenharia de prompt)]

def generate_default_prompt(content: str, chat_id: int):
    
    messages = listar_mensagens(chat_id)[-8:]
    cards = buscar_cards_semelhantes(content, limit=3)

    system_content = """
Você é a TutorIA, uma inteligência artificial responsável por auxiliar
o usuário em seus estudos.

Você pode utilizar o material dos cards fornecidos abaixo para embasar
suas respostas. Os cards são materiais de estudo recuperados por
similaridade e podem ser utilizados como contexto adicional.

Não mencione os cards ou o processo de recuperação de contexto ao usuário,
a menos que isso seja relevante para a resposta.

Utilize o conteúdo dos cards como material de apoio, mas não invente
informações que não estejam presentes no contexto ou que você não saiba.

CARDS DE CONTEXTO:
"""

    for i, card in enumerate(cards, start=1):
        system_content += f"""

--- CARD {i} ---
{card["content"]}

"""

    prompt = [
        {
            "role": "system",
            "content": system_content.strip()
        }
    ]

    for message in messages:
        prompt.append({
            "role": message["role"],
            "content": message["content"]
        })

    if content:
        prompt.append({
            "role": "user",
            "content": content
        })

    return prompt


def send_to_llm(content: str, chat_id: int):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": generate_default_prompt(content, chat_id),
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


def send_to_llm_stream(content: str, chat_id: int):
    with requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": generate_default_prompt(content, chat_id),
            "stream": True
        },
        stream=True,
        timeout=(5, 120)
    ) as response:
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line)

            if "error" in data:
                raise RuntimeError(data["error"])

            chunk = data.get("message", {}).get("content", "")
            if chunk:
                yield chunk

            if data.get("done"):
                break

def stream_and_save(content: str, chat_id: int):
    resposta_completa = []
    try:
        for chunk in send_to_llm_stream(content, chat_id):
            resposta_completa.append(chunk)
            yield chunk
    finally:
        texto = "".join(resposta_completa)
        if texto:
            criar_mensagem(chat_id, role="user", content=content)
            criar_mensagem(chat_id, role="assistant", content=texto)