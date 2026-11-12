---
title: "Count Tokens and Estimate Costs for AI Hackathon Projects"
description: "Count tokens and estimate cost before your AI hackathon demo runs. Build a small Python tool with two encodings and see why text size changes cost."
---

# Count tokens in your text with a tokenizer library

You will build a small Python tool that counts the tokens in a text file and turns the count into a cost estimate. It takes about 20 minutes and needs no API key.

**Level:** Beginner. **You need:** Python 3.10 or newer and a terminal. **Tested:** 10 November 2026 on macOS with Python 3.14 and `tiktoken` 0.14.0. The Windows command is from the Python docs and was not run.

In an AI hackathon you may have limited credits, so knowing how many tokens a prompt uses tells you what you can afford. Once you can count them, see the [upcoming AI hackathons](/ai-hackathons/) and plan your budget.

## Why count tokens

A language model does not read words. It reads tokens, which are pieces of text. A short, common word is often one token. A long or rare word is split into several. Providers set limits and prices by the token, so knowing the count before you send text tells you whether it fits and roughly what it will cost.

## See it running first

By the end you will run one command and get this:

{{shot:05-cost|The finished tool printing a token count and a cost for two encodings}}

The cost column comes from a price you type in. The rest of this tutorial builds the tool from scratch.

## Step 1. Create a project folder and a virtual environment

A virtual environment keeps this project's packages apart from the rest of your machine. Make a folder, open a terminal in it, and run:

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Then activate it. On macOS and Linux use `source .venv/bin/activate`. On Windows use `.venv\Scripts\activate`. Every command below assumes the environment is active.

## Step 2. Install tiktoken

`tiktoken` is a tokenizer library published by OpenAI. It turns text into token numbers on your own machine, so it needs no API key. List it in `requirements.txt` so anyone can install the same thing:

{{file:requirements.txt}}

Install it:

{{cmd:02-install}}

{{shot:02-install|Terminal after installing tiktoken, showing the package name and version}}

The first time you count tokens, `tiktoken` downloads the encoding data it needs, so the first run needs an internet connection.

## Step 3. See one sentence split into tokens

Before counting a whole file, look at how a single sentence breaks up. This script encodes a sentence, then decodes each token number back to its text piece. It uses the `cl100k_base` encoding, one of the encodings `tiktoken` ships.

{{file:tokens_demo.py}}

Run it:

{{cmd:03-split}}

{{shot:03-split|Seven words split into eight tokens, with each token number and its text}}

The sentence has 7 words and 8 tokens. Each word became one token, and the full stop became its own. The space before a word is part of that word's token, which is why each piece starts with a space. Words and tokens are close here, but they are not the same thing.

## Step 4. Count the tokens in a file

Now count a whole file. This script takes a path, reads the file and counts tokens for two encodings. Models from different generations use different encodings, so the counts can differ. The script prints a friendly message and exits with code 2 if the file is missing, which Step 7 shows.

{{file:count_tokens.py}}

You also need some text to count. Save this as `sample.txt`, or use your own notes:

{{file:sample.txt}}

Run the counter:

{{cmd:04-count}}

{{shot:04-count|Characters, words and token counts for sample.txt in two encodings}}

The sample has 613 characters and 119 words. Both encodings count 136 tokens. That is more tokens than words, because longer words and punctuation take extra tokens.

## Step 5. Turn the count into a cost estimate

Providers price input by the million tokens. Pass the price with `--price-per-million`. Copy the real number from your provider's price page on the day you run it, because prices change. The `3.00` below is an example, not a real price.

{{cmd:05-cost}}

{{shot:05-cost|Token counts with a cost column based on an example price of 3 dollars per million tokens}}

At that example price, this file costs about $0.0004 to send once. Small files cost very little. The numbers matter when you send many requests, or very large documents.

## Step 6. Count a text in two languages

The two encodings agree on plain English. They can disagree on other text. Save this line as `multilingual.txt`:

{{file:multilingual.txt}}

{{cmd:05b-languages}}

{{shot:05b-languages|A Russian and Chinese sentence needs 24 tokens in one encoding and 13 in the other}}

The same 36 characters need 24 tokens with `cl100k_base` and 13 with `o200k_base`. The newer encoding splits this text into fewer pieces. If you build for users who write in other languages, count with the encoding that matches your model.

## Step 7. Check what a mistake looks like

Run the counter on a file that does not exist:

{{cmd:06-missing}}

{{shot:06-missing|The friendly error message for a missing file}}

You get a clear message instead of a long error trace. The command ends with exit code 2, so a script or a scheduler can tell that it failed.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'tiktoken'`.** The virtual environment is not active, or the install did not finish. Activate it and run `pip install -r requirements.txt` again.
- **The first run is slow or fails with a network error.** `tiktoken` downloads encoding data on first use. Check your connection and run it again.
- **Your count differs from a provider's own number.** Tokenizers differ between model families. Use the tokenizer that matches your model, and treat this tool's number as an estimate.

## Frequently asked questions

**What is a token in an AI hackathon project?**

A token is a piece of text that a model reads. A short, common word is often one token, and a long or rare word is split into several. In the test, a sentence of 7 words became 8 tokens.

**How do I estimate API cost before a hackathon demo?**

Count the tokens with `tiktoken`, then multiply by your provider's price per million tokens. The 136-token sample file cost about $0.0004 at an example price of $3.00 per million. That price is an example, so copy the real one from your provider's price page.

**Why do different models count different numbers of tokens?**

Models use different encodings. The same 36-character Russian and Chinese line needed 24 tokens with `cl100k_base` and 13 with `o200k_base`. Count with the encoding that matches your model.

## What to try next

- Count a longer document and watch the cost estimate grow.
- Add a third encoding to the `ENCODINGS` list and compare.
- Read the whole folder instead of one file.

## How this tutorial was tested

Every command and every screenshot above comes from one real run on 10 November 2026. The code in the blocks is copied from the project files, not retyped. The steps were then run again from an empty folder, and all of them passed. The screenshots show the saved output of those commands in a terminal-style frame.
