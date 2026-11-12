"""What happens when your wrapper retries on top of a client that also retries."""
import logging
import sys

from anthropic import Anthropic

from resilient import ask
from standin import StandIn

logging.basicConfig(level=logging.WARNING, format="  %(message)s", stream=sys.stdout)

for label, max_retries in (("max_retries=0 on the client", 0), ("default client, max_retries=2", 2)):
    print(label)
    with StandIn(fail=99, status=529, retry_after=None) as stand_in:
        client = Anthropic(base_url=stand_in.base_url, api_key="stand-in-key", max_retries=max_retries)
        answer = ask(client, "hello", "saved text", max_attempts=3, base=0.1)
        print(f"  wrapper attempts: {answer.attempts}, calls that reached the stand-in: {len(stand_in.calls)}")
