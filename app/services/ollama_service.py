import json

import requests

from app.config.settings import SYSTEM_PROMPT,OLLAMA_URL, MODEL, TEMPERATURE, MAX_TOKENS, EMAIL_SUPORT
from app.services.chunk_service import buscar_chunks_semelhantes
from app.services.chat_service import listar_mensagens, criar_mensagem

# Parâmetros do pipeline de RAG
MAX_MESSAGES = 4
MAX_CHUNKS = 3
MAX_DISTANCE = 0.80
TIMEOUT = (5, 120)  # (conexão, leitura) em segundos

# Reaproveita a conexão HTTP entre as requisições
_session = requests.Session()

def _buscar_chunks(content: str) -> list[dict]:
    if not content:
        return []

    chunks = buscar_chunks_semelhantes(content, limit=MAX_CHUNKS)

    if MAX_DISTANCE is not None:
        chunks = [c for c in chunks if c["distance"] <= MAX_DISTANCE]

    return chunks


def _formatar_contexto(chunks: list[dict]) -> str:
    if not chunks:
        return "(nenhum chunk encontrado)"

    return "\n\n".join(
        f"--- CHUNK {i} ---\n{chunk['content']}"
        for i, chunk in enumerate(chunks, start=1)
    )


def generate_default_prompt(content: str, chat_id: int):
    historico = listar_mensagens(chat_id)[-MAX_MESSAGES:]
    chunks = _buscar_chunks(content)

    system_content = SYSTEM_PROMPT.format(
        email=EMAIL_SUPORT,
        contexto=_formatar_contexto(chunks)
    )

    # O system prompt vai primeiro, que é a posição esperada pelos modelos de chat
    prompt = [{"role": "system", "content": system_content}]

    prompt.extend(
        {"role": m["role"], "content": m["content"]}
        for m in historico
    )

    if content:
        prompt.append({"role": "user", "content": content})

    return (prompt, chunks)


def _montar_payload(prompt: list[dict], stream: bool) -> dict:
    return {
        "model": MODEL,
        "messages": prompt,
        "stream": stream,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": MAX_TOKENS
        }
    }


def _salvar_troca(chat_id: int, pergunta: str, resposta: str):
    criar_mensagem(chat_id, role="user", content=pergunta)
    return criar_mensagem(chat_id, role="assistant", content=resposta)


def send_to_llm(content: str, chat_id: int):
    (prompt, chunks) = generate_default_prompt(content, chat_id)
    # print("Prompt enviado à LLM: %s", prompt)

    response = _session.post(
        OLLAMA_URL,
        json=_montar_payload(prompt, stream=False),
        timeout=TIMEOUT
    )
    response.raise_for_status()

    res = response.json()["message"]["content"]
    message_id = _salvar_troca(chat_id, content, res)

    return {
        "id": message_id,
        "content": res,
        "context": chunks
    }


def send_to_llm_stream(content: str, chat_id: int):
    (prompt, _) = generate_default_prompt(content, chat_id)
    # print("Prompt enviado à LLM: %s", prompt)

    with _session.post(
        OLLAMA_URL,
        json=_montar_payload(prompt, stream=True),
        stream=True,
        timeout=TIMEOUT
    ) as response:
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line)

            if "error" in data:
                raise RuntimeError(data["error"])

            token = data.get("message", {}).get("content", "")
            if token:
                yield token

            if data.get("done"):
                break


def stream_and_save(content: str, chat_id: int):
    resposta_completa = []
    try:
        for token in send_to_llm_stream(content, chat_id):
            resposta_completa.append(token)
            yield token
    finally:
        texto = "".join(resposta_completa)
        if texto:
            _salvar_troca(chat_id, content, texto)