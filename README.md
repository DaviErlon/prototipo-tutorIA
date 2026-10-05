to usando o python 3.10.20
qualquer erro ja desconfia da versao kkkk

instalem o ollama, dps baixa o embed que o codigo ta usando:
    ollama pull nomic-embed-text

(se quiser confere se baixou memo com "ollama list")

instalar as dependencias:
    pip install -r requirements.txt

executar com:
    uvicorn app.main:app --reload

importar os cards de teste:
python -m app.import_cards

Coloquei esse troço aí pra importar os card belê

tarefas: desenvolver o front e inserir os cards, morô?