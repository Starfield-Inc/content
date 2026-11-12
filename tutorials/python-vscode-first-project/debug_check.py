"""Drive debugpy, the debugger VS Code uses, from a script.

Sets one breakpoint on the line `client = Anthropic()` in hello_haiku.py, runs the
program until it stops there, prints the local variables, then ends the program
before the API call. This is the same sequence of requests VS Code sends when you
press F5 with a breakpoint set.
"""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = (Path(__file__).parent / "hello_haiku.py").resolve()
LINE = next(i for i, t in enumerate(SCRIPT.read_text().splitlines(), 1) if "client = Anthropic()" in t)

adapter = subprocess.Popen([sys.executable, "-m", "debugpy.adapter"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
seq = 0


def send(command, arguments=None):
    global seq
    seq += 1
    body = json.dumps({"seq": seq, "type": "request", "command": command, "arguments": arguments or {}}).encode()
    adapter.stdin.write(b"Content-Length: %d\r\n\r\n" % len(body) + body)
    adapter.stdin.flush()
    return seq


def read():
    length = 0
    while True:
        line = adapter.stdout.readline().strip()
        if not line:
            break
        if line.lower().startswith(b"content-length:"):
            length = int(line.split(b":")[1])
    return json.loads(adapter.stdout.read(length))


def wait_for(match):
    while True:
        msg = read()
        if match(msg):
            return msg


def call(command, arguments=None):
    want = send(command, arguments)
    return wait_for(lambda m: m["type"] == "response" and m["request_seq"] == want)


call("initialize", {"adapterID": "debugpy", "linesStartAt1": True, "columnsStartAt1": True})
send("launch", {"program": str(SCRIPT), "args": ["debugging in VS Code"], "console": "internalConsole",
                "python": [sys.executable], "env": {"ANTHROPIC_API_KEY": "placeholder-not-used"}})
wait_for(lambda m: m.get("event") == "initialized")
resp = call("setBreakpoints", {"source": {"path": str(SCRIPT)}, "breakpoints": [{"line": LINE}]})
print(f"Breakpoint set on line {LINE} of hello_haiku.py, verified={resp['body']['breakpoints'][0]['verified']}")
call("configurationDone")
stopped = wait_for(lambda m: m.get("event") == "stopped")
print(f"Stopped: reason={stopped['body']['reason']}")
thread = stopped["body"]["threadId"]
frame = call("stackTrace", {"threadId": thread})["body"]["stackFrames"][0]
print(f"Paused in {frame['name']}() at line {frame['line']}")
scopes = call("scopes", {"frameId": frame["id"]})["body"]["scopes"]
local = next(s for s in scopes if s["name"] == "Locals")
for var in call("variables", {"variablesReference": local["variablesReference"]})["body"]["variables"]:
    if var["name"] in ("topic", "prompt"):
        print(f"  {var['name']} = {var['value']}")
call("disconnect", {"terminateDebuggee": True})
adapter.terminate()  # the adapter waits for a new session, so stop it ourselves
adapter.wait(timeout=10)
print("Program ended at the breakpoint. No API call was made.")
