import json
from pathlib import Path

import anthropic
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from compare import compare

PAGE = Path(__file__).with_name("index.html")
SAVED = Path(__file__).with_name("demo_result.json")

app = FastAPI()


class CompareRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=500)


@app.post("/compare")
def compare_route(req: CompareRequest):
    try:
        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY when a request arrives
        return {"results": compare(client, req.prompt)}
    except anthropic.APIError:
        # Do not pass the provider's error text to the browser.
        raise HTTPException(status_code=502, detail="A model call failed. Check the server log.")


@app.get("/", response_class=HTMLResponse)
def index(demo: int = Query(0)):
    # /?demo=1 shows the result saved by compare.py --save. It makes no model calls,
    # so a screenshot tool can open the page for free as often as it likes.
    start = json.loads(SAVED.read_text()) if demo and SAVED.exists() else None
    return PAGE.read_text().replace("__START__", json.dumps(start).replace("<", "\\u003c"))
