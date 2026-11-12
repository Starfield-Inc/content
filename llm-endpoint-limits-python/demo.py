"""Start the real server on port 8136, send real requests, print what a client sees.

Usage: python demo.py rate | cap | restart | logs
"""
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx

PORT = 8136
BASE = f"http://127.0.0.1:{PORT}"
LOG = Path(__file__).with_name("blocked.log")


def start(extra_env):
    env = {**os.environ, **extra_env}
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "app:app", "--port", str(PORT), "--log-level", "warning"], env=env)
    for _ in range(60):
        try:
            httpx.get(f"{BASE}/usage", timeout=1)
            return proc
        except httpx.HTTPError:
            time.sleep(0.5)
    proc.terminate()
    sys.exit("server did not start")


def ask(user, question):
    r = httpx.post(f"{BASE}/ask", json={"question": question}, headers={"X-User": user}, timeout=60)
    extra = f" Retry-After: {r.headers['Retry-After']}" if "Retry-After" in r.headers else ""
    print(f"[{user}] HTTP {r.status_code}{extra} {r.text}")
    return r


def usage():
    print("usage:", httpx.get(f"{BASE}/usage").text)


def main():
    mode = sys.argv[1]
    if mode == "logs":
        print(LOG.read_text() if LOG.exists() else "no blocked calls logged")
        return
    if mode == "rate":
        LOG.unlink(missing_ok=True)  # start the blocked-call log fresh
        server = start({"RATE_LIMIT": "2", "RATE_WINDOW": "60", "DAILY_CAP_USD": "1"})
    elif mode == "cap":
        server = start({"RATE_LIMIT": "100", "DAILY_CAP_USD": "0.0008"})
    elif mode == "restart":
        server = start({})
    else:
        sys.exit(__doc__)
    try:
        if mode == "rate":
            for q in ("What is a rate limit?", "Name one HTTP status code.", "Say hello."):
                ask("ana", q)
            ask("ben", "Say hello.")
            usage()
        elif mode == "cap":
            for i in range(10):
                if ask("ana", "In two sentences, what is a token in a language model?").status_code == 429:
                    break
            usage()
        else:
            ask("ana", "Name one colour.")
            usage()
            server.terminate()
            server.wait()
            server = start({})
            print("after restart:")
            usage()
    finally:
        server.terminate()
        server.wait()


main()
