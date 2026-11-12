"""Show how a 429 and a 529 arrive, using the real SDK against the local stand-in."""
import anthropic
from anthropic import Anthropic

from prompt import MAX_TOKENS, MODEL, PROMPT
from standin import StandIn


def call(client):
    return client.messages.create(model=MODEL, max_tokens=MAX_TOKENS,
                                  messages=[{"role": "user", "content": PROMPT}])


def show(error):
    print(f"  class: {type(error).__name__}")
    print(f"  status_code: {error.status_code}")
    print(f"  error type in the body: {error.type}")
    print(f"  retry-after header: {error.response.headers.get('retry-after')}")


print("1. A 429 with retry-after 1. The client has max_retries=0, so nothing retries.")
with StandIn(fail=1, status=429, retry_after=1) as stand_in:
    client = Anthropic(base_url=stand_in.base_url, api_key="stand-in-key", max_retries=0)
    try:
        call(client)
    except anthropic.RateLimitError as error:
        show(error)
    print(f"  calls that reached the stand-in: {len(stand_in.calls)}")

print("2. A 529 with no retry-after header. Same client settings.")
with StandIn(fail=1, status=529, retry_after=None) as stand_in:
    client = Anthropic(base_url=stand_in.base_url, api_key="stand-in-key", max_retries=0)
    try:
        call(client)
    except anthropic.OverloadedError as error:
        show(error)
        print(f"  is it also an InternalServerError? {isinstance(error, anthropic.InternalServerError)}")

print("3. The default client (max_retries=2) against two 429s then a reply.")
with StandIn(fail=2, status=429, retry_after=1) as stand_in:
    client = Anthropic(base_url=stand_in.base_url, api_key="stand-in-key")
    response = call(client)
    print(f"  no exception. Reply: {response.content[0].text}")
    print(f"  calls that reached the stand-in: {len(stand_in.calls)}, gaps in seconds: {stand_in.gaps()}")

print("4. The default client against three 429s.")
with StandIn(fail=3, status=429, retry_after=1) as stand_in:
    client = Anthropic(base_url=stand_in.base_url, api_key="stand-in-key")
    try:
        call(client)
    except anthropic.RateLimitError as error:
        print(f"  raised {type(error).__name__} after {len(stand_in.calls)} calls, gaps in seconds: {stand_in.gaps()}")
