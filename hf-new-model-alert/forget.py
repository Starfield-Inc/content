"""Remove the newest entry from seen.json, to pretend that model has just appeared."""
import json

with open("seen.json") as f:
    seen = json.load(f)
newest = max(seen, key=seen.get)
del seen[newest]
with open("seen.json", "w") as f:
    json.dump(seen, f, indent=2, sort_keys=True)
print(f"Forgot {newest}")
