# Keep a demo working when the API rate limit hits (TT-005)

A retry wrapper with exponential backoff and jitter, a saved-answer fallback, and a local stand-in server that reproduces 429 and 529 errors without calling the API.

| File | What it is |
|---|---|
| `prompt.py` | Model name, token cap and the prompt |
| `one_call.py` | One real API call; saves the reply to `saved_answer.json` |
| `show_sdk_retry.py` | Prints the SDK's retry rules from the installed package |
| `standin.py` | Local stand-in server: errors for the first N calls, then a reply. A test tool, not the API |
| `reproduce.py` | Shows how 429 and 529 arrive as SDK exceptions |
| `resilient.py` | The wrapper: `ask()` and `backoff_delay()` |
| `demo_wrapper.py` | Runs the wrapper against the stand-in and logs each retry |
| `layers.py` | Shows what two retry layers do to the call count |
| `test_resilient.py` | Unit tests (standard library `unittest`) |
| `spend_log.py` | Budget helper: one line per real API call in `spend.log` |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (venv active, packages installed, key exported from `.env`):

    python one_call.py
    python reproduce.py
    python demo_wrapper.py
    python -m unittest -v test_resilient
