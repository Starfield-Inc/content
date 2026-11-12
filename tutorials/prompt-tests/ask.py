"""Send one of the prompts and print the answer: python ask.py capital"""
import sys

from llm import ask
from prompts import PROMPTS

name = sys.argv[1]
print(f"Prompt: {PROMPTS[name]}")
print(f"Answer: {ask(PROMPTS[name])}")
