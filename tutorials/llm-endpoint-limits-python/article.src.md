---
title: "Add Rate Limits and a Spending Cap: AI Hackathon Guide"
description: "AI hackathon safety: add rate limiting and a daily spending cap to an LLM endpoint. Count requests per user and stop at the cap."
seo_title: "Add Rate Limits and a Spending Cap: AI Hackathon Guide"
meta_description: "AI hackathon safety: add rate limiting and a daily spending cap to an LLM endpoint. Count requests per user and stop at the cap."
---

# Add rate limiting and a daily spending cap to an LLM endpoint in Python

You build a FastAPI endpoint that limits how often each user can call a language model, adds up the real cost of each call, and answers with HTTP 429 once a daily cap is reached.

**Time:** about 45 minutes. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, and an Anthropic API key. **Tested:** 11 November 2026 with Python 3.14.6, `anthropic` 2.8.0, `fastapi` 0.162.4, `uvicorn` 0.54.0 and `httpx` 0.28.1 on macOS.

Model replies differ from run to run. Your words, token counts and costs will not match the output below exactly. The shape of the output will.

Once an AI hackathon demo link is public, anyone can use it, and a spending cap keeps a surprise bill away. If you are preparing a project, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A public endpoint that calls a paid API spends your money for every visitor. Two guards cover two different risks. A request limit stops one user from hammering the endpoint. A cost cap stops the total, whoever the callers are. This tutorial builds both, and it ends with a list of what they do not protect against.

## See it running first

This is the cost cap tripping on real calls. The cap in this run is set to $0.0008, a very small number chosen so a few cheap calls reach it. The fourth request gets HTTP 429.

{{shot:06-cap|Terminal output of demo.py cap: three answers with HTTP 200, then HTTP 429 with the message daily cost cap reached}}

The rest of the tutorial builds it from scratch.

## Step 1: Set up the project

Make a folder, create a virtual environment and activate it.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt`:

{{file:requirements.txt}}

Install it. The output lists the versions used for this tutorial. FastAPI and the other packages installed on Python 3.14.6 without extra steps.

{{cmd:02-install}}

{{shot:02-install|Terminal listing the installed versions of anthropic, fastapi, httpx and uvicorn}}

Put your key in a `.env` file from this template, and load it into your terminal with `set -a; source .env; set +a`. Never paste a real key into code or a screenshot.

{{file:.env.example}}

## Step 2: Write the two guards

The guards live in `limits.py`, apart from the web code, so they can be checked without a server and without an API call.

`RateLimiter` keeps a list of recent request times for each user. A request is allowed if the user has made fewer than `limit` requests in the last `window` seconds. Otherwise it returns how many seconds to wait, which becomes the `Retry-After` header.

`DailyCap` adds up the spend for one UTC day and starts again at zero when the date changes. The cost of a call comes from the token counts the API returns, multiplied by a price. The prices at the top of the file are an assumption: they are example numbers chosen for this tutorial, not published prices. Look up the current prices for your model and change them before you trust any dollar figure.

The cap is checked before a call and the real cost is added after it. So one call can carry the total past the cap. The cap is a stop, not an exact ceiling.

{{file:limits.py}}

## Step 3: Check the guards with fixed numbers

`test_limits.py` uses a fake clock and a fake date. It checks that the third request in a window waits, that another user has its own count, that the window passes, and that a new day resets the total. A test with fixed numbers is a good extra, but it does not replace the real calls later.

{{file:test_limits.py}}

{{cmd:03-unit}}

{{shot:03-unit|Terminal output of test_limits.py ending with all checks passed}}

One call of 1000 input tokens and 100 output tokens costs $0.0015 at the example prices, which is over a $0.001 cap.

## Step 4: Build the endpoint

`app.py` has two routes. `POST /ask` sends a question to the model. `GET /usage` shows the counters. The order inside `/ask` matters. The request limit runs first, then the cap check, and only then the paid call, so a blocked request costs nothing.

Settings come from environment variables with small defaults. The user is the `X-User` header, or the client address if the header is missing. Every blocked call is appended to `blocked.log` with the time, the user and the reason.

The call turns thinking off and uses `max_tokens` of 80. In an earlier test with thinking on and a low `max_tokens`, `claude-haiku-5-5` could return only a thinking block and no text. The code also joins only the text blocks and falls back to "(empty reply)", so an empty reply does not crash the endpoint. A reply cut at 80 tokens ends mid-sentence, as the screenshots show.

{{file:app.py}}

If the key is missing, the app stops at start-up with a clear message. This is what that mistake looks like:

{{cmd:04-no-key}}

{{shot:04-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

## Step 5: Reject over the per-user limit

`demo.py` starts the real server on port 8136 and sends real requests. This run sets the limit to 2 requests per 60 seconds and a high cap, so only the limit can block.

{{file:demo.py}}

{{cmd:05-rate}}

{{out:05-rate}}

{{shot:05-rate|Terminal output of demo.py rate: two answers for ana, HTTP 429 with Retry-After 58, then an answer for ben}}

User `ana` gets two answers, then HTTP 429 with `Retry-After: 58` and the body `{"error":"rate limit"}`. User `ben` still gets an answer, because his count is separate. Only three calls reached the model. The counters show 3 calls and a spend of $0.000317.

## Step 6: Stop at the daily cost cap

This run sets the cap to $0.0008 and the request limit high. The same question is asked until the endpoint answers 429. Each answer costs about $0.0004 at the example prices.

{{cmd:06-cap}}

{{out:06-cap}}

After the second call the total is $0.000791, just under the cap, so a third call is allowed. It brings the total to $0.001224, which is over the cap. The fourth request gets HTTP 429 with `{"error":"daily cost cap reached"}`. That is the 429 a client sees, and the model is not called for it. The total ended $0.000424 above the cap, which is the one-call overshoot described in Step 2.

## Step 7: Read the blocked-call log

Each block was written to `blocked.log` as one JSON line, so you can count blocked calls and see which user caused them.

{{cmd:07-logs}}

{{shot:07-logs|Terminal output of the blocked-call log: one rate limit line and one daily cost cap reached line}}

## Step 8: See a restart wipe the counters

The counters are Python objects in memory. This step makes one call, stops the server, starts it again and reads the usage.

{{cmd:08-restart}}

{{shot:08-restart|Terminal output: one call is counted, then after the restart the usage shows 0 calls and a spend of 0.000000}}

Before the restart the usage shows 1 call. After it, 0 calls. A restart gives every user a fresh limit and a fresh cap. Anyone who can crash or redeploy your service resets your protection.

## Step 9: Run the server yourself

Start the server on port 8136 and open the usage page in a browser.

{{cmd:09-serve}}

{{shot:09-serve|Browser showing the usage page: 0 calls, spend 0.000000, cap 0.001000, limit 5 per 60s per user}}

A fresh server shows 0 calls, a cap of $0.001000 and the default limit of 5 requests per 60 seconds per user. To make a call yourself, use `curl -X POST http://127.0.0.1:8136/ask -H "Content-Type: application/json" -H "X-User: ana" -d '{"question": "Say hello."}'`.

## Security review: what this does not protect against

This is a teaching example. It is not a complete defence, and it is not security advice for your production system. Have someone review a real deployment.

- **Spoofed users.** The user is a header the client sends. Anyone can change it and get a fresh limit each time. Use a signed-in identity for a real limit.
- **Shared addresses.** Without the header the limit falls back to the client address. People behind one office or school network share it, and one heavy user blocks the others. Behind a proxy, the address you see may be the proxy's.
- **Restarts and several processes.** Counters are in memory. A restart clears them (Step 8). Two copies of the server each keep their own counters, so the real limit is doubled. A shared store such as a database is the usual fix.
- **One call of overshoot.** The cap is checked before the call. Several calls started at the same moment can all pass the check, so the total can go over by more than one call.
- **Prices go stale.** The cost is a calculation from example prices. If the real price is higher, the real spend is higher than the cap says. The cap does not read your provider's bill. Set a spending limit in your provider account as well.
- **Other attacks.** Nothing here covers authentication, abuse of other routes, large request bodies beyond the 500-character question limit, or prompt content. The blocked-call log stores the user name, so treat it as personal data if the names are real.

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set`.** The variable is not in the terminal you are running from. Run the `set -a; source .env; set +a` line again there.
- **`address already in use` on port 8136.** An earlier server is still running. Stop it, or change the port in the command and in `demo.py`.
- **The cap never trips.** Replies are short, so each call costs little. Lower `DAILY_CAP_USD`, or ask a question with a longer answer.
- **The reply is empty.** With thinking on and a low `max_tokens`, a reply can hold only a thinking block. The code here turns thinking off and handles an empty reply.
- **The 429 shows up too early.** The default limit is 5 requests per 60 seconds per user. Raise `RATE_LIMIT` for your own tests.

## Frequently asked questions

**How do I stop people running up my API bill?**

Use two guards. Limit requests per user so one person cannot flood the endpoint, and keep a daily cost total from the token counts the API returns, so the endpoint stops at a set amount. In the test, the cap of $0.0008 stopped the endpoint on the fourth request.

**What limit should a demo have?**

The tutorial did not find a right number, because it depends on your price and your audience. It used 2 requests per minute to show the 429, and a default of 5 per minute. Start low, read the blocked-call log, and raise the limit if real users are blocked.

**How do I log blocked calls?**

Write one line each time you return 429, with the time, the user and the reason. The app does this in `blocked.log`. In the test the log held one rate limit line and one daily cost cap reached line.

## What to try next

- Keep the counters in a database or Redis so a restart does not clear them.
- Limit by signed-in user instead of a header.
- Return the remaining budget in a response header so a client can show it.

## How this tutorial was tested

- Date: 11 November 2026. Python 3.14.6, `anthropic` 2.8.0, `fastapi` 0.162.4, `uvicorn` 0.54.0, `httpx` 0.28.1, macOS. The model is `claude-haiku-5-5`.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls and a real running server on port 8136.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. Model replies and costs differed slightly between the two runs (for example the cap run ended at $0.001229 on the replay), as expected.
- A full run makes 7 model calls with at most 80 output tokens each, well under one cent at the example prices.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window. The Step 9 screenshot is a real browser capture of the running page.
- The prices in `limits.py` are example numbers, not published prices. They were not checked against a price list.
- Not run: Windows, Linux, Python versions other than 3.14.6, more than one server process, requests from many different addresses, a proxy in front of the server, and a long-running server across a UTC date change (the date reset is checked only with a fake date in `test_limits.py`).
