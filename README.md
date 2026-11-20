instalar as dependencias:
    pip install -r requirements.txt

extensoes postgres:
    - pg vector
    - pg search

executar com:
    uvicorn app.cmd.main:app --reload

extrair chunks de pdfs em documents/ para chunking/chunks.csv :
python -m app.cmd.ingest_pdf

vetorizar e lançar os chunking/chunks.csv para o postgres:
python -m app.cmd.csv_to_bd

tarefas: consulta hibrida =O