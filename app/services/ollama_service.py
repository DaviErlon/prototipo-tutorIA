import requests
import json

from app.config.settings import OLLAMA_URL, MODEL, TEMPERATURE
from app.services.cards_service import buscar_cards_semelhantes
from app.services.chat_service import listar_mensagens, criar_mensagem

# definir hiper parâmetros da llm

# historico: list[message], cards: list[card]
# gerar o prompt padrao (engenharia de prompt)]

def generate_default_prompt(content: str, chat_id: int):
    
    messages = listar_mensagens(chat_id)[-4:]
    chunks = buscar_cards_semelhantes(content, limit=3)

    # filtro de chunks aqui

    system_content = """
Você é a TutorIA, uma inteligência artificial responsável por auxiliar
os universitários da universidade Unopar em suas dúvidas acadêmicas e institucionais.

Você pode utilizar o material fornecido abaixo para embasar
suas respostas. Os chunks são materiais de estudo recuperados por
similaridade e podem ser utilizados como contexto adicional.

Nunca mencione os chunks ou o processo de recuperação de contexto ao usuário.

Se não houver chunks de contexto, diga ao usuário educadamente que não sabe
responder a pergunta e sugira o transbordo humano para o e-mail assistance@unopar.com

CHUNKS DE CONTEXTO: [
"""
    for i, chunk in enumerate(chunks, start=1):
        system_content += f"""
--- CHUNK {i} ---
{chunk["content"]}

"""
    system_content += "\n]"

    prompt = []

    for message in messages:
        prompt.append({
            "role": message["role"],
            "content": message["content"]
        })

    prompt.append(
        {
            "role": "system",
            "content": system_content.strip()
        }
    )

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
            "stream": False,
            "options": {
                "temperature": TEMPERATURE
            }
        }
    )
    response.raise_for_status()
    data = response.json()
    res = data["message"]["content"]

    criar_mensagem(chat_id, role="user", content=content)
    message_id = criar_mensagem(chat_id, role="assistant", content=res)

    return {
        "id": message_id,
        "content": res
    }


def send_to_llm_stream(content: str, chat_id: int):
    with requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": generate_default_prompt(content, chat_id),
            "stream": True,
            "options": {
                "temperature": TEMPERATURE
            }
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