
import csv
import sys
from pathlib import Path
from app.databases.chroma import get_collection

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = ROOT_DIR / "chunks.csv"
CHROMA_PATH = ROOT_DIR / "chroma_data"
COLLECTION_NAME = "chunks"


def importar_csv():
    collection = get_collection(COLLECTION_NAME)

    ids = []
    documents = []
    metadatas = []

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as arquivo:
        reader = csv.DictReader(arquivo)

        colunas = {"doc", "pagina", "tipo", "texto"}
        if not colunas.issubset(reader.fieldnames or []):
            raise ValueError(
                "O CSV deve possuir as colunas: doc, pagina, tipo, texto"
            )

        for numero, linha in enumerate(reader, start=1):
            texto = linha["texto"].strip()
            if not texto:
                continue

            ids.append(f"chunk_{numero}")
            documents.append(texto)
            metadatas.append({
                "doc": linha["doc"].strip(),
                "pagina": int(linha["pagina"]),
                "tipo": linha["tipo"].strip(),
            })

    if not documents:
        print("Nenhum texto válido encontrado no CSV.")
        return

    # Insere ou atualiza os registros que possuem os mesmos IDs.
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"{len(documents)} chunks importados para '{COLLECTION_NAME}'.")
    print(f"Total de registros na coleção: {collection.count()}")


if __name__ == "__main__":
    try:
        importar_csv()
    except Exception as erro:
        print(f"Erro ao importar CSV: {erro}", file=sys.stderr)
        sys.exit(1)