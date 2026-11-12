"""Run only the moderation pass on the fixed drafts."""
import os
import sys

from assistant import make_client, moderate
from drafts import BAD, GOOD, INJECTION

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

client = make_client()
for name, text in (("good", GOOD), ("bad", BAD)):
    allowed, reason = moderate(client, text)
    print(f"{name:5} allowed={allowed}  reason: {reason}")
