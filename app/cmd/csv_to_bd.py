"""
importar_csv.py
===============
Lê o CSV gerado pelo ingest.py (colunas em CSV_COLUNAS) e grava cada
linha como um Chunk no banco.

Uso:
    python importar_csv.py
"""

import csv
import sys
from pathlib import Path

from app.config.settings import CSV_COLUNAS, CSV_PATH
from app.schemas.models import Chunk
from app.services.chunk_service import criar_chunk


def linha_para_chunk(linha: dict) -> Chunk | None:
    texto = (linha["texto"] or "").strip()

    if not texto:
        return None

    return Chunk(
        content=texto,
        document=(linha["doc"] or "").strip(),
        page= int(linha["pagina"]),
    )


def importar_csv(csv_path=CSV_PATH) -> tuple[int, int]:
    csv_path = Path(csv_path).resolve()
    importados = 0
    ignorados = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as arquivo:
        reader = csv.DictReader(arquivo)

        if not set(CSV_COLUNAS).issubset(reader.fieldnames or []):
            raise ValueError(
                f"O CSV deve possuir as colunas: {', '.join(CSV_COLUNAS)}"
            )

        for numero, linha in enumerate(reader, start=2):
            try:
                chunk = linha_para_chunk(linha)

                if chunk is None:
                    ignorados += 1
                    continue

                criar_chunk(chunk)

            except Exception as erro:
                ignorados += 1
                print(f"Linha {numero} ignorada: {erro}", file=sys.stderr)
                continue

            importados += 1

            if importados % 50 == 0:
                print(f"{importados} chunks importados...")

    print(f"{importados} chunks importados, {ignorados} ignorados.")
    return importados, ignorados


def main() -> int:
    try:
        importar_csv()
    except Exception as erro:
        print(f"Erro ao importar CSV: {erro}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())