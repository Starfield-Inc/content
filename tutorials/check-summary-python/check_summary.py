import json
import os
import re
import sys

from anthropic import Anthropic

from spend_log import log_usage

MODEL = "claude-haiku-5-5"

EXTRACT_PROMPT = """List every factual claim in the summary below as a short, self-contained sentence.
One fact per claim. Keep numbers, names and dates exactly as written in the summary.
Do not add any number, name or date that the summary does not state in that sentence.
Reply with a JSON list of strings and nothing else.

Summary:
{summary}"""

FIND_PROMPT = """Here is a source text and one claim.
Find the one sentence in the source that supports the claim, and copy it exactly, word for word.
If no sentence in the source supports the claim, use null.
Reply with JSON only, in this form: {{"quote": "<exact sentence or null>", "supports": true or false}}
"supports" is true only if the quote states what the claim states.

Source:
{source}

Claim: {claim}"""


def ask(client, prompt, max_tokens=3000):
    """One call. Returns the text of the reply and logs the token use.

    The limit is generous because this model can spend tokens thinking before it writes.
    With a limit of 300 the reply came back empty."""
    response = client.messages.create(model=MODEL, max_tokens=max_tokens, messages=[{"role": "user", "content": prompt}])
    log_usage("check_summary.py", response)
    return "".join(block.text for block in response.content if block.type == "text")


def parse_json(text):
    """Return the last JSON value in the reply, or None.

    The model sometimes writes one answer, then "Wait, correcting:" and a second one, so the
    last value is the one to trust. strict=False allows a raw line break inside a string.
    """
    decoder = json.JSONDecoder(strict=False)
    last, pos = None, 0
    while True:
        match = re.compile(r"[\[{]").search(text, pos)
        if not match:
            return last
        try:
            last, pos = decoder.raw_decode(text, match.start())
        except json.JSONDecodeError:
            pos = match.start() + 1


def normalise(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def numbers_in(text):
    return {n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)}


def judge(claim, answer, source):
    """Turn the model's answer into found / not found, and say why.

    The model has to quote the source. The code then checks the quote really is in the
    source, and that every number in the claim is in the quote. Neither check needs a model.
    """
    quote = answer.get("quote")
    if not quote:
        return "NOT FOUND", "the model found no supporting sentence"
    if normalise(quote) not in normalise(source):
        return "NOT FOUND", "the quoted sentence is not in the source"
    missing = numbers_in(claim) - numbers_in(quote)
    if missing:
        return "NOT FOUND", "number not in the quote: " + ", ".join(sorted(missing))
    if not answer.get("supports"):
        return "NOT FOUND", "the model says the quote does not support the claim"
    return "found", ""


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python check_summary.py source.txt summary.txt")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")
    source = open(sys.argv[1], encoding="utf-8").read()
    summary = open(sys.argv[2], encoding="utf-8").read()
    client = Anthropic()

    claims = parse_json(ask(client, EXTRACT_PROMPT.format(summary=summary)))
    if not isinstance(claims, list):
        sys.exit("The model did not return a list of claims. Run it again.")
    print(f"Summary: {sys.argv[2]}   Claims listed: {len(claims)}")
    print()

    not_found = 0
    for number, claim in enumerate(claims, 1):
        reply = ask(client, FIND_PROMPT.format(source=source, claim=claim))
        try:
            answer = parse_json(reply)
        except json.JSONDecodeError:
            answer = None
        if not isinstance(answer, dict):
            status, reason = "NOT FOUND", f"the reply was not valid JSON: {reply[:60]!r}"
        else:
            status, reason = judge(claim, answer, source)
        print(f"{number}. [{status}] {claim}")
        if reason:
            print(f"     why: {reason}")
        if status != "found":
            not_found += 1

    print()
    print(f"Report: {len(claims) - not_found} found, {not_found} not found, out of {len(claims)} claims.")


main()
