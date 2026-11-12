import argparse
import os
import sys
from pathlib import Path

MODEL = "claude-haiku-5-5"
BULLETS = {"short": 3, "medium": 5, "long": 8}
CHUNK_CHARS = 1500


def read_input(source):
    """Read a file, or pasted text from standard input when source is '-'."""
    if source == "-":
        return sys.stdin.read().strip()
    path = Path(source)
    if not path.is_file():
        sys.exit(f"Cannot find {source}")
    return path.read_text(encoding="utf-8").strip()


def split_text(text, max_chars):
    """Pack whole paragraphs into chunks of up to max_chars. A longer paragraph is cut at a space."""
    chunks, current = [], ""
    for paragraph in (p.strip() for p in text.split("\n\n") if p.strip()):
        while len(paragraph) > max_chars:
            cut = paragraph.rfind(" ", 0, max_chars)
            cut = cut if cut > 0 else max_chars
            if current:
                chunks.append(current)
                current = ""
            chunks.append(paragraph[:cut])
            paragraph = paragraph[cut:].strip()
        if current and len(current) + 2 + len(paragraph) > max_chars:
            chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        chunks.append(current)
    return chunks


def ask(client, prompt):
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        thinking={"type": "disabled"},  # with thinking on, max_tokens can run out before any text appears
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(block.text for block in response.content if block.type == "text").strip()
    if not text:
        sys.exit(f"The model returned no text (stop reason: {response.stop_reason}).")
    return text


def summarise(client, text, count):
    prompt = (
        "Summarise the text below.\n"
        "Line 1: a headline of at most 10 words, starting with 'HEADLINE: '.\n"
        f"Then exactly {count} bullet points, each starting with '- ' and holding one short sentence.\n"
        f"Use only facts from the text. Write nothing else.\n\n{text}"
    )
    return ask(client, prompt)


def main():
    parser = argparse.ArgumentParser(description="Summarise a text file or pasted text.")
    parser.add_argument("source", help="a text file, or - to read pasted text from standard input")
    parser.add_argument("--length", choices=BULLETS, default="medium", help="short=3, medium=5, long=8 bullets")
    parser.add_argument("--max-input", type=int, default=20000, help="refuse input longer than this many characters")
    parser.add_argument("--dry-run", action="store_true", help="show how the text would be split, send nothing")
    args = parser.parse_args()

    text = read_input(args.source)
    if not text:
        sys.exit("The input is empty.")
    if len(text) > args.max_input:
        sys.exit(f"Input is {len(text)} characters, over the limit of {args.max_input}. Nothing was sent.")
    parts = split_text(text, CHUNK_CHARS)
    if args.dry_run:
        print(f"{len(text)} characters, {len(parts)} part(s) of up to {CHUNK_CHARS} characters. Nothing was sent.")
        return
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

    from anthropic import Anthropic

    client = Anthropic()
    count = BULLETS[args.length]
    calls = 1
    if len(parts) > 1:
        notes = []
        for number, part in enumerate(parts, 1):
            notes.append(ask(client, f"List the 3 main facts in this part of a longer text, one line each.\n\n{part}"))
            print(f"part {number}/{len(parts)} done")
        text = "\n".join(notes)
        calls += len(parts)
        print()
    print(summarise(client, text, count))
    print(f"\n[{len(text)} characters sent to the final call, {len(parts)} part(s), {calls} model call(s)]")


if __name__ == "__main__":
    main()
