from fastapi import FastAPI

from .contracts import Request
from .conversation_chain import ConversationRAG

conversation_rag = ConversationRAG()

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.post("/inca_tabagism")
async def ask_inca(request: Request):
    response = await conversation_rag.chat(request)
    return response
