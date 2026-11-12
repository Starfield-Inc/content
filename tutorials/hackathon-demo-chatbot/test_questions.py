import json
import sys
import textwrap
import time
import urllib.request

BASE = "http://127.0.0.1:8031"
QUESTIONS = [
    "What is a REST API? Keep it to one sentence.",
    "Suggest a name for a chatbot about recycling.",
    "Name one thing that can go wrong in a live demo.",
    "How do I say good morning in Spanish?",
    "What is a vector database, in one sentence?",
]


def wait_for_server(seconds=30):
    end = time.time() + seconds
    while time.time() < end:
        try:
            urllib.request.urlopen(BASE + "/health", timeout=2).read()
            return
        except OSError:
            time.sleep(0.5)
    sys.exit("The server did not answer on " + BASE)


def ask(question):
    body = json.dumps({"message": question}).encode()
    request = urllib.request.Request(BASE + "/chat", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=60) as res:
        return json.loads(res.read())["reply"]


wait_for_server()
answered = 0
for number, question in enumerate(QUESTIONS, 1):
    reply = ask(question)
    print(f"{number}. Q: {question}")
    print(textwrap.fill(reply, width=100, initial_indent="   A: ", subsequent_indent="      "))
    if reply.strip():
        answered += 1
print(f"{answered} of {len(QUESTIONS)} questions answered")
sys.exit(0 if answered == len(QUESTIONS) else 1)
