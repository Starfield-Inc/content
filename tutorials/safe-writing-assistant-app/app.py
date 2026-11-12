import os
import sys
import time

from flask import Flask, jsonify, render_template, request

from assistant import make_client, moderate, suggest
from safety import MAX_DRAFT_CHARS, Rejected, check_length

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

app = Flask(__name__)
client = make_client()


@app.get("/")
def index():
    return render_template("index.html", limit=MAX_DRAFT_CHARS)


@app.get("/hold.js")
def hold():
    # Only for the screenshot run: keeps the page "loading" so a capture sees the result.
    time.sleep(8)
    return "", 200, {"content-type": "text/javascript"}


@app.post("/api/suggest")
def api_suggest():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify(error='Send JSON like {"draft": "..."}.'), 400
    try:
        draft = check_length(body.get("draft"))
        allowed, reason = moderate(client, draft)
        if not allowed:
            return jsonify(blocked=True, error=f"Not sent for suggestions. {reason}"), 422
        text, usage = suggest(client, draft)
    except Rejected as err:
        return jsonify(error=str(err)), err.status
    except Exception as err:  # the detail stays in the server log
        print("request failed:", type(err).__name__, err, file=sys.stderr)
        return jsonify(error="The writing service had a problem. Try again later."), 502
    return jsonify(suggestions=text, usage={"input": usage.input_tokens, "output": usage.output_tokens})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 8125)))
