# Call an LLM from JavaScript and show the answer on a web page (TT-011)

A Node server that holds the API key, one endpoint (`POST /api/ask`), and a page with a text box that shows the model's answer. No npm packages.

| File | What it is |
|---|---|
| `call.js` | One call to the model from Node, to see the request and the reply |
| `server.js` | The small server: serves the page, keeps the key, exposes `/api/ask`, handles errors |
| `index.html`, `app.js` | The page and its browser code (no key in either) |
| `check-leak.js` | Fetches what a browser receives and checks the key is not in it |
| `test-errors.js` | Sends bad requests and prints the replies |
| `.env.example` | The name of the variable to set |
| `steps.json` | The steps the runner replays (web steps use port 8111) |
| `article.src.md`, `article.md` | The tutorial |

Needs Node 20.6 or newer. Put your key in `.env` (copy `.env.example`), then:

    node --env-file=.env call.js
    node --env-file=.env server.js      # then open http://127.0.0.1:8111/
    node --env-file=.env check-leak.js  # in a second terminal, with the server running
    node test-errors.js                 # in a second terminal, with the server running
