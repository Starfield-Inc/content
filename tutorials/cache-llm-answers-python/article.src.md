---
seo_title: "Cache LLM Answers to Cut AI Hackathon Costs"
meta_description: "AI hackathon cost tip: cache LLM answers in Python. Hash the request, return hits, add an expiry and count the saving."
---

# Cache LLM answers in Python to skip repeat calls

You build a small cache that sits in front of the Anthropic API. It hashes the request, returns a stored answer when the same request comes back, forgets entries after a set time, and reports how many calls and tokens it saved on a test set.

**Time:** about 40 minutes. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, and an Anthropic API key. **Tested:** 11 November 2026 with Python 3.14.6 and the `anthropic` package 2.8.0 on macOS.

Model replies differ from run to run. Your words, token counts and timings will not match the output below. The shape of the output will: a miss makes a call, a hit does not.

Credits are limited in an AI hackathon, and a cache stops you paying twice for the same answer. If you plan to build something with a language model, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

Every call to a language model API costs tokens and takes seconds. Programs often ask the same thing more than once: a demo that reloads, a test suite that reruns, a user who clicks twice. A cache answers the repeats from a file on disk. The part that needs care is the key. If the key leaves out something that changes the answer, you return a wrong answer. If it includes something that does not matter, you miss when you did not need to.

This tutorial reports tokens, not money. The saved output has no prices, so the numbers below are calls, tokens and time. Multiply the tokens by the price on your provider's page on the day you run it.

## See it running first

This is the second run of the same seven questions. Nothing was sent to the API.

{{shot:06-second-run|Terminal output of ask_many.py on a second run: seven hits, zero API calls, zero time}}

The rest of the tutorial builds it from scratch.

## Step 1: Set up the project

Make a folder, create a virtual environment and activate it.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt` with one line:

{{file:requirements.txt}}

Install it. The output shows the version used for this tutorial.

{{cmd:02-install}}

{{out:02-install}}

Put your key in a file named `.env`, copied from this placeholder:

{{file:.env.example}}

Load it into your terminal session (macOS and Linux) with `set -a; source .env; set +a`. Never paste a real key into code, a screenshot or a chat. If the key is not set, the scripts stop with a plain message. This is what that looks like:

{{shot:04-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

## Step 2: Decide what goes into the key

The key is a hash of everything that can change the answer. Here that is the model name, `max_tokens`, the thinking mode, the system prompt and the question. The fields go into a JSON string with sorted keys, so the same fields always give the same text, and the text goes through SHA-256.

`llm_cache.py` holds the key function, the cache and the `ask` function. The whole file is below. The next steps use parts of it.

{{file:llm_cache.py}}

Run `key_demo.py`. It changes one field at a time and shows whether the key changes. No API call is made.

{{cmd:03-keys}}

{{shot:03-keys|Terminal output of key_demo.py: a new key for another model name, max_tokens, thinking mode, extra space, trailing space and lower case}}

Read the verdict column. The same request gives the same key. A different model name gives a new key, which is right: another model gives another answer. A different `max_tokens` or thinking mode also gives a new key. So does one extra space inside the question, or one space at the end.

The last three lines are the fix for whitespace. With `normalize=True`, the question is split on whitespace, joined with single spaces and lower-cased before hashing. The messy and the tidy question then share one key. That key also differs from the base key, because the base key was made without normalizing. Lower-casing is a choice, not a rule: if capital letters change the meaning of your questions, such as in code, do not lower-case.

## Step 3: Store the answer and return hits

The `Cache` class keeps a dictionary and writes it to a JSON file after each new answer. `get` returns an entry or `None`. `put` saves the text, the token usage from the API's `usage` field, and the time. The usage is saved so that a hit can report how many tokens it avoided.

`ask_many.py` runs `questions.txt` through the cache. The file has seven lines: four different questions, two exact repeats of the first two, and a messy repeat of the third with a double space and spaces at both ends.

{{file:questions.txt}}

{{file:ask_many.py}}

Run it with an empty cache:

{{cmd:05-first-run}}

{{shot:05-first-run|Terminal output of the first run: five misses with API calls and two hits at 0.0 ms}}

Five calls were made, for seven questions. Lines 5 and 6 were hits: they returned the stored answers for lines 1 and 2. Each miss took between 1159.9 ms and 2762.7 ms. A hit rounds to 0.0 ms. Total time was 9.00 s.

The tokens sent to the API were 190 input and 318 output, counted from the `usage` field of each real reply. The two hits avoided 78 input and 167 output tokens. For a hit, the `in=` and `out=` columns show the tokens of the original call.

Line 7 was a miss. The extra spaces made a new key, and the cache paid for an answer it already had.

## Step 4: Run it again

Run the same command without deleting the cache file:

{{cmd:06-second-run}}

{{out:06-second-run}}

All seven were hits and no call was made. The run avoided 268 input and 485 output tokens, and the total time rounds to 0.00 s. The cache file kept the answers between two separate runs of the program, which is the point of writing it to disk.

## Step 5: Fix the whitespace miss

Run the test set again with `--normalize` and a new cache file, so the old entries do not interfere:

{{cmd:07-normalize}}

{{shot:07-normalize|Terminal output with normalize on: four calls and three hits, the messy line is a hit}}

Four calls instead of five, and three hits instead of two. Line 7 now matches the answer stored for line 3. The input tokens sent fell from 190 to 153. The output tokens fell from 318 to 232, but part of that gap is the model answering differently, so do not credit all of it to the cache.

## Step 6: Change a setting and miss on purpose

The cache must not return an answer made under other settings. Run the first two questions with `--max-tokens 500` against the original `cache.json`, which holds answers made with 300:

{{cmd:08-settings}}

{{shot:08-settings|Terminal output with max_tokens 500: two misses, zero hits, even though the questions are in the cache}}

Both were misses. The questions were in the file, but under keys made with `max_tokens` 300. This is a correct miss. It costs a call, and it prevents mixing answers made under different settings.

## Step 7: Know which settings the model accepts

A common cache key holds the temperature. I planned to include it. When I added `temperature` to the call, the SDK method I used (`messages.create` in `anthropic` 2.8.0) had no such argument. Sending it through `extra_body` shows what the API says:

{{file:temperature_probe.py}}

{{cmd:08b-temperature}}

{{shot:08b-temperature|Terminal output: HTTP 400, temperature: Extra inputs are not permitted}}

For `claude-haiku-5-5` the request was refused, so temperature is not in this key. The rule is general: put every setting you send into the key, and nothing you do not send. If you use a model that takes a temperature, add it to `make_key`, or two requests that differ only in temperature will share an answer. I did not test other models.

## Step 8: Add an expiry

An answer can go stale. `Cache.get` compares the saved time with the time-to-live (TTL). If the entry is older, it deletes it and reports a miss. `expiry_demo.py` uses a 2 second TTL so the demo is short. A real TTL is hours or days, and depends on how fast your answers go out of date.

{{cmd:09-expiry}}

{{shot:09-expiry|Terminal output of expiry_demo.py: miss, hit, then miss again after a 3 second wait}}

The first ask was a miss at 1979.1 ms. The second, right away, was a hit. After a 3 second wait the entry had expired, and the third ask was a miss at 1592.3 ms.

## Step 9: Never cache an empty reply

A reply can hold no text. While building other tutorials, we saw that with thinking on and a low `max_tokens`, `claude-haiku-5-5` can return only a thinking block. I did not reproduce that here, because the code turns thinking off with `{"type": "disabled"}` and uses 300 tokens. The code still defends against it. `reply_text` joins only the text blocks, and `Cache.put` returns without saving when the text is empty. Otherwise one bad reply would be returned forever.

`test_cache.py` checks this with fixed data and a stand-in client. It makes no API call, so it is a check of the rule, not a test of the model.

{{cmd:10-empty}}

{{out:10-empty}}

## Troubleshooting

- **`TypeError: Messages.create() got an unexpected keyword argument 'temperature'`.** The SDK method has no `temperature` argument in the version tested. See Step 7. The API also refused it.
- **Every run is all misses.** Check that the cache file is in the folder you run from, and that nothing in the key changes each run, such as a timestamp in the system prompt.
- **Two questions that mean the same thing both miss.** The cache matches the exact text after tidying, not the meaning. Matching by meaning needs embeddings, and is not built here.
- **The cache returns an old answer.** Lower the TTL or delete the cache file.
- **The cache file holds your questions and answers as plain text.** Do not cache anything private, and do not commit the file.

## Frequently asked questions

**Does caching work when answers vary?**

Yes, with a limit. The cache returns the first answer it saw, so later calls repeat it. In this test the same question gave 87 output tokens in one run and 64 in another, so a fresh call would have been different. Cache when a stored answer is good enough.

**How long should I keep a cached answer?**

It depends on how fast the answer goes stale. The demo used 2 seconds only to show an expiry. Pick a TTL from your own data: a definition can stay for days, a question about today's news should not.

**How do I measure the saving?**

Count calls and read the `usage` field. On the seven-question test the first run made 5 calls instead of 7. The second run made none and avoided 268 input and 485 output tokens. Turn tokens into money with the price on your provider's page.

## What to try next

- Add a cap on the number of entries and remove the oldest first.
- Cache by meaning with embeddings, and check how often it returns a wrong answer.
- Keep the system prompt in a file and hash its contents, so an edit to it makes new keys.

## How this tutorial was tested

- Date: 11 November 2026. Python 3.14.6, `anthropic` 2.8.0, macOS. The model is `claude-haiku-5-5`, set in the `MODEL` constant.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls, with one exception: `test_cache.py` uses fixed data and a stand-in client on purpose.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment and no cache files. The replay passed. The saved text of replies differed between the two runs, as expected.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run: Windows, Linux, Python versions other than 3.14.6, and models other than `claude-haiku-5-5`. The empty-reply case from thinking mode was not reproduced. The cost was not computed because the saved output has no prices.
