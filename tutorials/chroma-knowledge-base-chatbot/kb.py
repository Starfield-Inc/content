"""Shared pieces: where the notes live, the Chroma collection, the chunker."""
from pathlib import Path

import chromadb

HERE = Path(__file__).parent
NOTES_DIR = HERE / "notes"
DB_DIR = HERE / "chroma_db"
COLLECTION = "team_notes"
MAX_CHARS = 400


def chunk_note(text, max_chars=MAX_CHARS):
    """Split a note on blank lines, then pack whole paragraphs up to max_chars.

    The first line of a note is its heading. It is added to every chunk so a chunk
    still says what it is about when it is read on its own.
    """
    heading, _, body = text.partition("\n")
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    chunks, current = [], ""
    for p in paragraphs:
        if current and len(current) + len(p) + 2 > max_chars:
            chunks.append(current)
            current = p
        else:
            current = f"{current}\n\n{p}" if current else p
    if current:
        chunks.append(current)
    return [f"{heading.strip()}\n\n{c}" for c in chunks]


def get_client():
    return chromadb.PersistentClient(path=str(DB_DIR))
