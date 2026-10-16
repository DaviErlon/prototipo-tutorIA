# inicializar todo mundo e rodar a API
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.chat_route import chat_router
from app.routes.chunk_route import chunk_router

app = FastAPI(
#    docs_url=None,
#    redoc_url=None,
#    openapi_url=None
)

app.include_router(chat_router)
app.include_router(chunk_router)

app.mount(
    "/",
    StaticFiles(directory="front", html=True),
    name="frontend"
)

