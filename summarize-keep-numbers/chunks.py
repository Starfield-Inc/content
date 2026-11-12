import sys
from pathlib import Path


def split_text(text, max_chars):
    """Split on blank lines, then pack whole paragraphs into chunks of up to max_chars.

    A paragraph longer than max_chars becomes its own chunk. It is not cut in the
    middle, because a cut can separate a number from the words that explain it.
    """
    chunks, current = [], ""
    for paragraph in (p.strip() for p in text.split("\n\n")):
        if not paragraph:
            continue
        if current and len(current) + 2 + len(paragraph) > max_chars:
            chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        chunks.append(current)
    return chunks


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python chunks.py FILE [MAX_CHARS]")
    if not Path(sys.argv[1]).is_file():
        sys.exit(f"Cannot find {sys.argv[1]}")
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    max_chars = int(sys.argv[2]) if len(sys.argv) > 2 else 900
    parts = split_text(text, max_chars)
    print(f"{len(text)} characters, {len(parts)} chunks (max {max_chars} characters)")
    for number, part in enumerate(parts, 1):
        print(f"chunk {number}: {len(part)} characters, starts: {part[:48]!r}")
