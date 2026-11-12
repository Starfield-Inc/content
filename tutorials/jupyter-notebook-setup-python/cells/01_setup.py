import os
from collections import Counter

import matplotlib.pyplot as plt
from anthropic import Anthropic

MODEL = "claude-haiku-5-5"

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise RuntimeError("Set ANTHROPIC_API_KEY before you run this notebook.")

client = Anthropic()
