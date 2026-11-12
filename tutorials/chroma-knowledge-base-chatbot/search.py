"""Print the chunks closest to a question. No model call, no key needed."""
import sys
import textwrap

from kb import COLLECTION, get_client


def retrieve(question, k=4):
    """Return a list of (source, distance, text) for the k closest chunks."""
    collection = get_client().get_collection(COLLECTION)
    result = collection.query(query_texts=[question], n_results=k)
    return [
        (meta["source"], dist, doc)
        for meta, dist, doc in zip(result["metadatas"][0], result["distances"][0], result["documents"][0])
    ]


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: python search.py "your question"')
    question = sys.argv[1]
    print(f"Question: {question}\n")
    for rank, (source, dist, text) in enumerate(retrieve(question), start=1):
        first_line = textwrap.shorten(text.split("\n\n", 1)[1], width=100, placeholder="...")
        print(f"{rank}. {source}  distance {dist:.3f}")
        print(f"   {first_line}")


if __name__ == "__main__":
    main()
