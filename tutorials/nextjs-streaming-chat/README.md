# Streaming chat page in Next.js (TT-029)

A chat page that streams answers from the Anthropic API through a Next.js route handler, keeps the history, has a Stop button and shows clear error states. The API key stays on the server.

All package versions are pinned to exact versions in `package.json` (no `^`), and `package-lock.json` is kept. Versions change fast, so re-check them before you publish.

| File | What it is |
|---|---|
| `app/api/chat/route.js` | The route handler: checks the body, streams the answer, closes the API call when the browser leaves |
| `app/page.js` | The chat page: message list, Send and Stop buttons, error banner with Try again |
| `app/layout.js`, `app/globals.css` | Page shell and styles |
| `scripts/call-route.mjs` | Calls the route and prints when each piece arrives |
| `scripts/drive.mjs` | Drives the page in Chrome (puppeteer-core) and saves screenshots |
| `scripts/with-server.sh` | Starts the built app on port 8129, runs a command, stops it |
| `scripts/check-leak.mjs` | Looks for the key in the files the browser downloads |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (Node 20.9 or newer, Google Chrome for the browser steps; copy `.env.example` to `.env` and add your key):

    npm install
    npm run build
    set -a; source .env; set +a
    npm start            # then open http://localhost:8129
    # or, while editing: npm run dev

The screenshots `images/shot-*.png` are real Chrome screenshots written by `scripts/drive.mjs`.
