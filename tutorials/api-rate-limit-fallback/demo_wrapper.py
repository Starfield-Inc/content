"""Run the wrapper against the stand-in: one case that recovers, one that falls back."""
import json
import logging
import sys

from anthropic import Anthropic

from resilient import ask
from standin import StandIn

logging.basicConfig(level=logging.WARNING, format="%(message)s",
                    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("retries.log", mode="w")])

saved = json.load(open("saved_answer.json"))


def client_for(stand_in):
    return Anthropic(base_url=stand_in.base_url, api_key="stand-in-key", max_retries=0)


print("Case 1: the stand-in returns 429 twice, then a reply.")
with StandIn(fail=2, status=429, retry_after=1) as stand_in:
    answer = ask(client_for(stand_in), saved["prompt"], saved["text"], base=0.5)
    print(f"source: {answer.source}, attempts: {answer.attempts}, calls: {len(stand_in.calls)}, gaps: {stand_in.gaps()}")
    print("text:", answer.text)

print()
print("Case 2: the stand-in returns 529 every time. No retry-after header.")
with StandIn(fail=99, status=529, retry_after=None) as stand_in:
    answer = ask(client_for(stand_in), saved["prompt"], saved["text"], base=0.5)
    print(f"source: {answer.source}, attempts: {answer.attempts}, calls: {len(stand_in.calls)}, gaps: {stand_in.gaps()}")
    print("text:", answer.text)
