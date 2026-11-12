sentences = [
    "How do I reset my password?",
    "The meeting starts at nine.",
    "Please send me the report.",
    "Where is the nearest station?",
    "The server restarted overnight.",
    "Could you share the slides?",
    "Our team won the prize.",
    "Close the door, please.",
]

numbered = "\n".join(f"{i}. {s}" for i, s in enumerate(sentences, 1))
prompt = (
    "Label each sentence as exactly one of: question, statement, request.\n"
    "Answer with one label per line, in order, and nothing else.\n\n" + numbered
)

response = client.messages.create(
    model=MODEL,
    max_tokens=100,
    thinking={"type": "disabled"},
    messages=[{"role": "user", "content": prompt}],
)
text = "".join(b.text for b in response.content if b.type == "text")
labels = [line.strip().lower() for line in text.splitlines() if line.strip()]

for s, label in zip(sentences, labels):
    print(f"{label:10} {s}")
print("tokens used:", response.usage.input_tokens, "in,", response.usage.output_tokens, "out")
