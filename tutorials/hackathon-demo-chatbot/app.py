import json
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Literal

import anthropic
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from spend_log import log_usage

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 300
SYSTEM = "You are the helper bot in a hackathon demo. Answer in at most three short sentences."
PAGE = Path(__file__).with_name("index.html")

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

client = anthropic.Anthropic()
app = FastAPI()


class Turn(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    history: list[Turn] = Field(default=[], max_length=20)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/chat")
def chat(req: ChatRequest):
    messages = [turn.model_dump() for turn in req.history]
    messages.append({"role": "user", "content": req.message})
    try:
        response = client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM, messages=messages)
    except anthropic.APIError:
        # Do not pass the provider's error text to the browser.
        raise HTTPException(status_code=502, detail="The model call failed. Check the server log.")
    log_usage("app.py", response)
    return {"reply": "".join(block.text for block in response.content if block.type == "text")}


@lru_cache
def demo_reply(question: str) -> str:
    return chat(ChatRequest(message=question))["reply"]


@app.get("/", response_class=HTMLResponse)
def index(ask: str = Query("", max_length=500)):
    # /?ask=... opens the page with one finished exchange, so a screenshot tool
    # can capture a conversation. Normal use is the form on the page.
    start = [{"role": "user", "content": ask}, {"role": "assistant", "content": demo_reply(ask)}] if ask else []
    return PAGE.read_text().replace("__START__", json.dumps(start).replace("<", "\\u003c"))
