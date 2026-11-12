---
title: "Track New Hugging Face Models: AI Hackathon Tutorial"
description: "AI hackathon tool: build a new-model alert from the public Hugging Face API. Filter copies and fine-tunes and remember what you have seen."
---

# Get an alert when a new model appears on Hugging Face

You will build a small Python script that lists new models from the organisations you choose, leaves out copies and fine-tunes of other people's models, remembers what it has already reported, and writes a message to the terminal and to a text file. It takes about 40 minutes and needs no account and no API key.

**Level:** Intermediate. **You need:** Python 3.10 or newer, a terminal and an internet connection. **Tested:** 10 November 2026 on macOS with Python 3.14 and `requests` 2.34.2. The Windows activate command was not run.

Sponsors of an AI hackathon may point teams to new models, and an alert tells you when a publisher you follow posts one. See the [upcoming AI hackathons](/ai-hackathons/) to find a place to use it.

## Why this is worth a script

Hugging Face is where many open-weight models are published. The lists on the site mix official releases with quantised copies and fine-tunes uploaded by other people. A script that watches named publishers gives you a short list, and a state file means you hear about each model once.

## See it running first

By the end, one command prints a message like this:

{{shot:06-first|Terminal showing the alert script finding 10 new models from four organisations}}

The models in the screenshot are what the API returned on 10 November 2026. Yours will differ, because the results depend on live data and on the date you run the script. The rest of this tutorial builds the script from scratch.

## Step 1. Create a virtual environment

Make a project folder, open a terminal in it, and run:

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Activate it with `source .venv/bin/activate` on macOS and Linux. Every command below assumes it is active.

## Step 2. Install requests

`requests` makes the web calls. It is the only package this project needs.

{{file:requirements.txt}}

{{cmd:02-install}}

{{shot:02-install|Terminal after installing requests, showing its name and version}}

## Step 3. Call the public models API

The Hub has a public endpoint, `https://huggingface.co/api/models`. It needs no token for public models. We ask for one organisation at a time (`author`), newest first (`sort=createdAt`), and only 30 models (`limit`). We ask for four fields with `expand[]` and nothing else,.

The script follows three rules for being polite. It sends a User-Agent that says who is calling. It pauses one second after each call. It stops if the API answers with HTTP 429 (too many requests) instead of trying again. The API also reports how many calls you have left in the current window, in a header called `ratelimit`, and the script reads it so you can see it.

{{file:hfapi.py}}

## Step 4. Look at what a model record contains

Before writing a filter, look at a real record. This script fetches 40 models from the publisher `unsloth`, which publishes many quantised copies of other people's models, and prints one that has a `base_model` tag. It prints only the tags that matter here.

{{file:show_one.py}}

{{cmd:03-fields}}

{{shot:03-fields|Terminal showing one model record with gated false and two base_model tags}}

Three fields are useful. `createdAt` is the date for the date filter. `tags` carries the licence (`license:other`) and the base model. `gated` says whether you must ask for access. The `base_model` tag appears twice: once in a short form (`base_model:mistralai/Mistral-Large-4-1T-A52B`) and once with the relation (`base_model:quantized:...`). The relation can also be `finetune`, `adapter` or `merge`.

## Step 5. Pick a filter by comparing real results

We tried four rules on the newest 40 models of seven organisations. Each rule answers "should this model be dropped?". They are in `filters.py`:

{{file:filters.py}}

`compare_filters.py` counts what each rule would drop, using one call per organisation:

{{file:compare_filters.py}}

{{cmd:04-compare}}

{{shot:04-compare|Table of how many models each of four rules would drop for seven organisations}}

What the table shows:

- **`gated` does not find copies.** It dropped 41 of 280 models. 40 of those were `meta-llama`, where every one of the 40 models is gated although Meta published them. It dropped nothing from `unsloth`. Gating is about access, not about origin.
- **Any `base_model` tag is too wide.** It dropped 147 of 280, including 25 from `Qwen`, 24 from `google` and 26 from `mistralai`. Publishers tag their own quantised and instruction-tuned releases with a base model too, and you want those.
- **A `base_model` owned by someone else works for these seven organisations.** It dropped 35 of 40 from `unsloth` and none from `Qwen`, `google`, `mistralai`, `deepseek-ai` or `meta-llama`. It also dropped 13 of 40 from `microsoft`. We did not read those 13 one by one, so we cannot say how many are copies and how many are Microsoft's own fine-tunes of other publishers' models. For an alert that is a reasonable result, since both are derived models.
- **Looking for words like `gguf` in the name is unreliable.** It dropped 19 of 40 from `unsloth` but also 4 from `Qwen`, 5 from `google` and 6 from `mistralai`, which are official releases.

We chose the other-author rule (`rule_other_author_base`). It has one gap, which step 8 shows: a re-upload with no `base_model` tag passes through. The main protection is the list of organisations you watch.

Unit tests on fixed records keep the rule honest when you change it. This is the one step that does not call the API:

{{file:tests/test_filters.py}}

{{cmd:05-test}}

{{shot:05-test|Terminal showing five tests passing}}

## Step 6. Write the alert script

The script reads `orgs.txt`, fetches each organisation, keeps models inside the date range, drops copies, and keeps only models not yet in `seen.json`. The state file is written to a temporary file and then renamed, so a crash cannot leave half a file. If an organisation returns no models, the script stops with exit code 2 and does not touch the state file. The message goes to the terminal and is appended to `alerts.txt`.

{{file:orgs.txt}}

{{file:hf_alert.py}}

## Step 7. Run it, then run it again

The initial run has an empty state file, so everything in the date range is new. The date range is 45 days by default.

{{cmd:06-first}}

On 10 November 2026 the four organisations gave 1 model for `Qwen`, none for `google`, 8 for `mistralai` and 1 for `deepseek-ai`: 10 in all. Nothing was dropped as a copy: none of these ten carries a `base_model` tag that points to another author. The last line shows 458 calls left in the window.

Run it again with nothing changed:

{{cmd:07-second}}

{{shot:07-second|Terminal showing no new models on the second run}}

Each organisation still shows its models in the date range, but every one has been seen, so the script prints "No new models since the last run." That is the state file doing its job.

To see an alert for a single new model without waiting for a release, `forget.py` removes the newest entry from `seen.json`:

{{file:forget.py}}

{{cmd:08-forget}}

{{shot:08-forget|Terminal showing one model announced again after forget.py}}

This time the script reports 1 new model, the entry that was forgotten. The text file keeps every message:

{{cmd:12-files}}

{{shot:12-files|Terminal showing alerts.txt and the start of seen.json}}

## Step 8. Watch a publisher full of copies

Now point the script at `unsloth` with a 14-day range. Separate state and message files keep this test away from your real ones.

{{cmd:09-copies}}

{{shot:09-copies|Terminal showing four models in range, three dropped as copies and one announced}}

Four models were in the range, three were dropped as copies, and one was announced: `unsloth/Kimi-K3.1-Pro`. With `--keep-copies`, the filter is off:

{{cmd:10-keep}}

{{shot:10-keep|Terminal showing all four unsloth models announced when the copy filter is off}}

The three that the filter removed are `Mistral-Large-4-1T-A52B` uploads in GGUF, FP8 and NVFP4 formats, each tagged as derived from a `mistralai` model. `Kimi-K3.1-Pro` has no `base_model` tag, so the rule keeps it. We did not check whether it is a re-upload of someone else's model. This is the gap in the rule. If the publisher is not on your list, it never comes up.

## Step 9. What a mistake looks like

Organisation names are case sensitive. `qwen` is not `Qwen`, and the API answers with an empty list and no error:

{{cmd:11-mistake}}

{{shot:11-mistake|Terminal showing no models found for the name qwen}}

The script catches the empty list, tells you to check the spelling, and exits with code 2. A scheduler that checks exit codes will then see the failure.

## Step 10. Send the message somewhere else

The message is a plain string, so you can send it elsewhere. Many chat tools accept an HTTP POST with a small JSON body to a webhook address they give you. In `hf_alert.py` you would add one `requests.post(webhook_url, json={"text": message})` after the message is built, and keep the address in an environment variable, never in the code. This tutorial does not set up or run any webhook, and the step is untested here. Check your chat tool's own documentation for the body it expects.

## Step 11. Run it on a schedule

We did not install a schedule while writing this. These are the usual options for you to try.

On macOS and Linux, `cron` runs a command at set times. You edit your table with `crontab -e` and add a line with five time fields and a command. The command needs full paths, because cron does not activate your virtual environment: run the Python inside `.venv` directly and `cd` to the project folder first, since the script reads `orgs.txt` and `seen.json` from the current folder.

On macOS, `launchd` is the built-in alternative. You write a property list file in `~/Library/LaunchAgents` with the program, its arguments, the working directory and a `StartCalendarInterval`, then load it with `launchctl`.

Whichever you use, run the script by hand first, keep the pause and the small limit, and do not poll more often than you need.

## Troubleshooting

- **"no models found" for an organisation you know exists.** Check the capitalisation. The name in the URL on the model page is the one to use.
- **"Rate limited".** The API returned HTTP 429. Wait the time it names, and check the `ratelimit` header it sends (`r` is calls left, `t` is seconds to reset). Lower `--limit` or call less often.
- **Nothing is reported although you know a model is new.** The model may be older than `--days`, may be tagged as built on another author's model, or may already be in `seen.json`. Delete `seen.json` to start again.
- **`ModuleNotFoundError: filters` when running the tests.** Run the command from the project folder, with `-t .`.

## Frequently asked questions

**How do I find new open models for a hackathon?**

Watch named publishers through the public Hugging Face models API, newest first. On 10 November 2026 the four organisations in the tutorial gave 10 models within a 45-day range.

**Can I use the Hugging Face API without a token?**

Yes, for public models. The calls in this tutorial used no token and no account. The API reports how many calls you have left in a `ratelimit` header, and 458 were left at the end of the run.

**How do I avoid copies and fine-tunes in a model list?**

Drop a model when its `base_model` tag points to another author. For `unsloth` over 14 days, 4 models were in range and 3 were dropped. The rule has a gap: a re-upload with no `base_model` tag passes through.

## What to try next

- Add `--skip-own-variants` for your own organisation's GGUF and FP8 uploads, using the relation in the tag (`quantized`, `adapter`).
- Add a `--json` option that writes each message as one JSON line, for other programs to read.
- Keep a count per day in `seen.json` and print a weekly summary.

## How this tutorial was tested

The code on this page is copied from the project files by a script, and every output and image comes from a real run on 10 November 2026 on macOS with Python 3.14. All steps ran from a clean state and were replayed from an empty copy of the folder. The API calls were real. They used no key and no account.

The screenshots of terminal steps are rendered from the saved output of each command. They are not captures of a terminal window, because this Mac blocks desktop screen capture for this tool.

Not run: Windows and Linux, the chat webhook, `cron` and `launchd`. Results change with the date and with what publishers upload. Model names and licences in the screenshots belong to their publishers and come from the Hub's public API.
