from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple

from app.llm_loader import load_llm
from app.config import SYSTEM_PROMPT_DEVELOPER_VIETNAM,SYSTEM_PROMPT_BASIC
from app.context import ChatContext
from app.chat_engine import chat_once

app = FastAPI(title="Local LLM Chatbot API")

llm = load_llm()  # load when server start


# ===== Request / Response schema =====

class ChatRequest(BaseModel):
    message: str
    history: List[Tuple[str, str]] = []


class ChatResponse(BaseModel):
    reply: str


# ===== API =====

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    context = ChatContext(
        # system_prompt = SYSTEM_PROMPT_DEV
        system_prompt=SYSTEM_PROMPT_BASIC
    )

    # Load history from client
    for role, content in req.history:
        if role == "user":
            context.add_user(content)
        elif role == "assistant":
            context.add_assistant(content)

    # Chat
    reply = chat_once(llm, context, req.message)

    return ChatResponse(
        reply=reply
    )
