"""Print the fields the API gives for one model, so you can see what a filter has to work with."""
import json

from hfapi import newest_models

models, _ = newest_models("unsloth", limit=40)
model = next(m for m in models if any(t.startswith("base_model:") for t in m["tags"]))
model["tags"] = [t for t in model["tags"] if t.startswith(("base_model", "license", "gguf", "region"))]
print(json.dumps(model, indent=2))
