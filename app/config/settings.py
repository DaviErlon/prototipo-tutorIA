import os
from pathlib import Path
from urllib.parse import quote_plus

ROOT_DIR = Path(__file__).resolve().parents[2]

def _obrigatoria(nome: str) -> str:
    valor = os.getenv(nome)
    if not valor:
        raise RuntimeError(f"Variável de ambiente obrigatória ausente: {nome}")
    return valor

def _caminho(nome: str, padrao: str) -> Path:
    return (ROOT_DIR / os.getenv(nome, padrao)).resolve()

def _ler_prompt() -> str:
    caminho = _caminho("SYSTEM_PROMPT_PATH", "system_prompt")
    if not caminho.exists():
        raise RuntimeError(f"Arquivo de system prompt não encontrado: {caminho}")
    return caminho.read_text(encoding="utf-8")

def _montar_database_url() -> str:
    user = quote_plus(_obrigatoria("POSTGRES_USER"))
    senha = quote_plus(_obrigatoria("POSTGRES_PASSWORD"))
    banco = _obrigatoria("POSTGRES_DB")
    socket = _obrigatoria("POSTGRES_SOCKET")

    return f"postgresql://{user}:{senha}@{socket}/{banco}"


# ENVs obrigatorias
OLLAMA_HOST = _obrigatoria("OLLAMA_HOST")
EMAIL_SUPORT = _obrigatoria("EMAIL_SUPORT")
DATABASE_URL = _montar_database_url()
SYSTEM_PROMPT = _ler_prompt()

# LLM
MODEL = "qwen3.5:2b"
TEMPERATURE = 0.7
MAX_TOKENS = 2000

# (PDFs -> CSV) PARAMETROS DE CHUNKINGS 
# CHUNK_SIZE = 1500
# OVERLAP = 150
# MIN_CHUNK = 120

# (PDFs -> CSV -> BD) DIRETORIOS
# PDF_DIR = _caminho("PDF_DIR", "documents")
CSV_PATH = _caminho("CSV_PATH", "chunkings/chunks.csv")
CSV_COLUNAS = ["doc", "pagina", "tipo", "texto"]
