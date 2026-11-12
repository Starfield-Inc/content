"""Answer a question from the notes only, with file-name citations."""
import os
import sys

from anthropic import Anthropic

from search import retrieve

MODEL = "claude-haiku-5-5"
NOT_FOUND = "not in the notes"

INSTRUCTIONS = f"""You answer questions about a hackathon team using only the note excerpts below.
Rules:
- Use only facts that appear in the excerpts. Do not use outside knowledge.
- After each fact, cite the file it came from in square brackets, for example [risks.md].
- If the excerpts do not contain the answer, reply with exactly: {NOT_FOUND}
- Keep the answer to three sentences or fewer."""


def build_prompt(question, chunks):
    blocks = [f'<note file="{source}">\n{text}\n</note>' for source, _, text in chunks]
    return f"{INSTRUCTIONS}\n\n" + "\n\n".join(blocks) + f"\n\nQuestion: {question}"


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: python ask.py "your question"')
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Load your .env file first.")

    question = sys.argv[1]
    chunks = retrieve(question, k=4)
    print(f"Question: {question}")
    print("Chunks sent: " + ", ".join(f"{s} ({d:.2f})" for s, d, _ in chunks) + "\n")

    response = Anthropic().messages.create(
        model=MODEL,
        max_tokens=300,
        thinking={"type": "disabled"},
        messages=[{"role": "user", "content": build_prompt(question, chunks)}],
    )
    answer = "".join(b.text for b in response.content if b.type == "text").strip()
    if not answer:
        sys.exit(f"The model returned no text (stop reason: {response.stop_reason}).")
    print("Answer:")
    print(answer)
    print(f"\n[tokens used: {response.usage.input_tokens} in, {response.usage.output_tokens} out]")


if __name__ == "__main__":
    main()
