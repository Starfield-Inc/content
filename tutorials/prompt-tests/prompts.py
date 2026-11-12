"""Five prompts. Each one has a matching test in test_prompts.py."""

PROMPTS = {
    "capital": "What is the capital of Australia? Answer in one word.",
    "json": "Give the chemical symbol and atomic number of gold as a JSON object with the keys "
            "symbol and number. Return only the JSON, with no code fence and no other text.",
    "list": "Name the three primary colours of light, one per line, with no numbers or bullets.",
    "summary": "Summarise this in one sentence of fewer than 20 words: Photosynthesis is the process "
               "plants use to turn sunlight, water and carbon dioxide into sugar and oxygen.",
    "minutes": "How many minutes are in 3 hours? Answer with the number only.",
}
