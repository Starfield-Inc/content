import json
import os
import re
import sys

from anthropic import Anthropic

from rulebook import load_rules, retrieve

MODEL = "claude-haiku-5-5"
DISCLAIMER = (
    "Disclaimer: this is a demo about a made-up rulebook. It is not legal advice "
    "and no lawyer has reviewed it."
)
REFUSAL = "I can only answer questions about the rules in the rulebook, and I cannot give legal advice."

SYSTEM = (
    "You answer questions about the court-style rules you are given. "
    "Use only those rules. Cite every rule you rely on as [Rule N], using its number exactly. "
    "Quote the key words of the rule in quotation marks. Answer in at most 60 words. "
    "If the question asks what a person should do, whether they will win, or for any "
    "advice, or if the rules do not answer it, reply with exactly REFUSE and nothing else."
)


def answer(client, question, rules):
    """Return (reply text, rule numbers sent to the model). Refuse without a call if nothing matches."""
    numbers = retrieve(question, rules)
    if not numbers:
        return REFUSAL, []
    context = "\n".join(f"Rule {n}. {rules[n]}" for n in numbers)
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        thinking={"type": "disabled"},
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Rules:\n{context}\n\nQuestion: {question}"}],
    )
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    if not text:
        sys.exit(f"The model returned no text (stop reason: {response.stop_reason}).")
    if text == "REFUSE":
        return REFUSAL, numbers
    return text, numbers


def main():
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        sys.exit('Usage: python ask.py "your question"')
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")
    rules = load_rules()
    reply, numbers = answer(Anthropic(), question, rules)
    final = f"{reply}\n\n{DISCLAIMER}"
    print(f"Question: {question}")
    print(f"Rules retrieved: {numbers or 'none'}\n")
    print(final)
    with open("answers.log", "a", encoding="utf-8") as log:
        log.write(json.dumps({"question": question, "answer": final}) + "\n")


if __name__ == "__main__":
    main()
