"""Open a live stream, read 3 events, then close the connection."""
import urllib.request

with urllib.request.urlopen("http://127.0.0.1:8041/demo?live=1", timeout=30) as response:
    events = 0
    for raw in response:
        if raw.startswith(b"data:"):
            events += 1
            if events == 3:
                break
print("left after 3 events")
