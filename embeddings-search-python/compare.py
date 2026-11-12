"""Embed one question and compare it with three sentences, one at a time."""
from common import cosine, embed, load_model, load_sentences

question = "Where can I get a boat to the island?"
sentences = load_sentences()
picks = [0, 5, 8]  # a close match, an unrelated cat sentence, an unrelated Python sentence

model = load_model()
q_vec = embed(model, [question])[0]
print(f"Question: {question}")
print(f"Question vector: {q_vec.shape[0]} numbers")
for i in picks:
    s_vec = embed(model, [sentences[i]])[0]
    print(f"cosine = {cosine(q_vec, s_vec):.3f}  {sentences[i]}")
print(f"cosine = {cosine(q_vec, q_vec):.3f}  (the question against itself)")
