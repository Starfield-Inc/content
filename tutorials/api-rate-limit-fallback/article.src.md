---
seo_title: Handle API Rate Limits in an AI Hackathon Demo
meta_description: Keep your AI hackathon demo working when an API rate limit hits. Add retry with backoff and a saved answer as a fallback, and test both.
---

# Keep your hackathon demo working when the API rate limit hits

You build a small wrapper around the Claude API that retries with exponential backoff and jitter, logs each retry, and falls back to a saved answer when the API keeps failing. You test it against a local stand-in server, so you never have to hit a real limit.

**Time:** about two hours. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, and an Anthropic API key. **Tested:** 10 November 2026 with Python 3.14.6 and `anthropic` 2.7.0 on macOS.

Model replies differ from run to run. Your reply will not match the one below word for word, and the timings will differ too.

Some AI hackathon sponsors raise API limits only for the length of the event, and demo day is when the limits bite hardest. A demo that shows an error page at that moment is worse than a demo that shows an answer you saved earlier. For more events like this, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A rate limit is the API telling you to slow down. The error is normal, it is temporary, and your code can plan for it. This tutorial does three jobs: it shows what the error looks like, it waits and tries again in a way that does not make things worse, and it keeps the demo on screen if waiting does not help.

One thing to say plainly. The stand-in server in this tutorial is a test tool I wrote. It sends the errors the API documents, so the SDK's real error classes run against them. It is not the API, and it says nothing about your account's limits. Real limits depend on your account and plan, and on the model. I never hit a real limit while writing this.

## See it running

Here is the finished wrapper handling an API that keeps returning 529, and then falling back. The rest of the tutorial builds it.

{{shot:07-wrapper|Terminal showing two cases: retries after a 429 that end in a live reply from the stand-in, and retries after 529 errors that end in the saved answer}}

## Step 1: Set up and make one real call

Create a virtual environment and install the SDK.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

{{file:requirements.txt}}

{{cmd:02-install}}

{{shot:02-install|Terminal listing the installed version of anthropic}}

Put your key in a file named `.env`. Copy the placeholder file and edit it:

{{file:.env.example}}

Never paste a real key into code, a screenshot or a chat. Load the file into your terminal session (macOS and Linux):

```bash
set -a; source .env; set +a
```

Without the key, the script stops with a message:

{{shot:03-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

The settings are in `prompt.py`. `thinking={"type": "disabled"}` turns off extended thinking, which the API docs list as accepted by `claude-haiku-5-5`.

{{file:prompt.py}}

{{file:spend_log.py}}

`one_call.py` makes the normal case: one real call that works. It also prints `client.max_retries`, and it saves the reply to `saved_answer.json`. That file is your fallback. Make it before the event, when the API is working.

{{file:one_call.py}}

{{cmd:04-one-call}}

{{out:04-one-call}}

{{shot:04-one-call|Terminal showing max_retries 2, a reply about recycling, the token counts and the saved file message}}

The number `2` on the opening line is the SDK's default. The next step shows where it comes from.

## Step 2: Read what the SDK already does

The SDK retries by itself. Before you add a second layer, read what the built-in one does. `show_sdk_retry.py` prints it from the package you installed, so the output is the code, not a description of it.

{{file:show_sdk_retry.py}}

{{cmd:05-sdk-source}}

{{out:05-sdk-source}}

{{shot:05-sdk-source|Terminal listing the SDK's default retry constants, the status codes it retries and its backoff calculation}}

Read it in three parts:

- **What it retries.** Status 408, 409, 429 and everything from 500 up, plus connection errors. A response header named `x-should-retry` can override the status code. A 400 or 401 is not retried.
- **How many times.** `DEFAULT_MAX_RETRIES = 2`, so up to three calls in all.
- **How long it waits.** If the response has a positive `retry-after` header, the SDK waits exactly that long. If not, it waits 0.5 s doubled for each retry, capped at 8.0 s, then multiplied by a random number between 0.75 and 1.0 as jitter.

Anthropic's error documentation says the same: the SDK retries connection errors, rate limits and 5xx errors twice by default, with exponential backoff, and honors `retry-after` when present.

So why write your own? Three reasons. The SDK gives up after two retries, and you may want more. It has no fallback. And its retry messages go to Python's `logging` module at info level (I read this in the source), which is silent unless you set logging up, so a stalled demo looks like a hung page.

## Step 3: Reproduce the errors without hammering the API

To test an error path you need the error. Sending real traffic until the API pushes back costs money, and is not repeatable. Instead, `standin.py` is a small local HTTP server. It answers `POST /v1/messages` with an error for N calls at the start, and then with a valid reply. You can set the status (429 or 529), the `retry-after` header, and N. It also records when each call arrived.

The SDK takes a `base_url` option, so you point the real client at the stand-in. The SDK code that parses the response, builds the error and decides about retries is the real code. Only the server is fake.

{{file:standin.py}}

`reproduce.py` shows four cases. The client in cases 1 and 2 has `max_retries=0`, so you see the raw error.

{{file:reproduce.py}}

{{cmd:06-reproduce}}

{{out:06-reproduce}}

{{shot:06-reproduce|Terminal showing a RateLimitError with status 429 and retry-after 1, an OverloadedError with status 529, and the default client retrying twice}}

What to notice:

- A 429 arrives as `anthropic.RateLimitError`. The `retry-after` header is on `error.response.headers`.
- A 529 arrives as `anthropic.OverloadedError`, which is a subclass of `anthropic.InternalServerError`. Catching `InternalServerError` catches both.
- In case 3 the default client hit two 429s and then got a reply, and your code saw no error at all. The stand-in received 3 calls, about a second apart, which is the `retry-after` value.
- In case 4 a third 429 made the default client give up and raise.

## Step 4: Add retry with backoff and jitter

`resilient.py` holds the wrapper. Here is why it looks like this.

- **Backoff.** Each wait is longer than the one before, so a struggling API gets room to recover.
- **Jitter.** Each wait is a random fraction of the ceiling. If many clients fail together and all wait the same time, they all return together. Randomness spreads them out. With a `retry-after` header the wrapper waits that long plus a small random amount.
- **A limit on waiting.** If the server asks for more than `max_wait` seconds, the wrapper stops and uses the saved answer. On a stage nobody waits a minute.
- **Which errors.** It retries rate limits, server errors and connection errors. A 401 means your key is wrong, and waiting will not fix it, so the wrapper raises it. A fallback that hides a bad key would hide a bug until demo day.
- **Logging.** Each retry writes one line: the attempt, the error class and status, the header, and the wait.
- **Functions you can replace.** `sleep` and `rand` are parameters so a test can run without waiting.

{{file:resilient.py}}

## Step 5: Add the saved answer and watch it work

`ask()` returns an `Answer` that says where the text came from, `live` or `saved`. Show that on screen in your real demo so you know which one the judges see.

`demo_wrapper.py` runs two cases against the stand-in. In case 1 the stand-in returns 429 twice and then a reply. In case 2 it returns 529 every time.

{{file:demo_wrapper.py}}

{{cmd:07-wrapper}}

{{out:07-wrapper}}

Case 1 recovered after two retries. Each wait was a little over the 1 s the stand-in asked for, because of the jitter, and the stand-in's own record of call gaps matches the log lines. Case 2 made 4 calls, waited between them, and then returned the saved answer from Step 1. The waits in this run were random numbers under a ceiling that doubles each time (0.5 s, 1 s, 2 s). The log lines are also written to `retries.log`.

## Step 6: Do not stack retry layers

The wrapper in `demo_wrapper.py` uses a client made with `max_retries=0`. That is deliberate. If you leave the SDK default in place, each of your attempts becomes up to three calls, and you hit the API harder at the moment it asked you to slow down. `layers.py` counts the calls.

{{file:layers.py}}

{{cmd:08-layers}}

{{out:08-layers}}

{{shot:08-layers|Terminal showing 3 calls with max_retries 0 and 9 calls with the default client for the same 3 wrapper attempts}}

Three wrapper attempts reached the stand-in as 3 calls with `max_retries=0` and as 9 calls with the default. Pick one layer. Either keep the SDK's two retries and write only the fallback, or set `max_retries=0` and own the whole policy, as here.

## Step 7: Test it

The tests start the stand-in on a free port, call `ask()` with the real SDK, and record the waits instead of sleeping. They check the success path, a `retry-after` wait, the exponential growth and the cap, the log lines, the fallback after the last attempt, a long `retry-after` going straight to the fallback, and that a 401 is raised. They use the standard library `unittest`, so there is nothing more to install.

{{file:test_resilient.py}}

{{cmd:09-tests}}

{{out:09-tests}}

{{shot:09-tests|Terminal showing eight tests passing}}

All eight tests passed. The tests prove that the wrapper behaves as designed against the stand-in. They do not prove how the real API behaves under a real limit.

## Questions people ask

**Why do I get a 429 error in my AI hackathon project?** A 429 means a rate limit was hit. In the SDK it arrives as `anthropic.RateLimitError`, and the `retry-after` header tells you how long to wait if the server sent one. Anthropic's error documentation also lists a 429 that comes from a spend cap and has no `retry-after` header, and says it keeps failing until access resumes, so retrying will not fix that one. Which limits apply to you depends on your account.

**What should my demo do when the API is down?** Retry a few times with growing, random waits, then show a saved answer and label it as saved. A 529 arrives as `OverloadedError`. In Step 5 the wrapper made 4 calls against a stand-in that always failed, then returned the saved reply. Raise errors that waiting cannot fix, such as a bad key.

**Should I use more than one model provider in an AI hackathon?** I did not test a second provider here, so I cannot say what it costs you in time. The wrapper has one place where the live call happens, so a second provider would be another attempt before the saved answer. The saved answer is the one fallback that needs no network.

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set`.** Load the key in the same terminal you run the script from.
- **`FileNotFoundError: saved_answer.json`.** Run `python one_call.py` once. It writes the file.
- **Your demo still calls the API far more than you expect.** Check the client's `max_retries`. See Step 6.
- **The wrapper raises `AuthenticationError`.** That is on purpose. The key is wrong or revoked.

## What to try next

- Show a small "saved answer" badge on the page when `source` is `saved`.
- Add a total time budget, so retries stop after a fixed number of seconds.
- Save each good live answer, so the fallback stays current.

## How this tutorial was tested

- Date: 10 November 2026. Python 3.14.6, `anthropic` 2.7.0, macOS. The model is `claude-haiku-5-5`, set in `prompt.py`.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs. The only real API call in each run is `one_call.py` in Step 1. Everything else runs against the local stand-in server.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. The model's reply differed between the two runs, as expected, and so did the random waits.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- The SDK behaviour in Step 2 is read from the installed package at version 2.7.0. Other versions can differ.
- Not run: a real rate limit or a real overloaded response from the API, other models, streaming calls, the async client, Windows, Linux, and Python versions other than 3.14.6.
