"""
ingest.py
=========
Extração de texto de PDFs + chunking, gerando um CSV com as colunas
definidas em CSV_COLUNAS (doc, pagina, tipo, texto).

Uso:
    python ingest.py
"""

import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd
import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import (
    CHUNK_SIZE,
    CSV_COLUNAS,
    CSV_PATH,
    MIN_CHUNK,
    OVERLAP,
    PDF_DIR,
)

def limpar(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto)
    texto = re.sub(r"-\n(\w)", r"\1", texto)            # hifenização no fim de linha
    texto = re.sub(r"(?<!\n)\n(?!\n)", " ", texto)      # quebras simples -> espaço
    texto = re.sub(r"[ \t]+", " ", texto).strip()
    return re.sub(r"^\d(?:\s?\d)?\s+", "", texto)       # número de página no início


def criar_splitter(chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP,) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        keep_separator="end",
    )


def extrair_chunks_pdf(pdf_path, splitter: RecursiveCharacterTextSplitter | None = None,min_chunk: int = MIN_CHUNK,) -> list[dict]:
    pdf_path = Path(pdf_path).resolve()
    splitter = splitter or criar_splitter()
    linhas = []

    with pymupdf.open(pdf_path) as doc:
        for numero, pagina in enumerate(doc, start=1):
            texto = limpar(pagina.get_text("text"))

            for pedaco in splitter.split_text(texto):
                if len(pedaco) < min_chunk:
                    continue

                linhas.append({
                    "doc": pdf_path.name,
                    "pagina": numero,
                    "tipo": "texto",
                    "texto": pedaco,
                })

    return linhas


def extrair_chunks_pasta(pdf_dir=PDF_DIR, **kwargs) -> pd.DataFrame:
    pdf_dir = Path(pdf_dir).resolve()
    linhas = []

    for pdf in sorted(pdf_dir.glob("*.pdf")):
        print(f"Processando: {pdf.name}")
        linhas += extrair_chunks_pdf(pdf, **kwargs)

    return pd.DataFrame(linhas, columns=CSV_COLUNAS)


def gerar_csv(pdf_dir=PDF_DIR, csv_path=CSV_PATH, **kwargs) -> pd.DataFrame:
    csv_path = Path(csv_path).resolve()
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    df = extrair_chunks_pasta(pdf_dir, **kwargs)
    df.to_csv(csv_path, index=False, encoding="utf-8")

    print(f"{len(df)} chunks salvos em {csv_path}")
    return df


def main() -> int:
    try:
        gerar_csv()
    except Exception as erro:
        print(f"Erro ao gerar CSV: {erro}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())