import sys

import tiktoken

text = " ".join(sys.argv[1:]) or "Tokens are not the same as words."
encoding = tiktoken.get_encoding("cl100k_base")

ids = encoding.encode(text)
print(f"Text:   {text}")
print(f"Words:  {len(text.split())}")
print(f"Tokens: {len(ids)}")
print()
for token_id in ids:
    piece = encoding.decode([token_id])
    print(f"{token_id:>7}  {piece!r}")
