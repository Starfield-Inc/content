"""Read every .md file in notes/, split it into chunks, store the chunks in Chroma.

No embedding code here: Chroma embeds the text with its default local model.
The script rebuilds the collection each time, so running it twice gives the same result.
"""
import sys

from kb import COLLECTION, NOTES_DIR, chunk_note, get_client


def main():
    files = sorted(NOTES_DIR.glob("*.md"))
    if not files:
        sys.exit(f"No .md files found in {NOTES_DIR.name}/")

    client = get_client()
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass  # first run: nothing to delete
    collection = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})

    ids, documents, metadatas = [], [], []
    for path in files:
        for n, chunk in enumerate(chunk_note(path.read_text(encoding="utf-8")), start=1):
            ids.append(f"{path.name}#{n}")
            documents.append(chunk)
            metadatas.append({"source": path.name, "chunk": n})

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Read {len(files)} notes, stored {collection.count()} chunks in chroma_db/")



if __name__ == "__main__":
    main()
