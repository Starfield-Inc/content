"""A local stand-in for the API, for tests. It is not the real API.

It answers POST /v1/messages with an error for the opening `fail` calls, then with a
valid reply. It records when each call arrived. Real limits depend on your account.
"""
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ERROR_TYPES = {429: "rate_limit_error", 529: "overloaded_error", 500: "api_error", 401: "authentication_error"}

OK_BODY = {
    "id": "msg_standin", "type": "message", "role": "assistant", "model": "claude-haiku-5-5",
    "content": [{"type": "text", "text": "This reply came from the local stand-in server, not the API."}],
    "stop_reason": "end_turn", "stop_sequence": None,
    "usage": {"input_tokens": 10, "output_tokens": 12},
}


class StandIn:
    """Use as a context manager. `calls` holds the arrival time of each request."""

    def __init__(self, fail=2, status=429, retry_after=1):
        self.fail, self.status, self.retry_after = fail, status, retry_after
        self.calls = []
        stand_in = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                self.rfile.read(int(self.headers.get("content-length", 0)))
                stand_in.calls.append(time.monotonic())
                if len(stand_in.calls) <= stand_in.fail:
                    body = {"type": "error", "request_id": "req_standin",
                            "error": {"type": ERROR_TYPES[stand_in.status], "message": "Stand-in error for testing."}}
                    self.send_response(stand_in.status)
                    if stand_in.retry_after is not None:
                        self.send_header("retry-after", str(stand_in.retry_after))
                else:
                    body = OK_BODY
                    self.send_response(200)
                data = json.dumps(body).encode()
                self.send_header("content-type", "application/json")
                self.send_header("content-length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def __enter__(self):
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *exc):
        self.server.shutdown()
        self.server.server_close()

    def gaps(self):
        """Seconds between each call and the one before it."""
        return [round(b - a, 2) for a, b in zip(self.calls, self.calls[1:])]
