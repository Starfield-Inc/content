# Test an MCP server with a client

A small MCP server with three safe tools, and a test client that starts it, lists its tools, calls each one, tries bad input, and prints a pass or fail checklist.

| File | What it does |
| --- | --- |
| `server.py` | The server: `word_count`, `convert_units`, `slugify`, over stdio |
| `test_client.py` | Starts a server file, runs 12 checks, exits 1 if any fail |
| `server_extra.py` | The same server with one unplanned tool, to show a failing check |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python test_client.py
python test_client.py server_extra.py
```

No API key and no network are needed after the install.
