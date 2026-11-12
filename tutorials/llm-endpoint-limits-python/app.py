import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from anthropic import Anthropic
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from limits import DailyCap, RateLimiter, cost_usd

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

MODEL = os.environ.get("TUTORIAL_MODEL", "claude-haiku-5-5")
MAX_TOKENS = 80
# Very small on purpose, so the tutorial can reach the cap with a few real calls.
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "5"))        # requests per user per window
RATE_WINDOW = int(os.environ.get("RATE_WINDOW", "60"))     # seconds
DAILY_CAP_USD = float(os.environ.get("DAILY_CAP_USD", "0.001"))
BLOCKED_LOG = Path(os.environ.get("BLOCKED_LOG", Path(__file__).with_name("blocked.log")))

app = FastAPI()
client = Anthropic()
limiter = RateLimiter(RATE_LIMIT, RATE_WINDOW)
cap = DailyCap(DAILY_CAP_USD)


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=500)


def block(user, reason, status, headers=None):
    """Log the blocked call, then answer with the status code the client should see."""
    line = {"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "user": user, "reason": reason}
    with open(BLOCKED_LOG, "a") as f:
        f.write(json.dumps(line) + "\n")
    return JSONResponse({"error": reason}, status_code=status, headers=headers)


@app.post("/ask")
def ask(body: Question, request: Request, x_user: str | None = Header(default=None)):
    user = x_user or request.client.host
    wait = limiter.allow(user)
    if wait:
        return block(user, "rate limit", 429, {"Retry-After": str(wait)})
    if not cap.is_open():
        return block(user, "daily cost cap reached", 429)

    response = client.messages.create(
        model=MODEL, max_tokens=MAX_TOKENS, thinking={"type": "disabled"},
        system="Answer in one short sentence.",
        messages=[{"role": "user", "content": body.question}],
    )
    spent = cap.add(cost_usd(response.usage.input_tokens, response.usage.output_tokens))
    answer = "".join(b.text for b in response.content if b.type == "text") or "(empty reply)"
    return {"answer": answer, "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens, "spent_today_usd": f"{spent:.6f}"}


@app.get("/usage")
def usage():
    return {"day": str(cap.day), "calls": cap.calls, "spent_usd": f"{cap.spent:.6f}",
            "cap_usd": f"{cap.cap_usd:.6f}", "rate_limit": f"{RATE_LIMIT} per {RATE_WINDOW}s per user"}
