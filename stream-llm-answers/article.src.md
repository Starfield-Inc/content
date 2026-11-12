---
seo_title: Stream Answers So Your AI Hackathon Demo Feels Fast
meta_description: Make your AI hackathon demo feel fast: stream a model's answer to a web page word by word, and handle a dropped connection without breaking the demo.
---

# Add streaming so your hackathon demo feels fast

You build a small FastAPI server that streams a Claude answer to a web page piece by piece, a page that shows the text arriving, and a way to carry on when the connection drops.

**Time:** about two hours. **Level:** intermediate. **You need:** Python 3.10 or newer, a browser, an Anthropic API key, and the habit of running a small FastAPI app (the [demo chatbot tutorial](../hackathon-demo-chatbot/article.md) covers it). **Tested:** 10 November 2026 with Python 3.14.6, `anthropic` 2.7.0, `fastapi` 0.162.2 and `uvicorn` 0.54.0 on macOS.

Model replies and timings differ from run to run. Your numbers will not match the ones below.

Judges at an AI hackathon watch your demo for a few minutes, and an answer that appears word by word feels faster than one that arrives all at once. Streaming does not make the model finish sooner. It shows the reader something sooner, and Step 1 measures the gap. If you are still choosing an event, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A demo with a blank box and a spinner feels slow even when the model is not. A streamed answer starts to appear as soon as the model writes its opening words. The price is a second thing that can break on stage: a long-lived connection. This tutorial covers both the speed-up and the failure.

## See it running

This is the finished page. It replays a saved answer, so opening it costs nothing. The rest of the tutorial builds it from scratch.

{{shot:08-page|The streaming demo page with a finished answer about showing output as it is written, a status line with chunk counts, and two buttons}}

## Step 1: Stream one answer and time it

Start with the model call alone, before any web code. `client.messages.stream(...)` returns a stream, and `stream.text_stream` yields the text in pieces as the API sends them. The script notes when each piece arrived, saves them to `cache.json`, and prints the wait for the opening piece against the wait for the whole answer.

Settings sit in `prompt.py`. The prompt is fixed on purpose: the server never sends a visitor's text to the API, so a stranger cannot spend your credit. `thinking={"type": "disabled"}` turns off extended thinking so the stream is text only. The API docs list this setting as accepted by `claude-haiku-5-5`.

{{file:prompt.py}}

{{file:spend_log.py}}

{{file:timing.py}}

Create the environment and install the packages.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

{{file:requirements.txt}}

{{cmd:02-install}}

{{shot:02-install|Terminal listing the installed versions of anthropic, fastapi and uvicorn}}

Put your key in a file named `.env`. Copy the placeholder file and edit it:

{{file:.env.example}}

Never paste a real key into code, a screenshot or a chat. Load the file into your terminal session (macOS and Linux):

```bash
set -a; source .env; set +a
```

Without the key, the script stops with a message:

{{shot:03-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

Now run it. This makes one real API call.

{{cmd:04-timing}}

{{out:04-timing}}

{{shot:04-timing|Terminal showing the streamed answer, the chunk count and the two timings}}

In this run the opening chunk arrived after 0.97 s and the last after 2.03 s. A page that waits for the whole answer shows nothing for 2.03 s. A page that streams shows text after 0.97 s. Your numbers will differ. A screenshot is a single frame, so it cannot show text arriving. These two timings are the evidence for streaming.

## Step 2: Send the chunks from the server

The browser has a built-in way to read a stream of server messages, `EventSource`, and it expects the server-sent events format. Each event is a few `field: value` lines ended by a blank line. The server sends:

- `id`: the number of the chunk, so a client can say where it stopped.
- `data`: the text as a JSON string, so spaces and line breaks survive.
- `event: done` at the end, so the client can tell a finished answer from a cut one.
- `retry: 300` on the opening event, which asks the browser to reconnect after 300 ms.

`/demo` has two modes. Plain `/demo` replays the saved chunks with their recorded gaps and makes no API call. It is what you rehearse with, and what the screenshot tool opens. `/demo?live=1` makes one real call. The live route is capped at five calls per server process, and the file shows what happens when the key is missing.

{{file:app.py}}

Start the server and ask for a live answer with `curl`. This makes one real API call. The saved output below shows the opening and closing events.

{{cmd:05-sse-live}}

{{out:05-sse-live}}

{{shot:05-sse-live|Terminal showing server-sent events with ids and data lines, ending with an event named done}}

Each `data:` line is a small piece of the answer, cut where the model sent it. The stream ends with `event: done` and the number of chunks. Not every piece is a whole word, and the page does not need it to be.

## Step 3: Read the chunks in the page

The page opens an `EventSource`, appends each piece to a box with `textContent` (never `innerHTML`, since model text is not trusted), and keeps count. It also records when the opening chunk arrived. Opening the page with `?speed=0` replays the saved answer with no gaps, so the whole answer lands in a few milliseconds. That is why the screenshot at the top of this article shows a finished answer. Without `speed=0` the saved answer arrives with its recorded gaps, and the live button streams a real answer.

{{file:index.html}}

Start the server and open the page in your browser.

```bash
uvicorn app:app --port 8041
```

Open `http://127.0.0.1:8041/` and press the buttons. The left button replays the saved answer from `cache.json`. The second makes one real call for each press.

## Step 4: Handle a dropped connection

A stream can end early: a phone leaves Wi-Fi, a laptop sleeps, a proxy closes an idle connection. From the client side, the symptom is the same: the response ends and no `done` event arrived. The answer is half on screen.

`EventSource` reconnects by itself and sends the id of the last event it got in a `Last-Event-ID` header. The server reads that header, and for a saved answer it carries on from the next chunk. `test_drop.py` does by hand what the browser does: it reads four events, notices the missing `done`, asks again with the last id, and checks that the joined text equals the saved answer. The server ends the response cleanly after four events when you pass `drop_after=4`, which a real network drop does not, but the client sees the same thing.

{{file:test_drop.py}}

{{cmd:06-drop}}

{{out:06-drop}}

{{shot:06-drop|Terminal showing four events, no done event, a resume after event 3 and a match with the saved answer}}

A live answer cannot be resumed. The model would have to write it again, and that is a second paid call that may not match the earlier one. The server answers a live reconnect with status 409, which makes the browser stop retrying, and the page keeps the text it has and asks the reader to run it again. I did not run that 409 path in the saved evidence.

There is a cost on the other side too. If the reader leaves while a live answer is still coming, you want the upstream call to stop. In `app.py` the `async with` block around the stream closes the upstream connection when the server cancels the generator. `leave_early.py` opens a live stream and closes it after three events:

{{file:leave_early.py}}

{{cmd:07-leave}}

{{out:07-leave}}

{{shot:07-leave|Terminal showing the script leaving after 3 events and the server line saying the client left and the upstream stream was closed}}

The server noticed the loss only after it had already sent more events than the script read, because the data sits in socket buffers. That is why the count in the server line is higher than 3. The saved output shows the server logged that the upstream stream was closed. It does not show what the API billed for the cut call. That call is not in `spend.log`, which logs only finished answers.

## Questions people ask

**Does streaming make an AI hackathon demo better?** It does not shorten the total time. In the saved run the whole answer took 2.03 s and the text started to appear at 0.97 s. What changes is how long the page looks empty. Whether judges prefer that is a judgement I did not test.

**What happens to a streamed answer if the connection drops?** The stream ends without a `done` event. For a saved answer, the browser reconnects and the server continues from the next chunk, as in Step 4. A live answer cannot continue where it stopped, so the page keeps the text it has and asks for a new run.

**Can I add streaming late in an AI hackathon?** The change touches two places: the model call becomes `client.messages.stream`, and the page reads an `EventSource` instead of waiting for one response. Keep the old non-streaming route until the streamed one works, and keep a saved answer for the demo path.

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set` from `timing.py`.** Load the key in the same terminal you run the script from.
- **`/demo` fails with a missing `cache.json`.** Run `python timing.py` once. It writes the file the saved route replays.
- **The live button returns an error after a few presses.** The server allows five live calls for each run of `uvicorn`. Restart it to reset the count.
- **The page shows text all at once.** Check the URL for `speed=0`, which removes the recorded gaps. The server sends `X-Accel-Buffering: no`, which asks nginx not to hold back the stream. I did not test behind a proxy.
- **`Address already in use`.** An old server is still running on port 8041. Stop it or choose another port.

## What to try next

- Show a typing cursor until the `done` event arrives.
- Save each finished live answer to `cache.json` so your rehearsal route stays current.
- Add a timeout on the page that shows the saved answer if no chunk arrives in a few seconds.

## How this tutorial was tested

- Date: 10 November 2026. Python 3.14.6, `anthropic` 2.7.0, `fastapi` 0.162.2, `uvicorn` 0.54.0, macOS. The model is `claude-haiku-5-5`, set in `prompt.py`.
- The code in this article is copied from the project files by a script. Output and screenshots come from saved logs of real runs, with real API calls in Steps 1, 2 and 4.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. Model text and timings differed between runs, as expected.
- The page screenshot is a real Chrome screenshot of the running page, opened with `?speed=0`. Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run in the saved evidence: pressing the buttons in a browser, the live button, the 409 and 429 responses of the live route, and the missing-key response of `/demo?live=1`. I checked the browser reconnect once, outside the saved steps, by opening the page in headless Chrome with `?speed=0&drop=1`. Its status line showed one reconnect and a finished answer. That check is not in the evidence folder.
- Not run: Windows, Linux, browsers other than Chrome, and Python versions other than 3.14.6.
