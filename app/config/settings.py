import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]

load_dotenv(ROOT_DIR / ".env")

def _obrigatoria(nome: str) -> str:
    valor = os.getenv(nome)
    if not valor:
        raise RuntimeError(f"Variável de ambiente obrigatória ausente: {nome}")
    return valor


def _caminho(nome: str, padrao: str) -> Path:
    return (ROOT_DIR / os.getenv(nome, padrao)).resolve()

# ENVs obrigatorias
OLLAMA_URL = _obrigatoria("OLLAMA_URL")
EMAIL_SUPORT = _obrigatoria("EMAIL_SUPORT")
DATABASE_URL = _obrigatoria("DATABASE_URL")

# LLM
MODEL = "qwen3:8b"
TEMPERATURE = 0.7
MAX_TOKENS = 2000

# (PDFs -> CSV) PARAMETROS DE CHUNKINGS 
CHUNK_SIZE = 1500
OVERLAP = 150
MIN_CHUNK = 120

# (PDFs -> CSV) DIRETORIOS
PDF_DIR = _caminho("PDF_DIR", "documents")
CSV_PATH = _caminho("CSV_PATH", "chunkings/chunks.csv")
CSV_COLUNAS = ["doc", "pagina", "tipo", "texto"]

SYSTEM_PROMPT_PATH = _caminho("SYSTEM_PROMPT_PATH", "system_prompt")
SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")