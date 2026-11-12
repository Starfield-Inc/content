---
title: "Test Your Prompts: An AI Hackathon Tutorial"
description: "An AI hackathon tutorial on prompt tests: five prompts, rule-based checks and one change that breaks a test, so you catch problems before demo day."
---

# Write prompts as tests: build a tiny prompt test file

You will build a test file that sends five prompts to the Claude API and checks each answer by rule: expected facts, format and length. Then you will change one prompt and watch a check fail. It takes about 30 minutes.

**Level:** Intermediate. **You need:** Python 3.10 or newer, a terminal, and an Anthropic API key. **Tested:** 10 November 2026 on macOS with Python 3.14.6 and `anthropic` 2.7.0, using the model `claude-haiku-5-5`. The Windows commands were not run.

A prompt change at midnight can break a demo in an AI hackathon, and a small test file shows what it broke. See the [upcoming AI hackathons](/ai-hackathons/) for a place to use it.

## Why treat a prompt like code

When you edit a function, a test tells you what the edit broke. A prompt has no such safety net by default. You change a word, the answer to one question looks fine, and a different question quietly gets worse. A small file of prompts with checks gives you the same signal: run it before and after a change and read what failed.

The checks here are rules, not opinions. A rule can say that the answer must name Canberra, must be valid JSON, or must be shorter than 20 words. Rules cannot judge tone or quality. They catch the failures that are easy to define.

## See it running first

By the end you will run the tests against a changed prompt and see this:

{{shot:06-fail|Test output where four tests pass and the summary test fails its word-count check}}

Four tests pass and one check fails, and the failure message says which check and why. Model output varies between runs, so the exact numbers on your machine may differ. The rest of this tutorial builds the file from scratch.

## Step 1. Create a virtual environment

A virtual environment keeps this project's packages apart from the rest of your machine. Make a folder, open a terminal in it, and run:

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Activate it. On macOS and Linux use `source .venv/bin/activate`. On Windows use `.venv\Scripts\activate`. Every command below assumes the environment is active.

## Step 2. Install the SDK and set your key

The only package is the official Anthropic Python SDK. The tests use `unittest`, which comes with Python.

{{file:requirements.txt}}

{{cmd:02-install}}

{{shot:02-install|Terminal after installing the anthropic package, showing the name and version}}

Create a file named `.env` in the project folder with your own key, or export the variable in your terminal. Never paste a key into code. The project ships a `.env.example` that shows the format:

{{file:.env.example}}

## Step 3. Write a helper that sends a prompt

`llm.py` sends one prompt and returns the text. It keeps the model name in a `MODEL` constant and sets `max_tokens` to 300 so a long answer cannot run up the bill. It turns thinking off with `thinking={"type": "disabled"}` so the answers are plain text. After every call it writes a line to `spend.log` with the input and output tokens from the response's `usage` field.

{{file:llm.py}}

## Step 4. List the prompts

Each prompt asks for something you can check by rule. Keeping the prompts in their own file means the tests can load a changed copy later without touching the test code. The prompts ask for a one-word answer, a JSON object, three lines, a short summary and a bare number.

{{file:prompts.py}}

Send one of them to see the raw answer:

{{file:ask.py}}

{{cmd:03-ask}}

{{shot:03-ask|Terminal showing the capital prompt and the answer Canberra}}

## Step 5. Write the checks

Each test sends one prompt and then checks the answer by rule. There are three kinds of rule here:

- **Expected facts.** The answer to the capital prompt must contain "canberra". The JSON must have symbol `Au` and number `79`. The list must mention red, green and blue.
- **Format.** The JSON prompt must return something `json.loads` accepts. The list must have exactly three non-empty lines. The minutes prompt must return exactly `180`.
- **Length.** The capital answer must be at most three words. The summary must be under 20 words.

Tests that check several things use `subTest`, so one failed check does not hide the others, and every assertion carries the model's answer in its failure message. The file reads the prompts from the module named in the `PROMPTS_MODULE` variable, and uses `prompts` when it is not set.

{{file:test_prompts.py}}

## Step 6. Run the five tests

{{cmd:04-pass}}

{{shot:04-pass|Test output showing five tests passing}}

All five tests passed in this run, so each answer met its rules. Each run makes five API calls, one per prompt.

## Step 7. Change one prompt

Now change one thing and run the same tests. `prompts_changed.py` is a copy of `prompts.py` where the summary prompt no longer asks for a short answer. This is the whole change:

{{cmd:05-diff}}

{{shot:05-diff|Output of diff showing the summary prompt changed from a one-sentence request to explain in detail}}

The first difference is only the file's comment. The second is the prompt: "Summarise this in one sentence of fewer than 20 words" became "Explain this in detail".

## Step 8. Watch the check fail

Run the tests again with `PROMPTS_MODULE` pointing at the changed file. The output goes through a filter that removes the folder path from the traceback, so the image shows `test_prompts.py` and not where the project lives on this machine.

{{cmd:06-fail}}

{{shot:06-fail|Test output where four tests pass and the summary test fails its word-count check}}

{{out:06-fail}}

Four tests still passed. The summary test failed the check named "under 20 words", and the message says the answer had 134 words. The checks for the facts, light and sugar or glucose, did not fail on this run. That is what a test is for: it tells you which rule broke, not just that something did. A failing length check after you removed the length instruction is the expected result, and the test would also catch the same failure if the change had been an accident.

## Step 9. What a missing key looks like

If no key is set, the test file stops when it loads and says why. Here the step runs without a key on purpose:

{{cmd:07-no-key}}

{{shot:07-no-key|Terminal showing the message that ANTHROPIC_API_KEY is not set}}

The exit code is 2. Create the `.env` file or export the variable in the same terminal you run the tests from.

## Step 10. Check what it cost

`spend.py` adds up `spend.log` and turns the totals into a dollar estimate with the prices for this model, which were 0.10 dollars per million input tokens and 0.50 dollars per million output tokens when this was tested. Check the provider's price page for current prices.

{{file:spend.py}}

{{cmd:08-spend}}

{{shot:08-spend|Terminal showing the number of calls, the token totals and the estimated cost}}

This run made 11 calls: one for `ask.py`, five for the passing run and five for the changed run.

## Troubleshooting

**"ANTHROPIC_API_KEY is not set".** Add the key to `.env` in the folder you run the tests from, or export it in the same terminal.

**A test fails on a prompt you did not change.** Model output varies between runs. A check that depends on exact wording, such as "the answer must be exactly 180", can fail when the model adds a full stop or a word. Read the answer in the failure message, then decide whether the prompt or the rule needs to change.

**The JSON test fails.** The model may wrap the JSON in a code fence or add a sentence. Ask for JSON only in the prompt, as `prompts.py` does, and keep the test strict so that a change in format shows up.

## Frequently asked questions

**How do I test a prompt automatically?**

Send each prompt to the model and check the answer by rule: expected facts, format and length. Here all five tests passed, and after one prompt was changed, the check "under 20 words" failed because the answer had 134 words.

**Can I test model output when it changes every run?**

Rules still work when the wording changes, but a rule that needs exact text can fail. The check for exactly `180` can fail if the model adds a full stop. Running each prompt three times was not tested here.

**How many prompt tests are enough for a hackathon?**

Not tested here. This tutorial used five prompts, each with its own rule. The right number depends on your project.

## What to try next

- Add a sixth prompt for something your own project needs, with one fact check and one length check.
- Run each prompt three times and fail the test only if two out of three runs break a rule.
- Keep `spend.log` open while you work and set yourself a call budget before a long session.

## How this tutorial was tested

The tutorial was run on 10 November 2026 on macOS with Python 3.14.6, `anthropic` 2.7.0 and the model `claude-haiku-5-5`. The code blocks are copied from the project files, and the output blocks are the saved output of the real run. The steps were replayed from an empty copy of the folder. Screenshots are terminal-style images rendered from the saved output of each command. They are not captures of a terminal window. Not run: Windows and Linux, and any model other than `claude-haiku-5-5`.
