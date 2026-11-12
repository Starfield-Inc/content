import asyncio
import json
import os
from pathlib import Path

import anthropic
from fastapi import FastAPI, Header, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from prompt import MAX_TOKENS, MODEL, PROMPT
from spend_log import log_usage

MAX_LIVE_CALLS = 5  # per server process: a cap on what a stray visitor can spend
HERE = Path(__file__).parent

app = FastAPI()
live_calls = 0


def sse(data, event=None, event_id=None):
    """Format one server-sent event. The data is JSON so spaces and newlines survive."""
    lines = []
    if event_id == 0:
        lines.append("retry: 300")  # ask the browser to reconnect after 300 ms, not its default
    if event_id is not None:
        lines.append(f"id: {event_id}")
    if event:
        lines.append(f"event: {event}")
    lines.append(f"data: {json.dumps(data)}")
    return "\n".join(lines) + "\n\n"


def load_cache():
    return json.loads((HERE / "cache.json").read_text())


async def replay(start, speed, drop_after):
    """Send the saved chunks with their recorded gaps. No API call."""
    cache = load_cache()
    chunks = cache["chunks"]
    previous = chunks[start - 1]["t"] if start else 0.0
    for i in range(start, len(chunks)):
        if drop_after is not None and start == 0 and i >= drop_after:
            return  # end the response early, with no done event
        await asyncio.sleep(max(0.0, chunks[i]["t"] - previous) * speed)
        previous = chunks[i]["t"]
        yield sse(chunks[i]["text"], event_id=i)
    yield sse({"chunks": len(chunks)}, event="done")


async def live():
    """Stream a fixed-prompt answer from the API. One call per request."""
    client = anthropic.AsyncAnthropic()
    sent = 0
    try:
        async with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            thinking={"type": "disabled"},
            messages=[{"role": "user", "content": PROMPT}],
        ) as stream:
            async for text in stream.text_stream:
                yield sse(text, event_id=sent)
                sent += 1
            log_usage("app.py", await stream.get_final_message())
        yield sse({"chunks": sent}, event="done")
    except asyncio.CancelledError:
        # The browser went away. Leaving the "async with" block closes the upstream stream.
        print(f"client left after {sent} events, upstream stream closed", flush=True)
        raise
    except anthropic.APIError:
        yield sse({"message": "The model call failed."}, event="problem")


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/demo")
async def demo(
    live_answer: bool = Query(False, alias="live"),
    speed: float = Query(1.0, ge=0, le=5),
    drop_after: int | None = Query(None, ge=0),
    last_event_id: str | None = Header(None),
):
    global live_calls
    headers = {"Cache-Control": "no-store", "X-Accel-Buffering": "no"}
    if not live_answer:
        start = int(last_event_id) + 1 if last_event_id is not None else 0
        return StreamingResponse(replay(start, speed, drop_after), media_type="text/event-stream", headers=headers)
    if last_event_id is not None:
        # A live answer cannot be resumed, and a new call would cost money. A 409 stops the browser retrying.
        return JSONResponse({"detail": "A live answer cannot be resumed. Run it again."}, status_code=409)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return JSONResponse({"detail": "ANTHROPIC_API_KEY is not set."}, status_code=503)
    if live_calls >= MAX_LIVE_CALLS:
        return JSONResponse({"detail": "Live call limit reached for this server."}, status_code=429)
    live_calls += 1
    return StreamingResponse(live(), media_type="text/event-stream", headers=headers)


@app.get("/", response_class=HTMLResponse)
def index():
    return (HERE / "index.html").read_text()
