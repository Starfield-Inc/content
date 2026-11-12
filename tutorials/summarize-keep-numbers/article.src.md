---
title: "Summarise a Long Article with an LLM and Keep the Numbers"
seo_title: "Summarise Long Texts Keeping Numbers: AI Hackathons"
meta_description: "Summarise long articles in an AI hackathon project without losing numbers. Split the text, merge summaries and check that every number survived."
description: "Summarise long articles in an AI hackathon project without losing numbers. Split the text, merge summaries and check that every number survived."
---

# Summarise a long article with an LLM without losing the numbers

You build a Python script that splits a long text into chunks, summarises each chunk, merges the results, and then lists every number from the source that the summary dropped or changed.

**Time:** about 40 minutes. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, and an Anthropic API key. **Tested:** 11 November 2026 with Python 3.14.6 and the `anthropic` package 2.8.0 on macOS.

Model replies differ from run to run. Your counts of kept and missing numbers will not match the output below. The shape of the output will.

A summary that changes a number is a risk in any AI hackathon demo, and a simple check can catch it. If you are planning a project, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A summary is short on purpose, so it leaves things out. For prose that is the point. For a report full of figures, a missing or altered figure can change the meaning, and the text still reads well. You cannot see the gap by reading the summary alone. A program can: pull the numbers out of the source, pull the numbers out of the summary, and compare the two lists.

## See it running first

This is the finished script summarising a made-up annual report with 72 distinct numbers. The summary is followed by a check that lists the numbers it did not keep.

{{shot:07-summarize|Terminal output of summarize.py: a four-paragraph summary followed by counts of kept and missing numbers}}

The rest of the tutorial builds it from nothing.

## Step 1: Set up the project

Create a virtual environment. The commands from here on assume it is active (`source .venv/bin/activate`).

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt` with one line:

{{file:requirements.txt}}

{{cmd:02-install}}

{{out:02-install}}

Put your key in a file named `.env`. Copy the placeholder file and edit it:

{{file:.env.example}}

Never paste a real key into code, a screenshot or a chat. Load the file into your terminal session on macOS or Linux:

```bash
set -a; source .env; set +a
```

## Step 2: Write a source text with many numbers

The tutorial uses `report.txt`, an annual report for a ferry cooperative. The cooperative and every figure in it are made up for this tutorial. It has dates, percentages, decimals, numbers with commas and numbers in the millions. Use your own text if you prefer. The checker only needs plain text.

You can read the whole file in the project folder. It is 3,356 characters long.

## Step 3: Extract the numbers

The checker is the part that does not depend on a model, so build and test it first. A number here is a run of digits with optional commas and an optional decimal part. `numcheck.py` removes the commas, so `1,284,500` and `1284500` count as the same number. It also drops trailing zeros after a decimal point, so `7.0` and `7` match. It skips a number that follows a letter or a dot, such as the 3 in `Q3`, because that digit is part of a name.

{{file:numcheck.py}}

Run it on the report:

{{cmd:03-extract}}

{{shot:03-extract|Terminal output of numcheck.py listing 72 distinct numbers from report.txt}}

The report holds 72 distinct numbers. Note the word "distinct": the script compares sets, so a number that appears three times counts once. A summary that keeps one of three mentions of 2025 passes for that number.

## Step 4: Compare against a summary you wrote

Before you involve a model, test the comparison on a summary with known faults. `bad_summary.txt` is a short summary written by hand. It rounds 1,284,500 to "about 1.3 million" and it says emissions fell to 7,900 tonnes, where the report says 7,800.

{{cmd:04-compare-fixed}}

{{shot:04-compare-fixed|Terminal output of numcheck.py: 8 numbers kept, 64 missing, and 7900 reported as not in the source}}

The checker reports 8 kept and 64 missing. It also reports `7900` under "In summary but not in source". That line is the one that catches a changed number: the changed figure shows up as new, and the original shows up as missing. A rounded figure is reported the same way, because "1.3 million" is not "1,284,500". Whether a rounded number is a fault is your call. The checker only shows the difference.

## Step 5: Split the text into chunks

A text that is longer than the model's input limit cannot go in one call, and a long input in a single call can also lose detail. The usual fix is to split it, summarise each part, then merge the parts. `chunks.py` splits on blank lines and packs whole paragraphs into chunks of up to a set size. It never cuts inside a paragraph, because a cut can separate a number from the words that explain it.

{{file:chunks.py}}

{{cmd:05-split}}

{{shot:05-split|Terminal output of chunks.py: 3356 characters split into 4 chunks}}

The report is 3,356 characters, and with a limit of 900 characters it comes out as 4 chunks. This report is short enough to fit in one call, so the chunk size here is set small to show the method. This tutorial did not test a text that is longer than a model's input limit.

## Step 6: Summarise, merge and check

`summarize.py` asks for a summary of each chunk in at most 60 words, joins those summaries, and asks for one merged summary. Both prompts carry the same rule: keep every number exactly as written, and do not round, convert or recompute. Then it runs the checker from Step 3 on the source and the merged summary.

{{file:summarize.py}}

First, see what a missing key looks like. Run the script in a terminal where the variable is not set:

{{cmd:06-no-key}}

{{shot:06-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

Now run it with the key loaded:

{{cmd:07-summarize}}

{{out:07-summarize}}

The summary has 163 words and keeps 35 of the 72 numbers. 37 are missing and none are invented. Look at the list of missing numbers. It includes the 4 from "4 routes" in the source, and the 2027 date for the new vessel. The model did what the prompt asked for the numbers it kept: the checker found no changed figure in this run. It did not keep everything, and the prompt asking it to do so did not change that.

## Step 7: Ask for a shorter summary

A shorter limit leaves less room for numbers. Run the same script with a limit of 50 words and compare:

{{cmd:08-short}}

{{shot:08-short|Terminal output of summarize.py with a 50-word limit: 12 numbers kept and 60 missing}}

The summary has 55 words and keeps 12 numbers. 60 are missing. In the replay the counts moved the other way (see the tested note), so treat any one run as a sample, not a rule. The model also wrote "four routes" with a word, so the source's 4 counts as missing even though the fact survived. That is a limit of the checker: it reads digits, not number words. It would also flag "1.3 million euros" if the source said "1,300,000 euros".

The word limit was 50 and the summary has 55 words. The model did not hold to the limit exactly in this run, so check the length yourself if it matters.

## Step 8: What a mistake looks like

Give the checker a file name that does not exist:

{{cmd:09-missing-file}}

{{shot:09-missing-file|Terminal output: Cannot find notes.txt}}

The script stops with a one-line message and a non-zero exit code, so a calling script can tell it failed.

## Troubleshooting

- **The summary says it cannot see any text, and the check reports every number missing.** This happened while building this tutorial. The model was called with a `max_tokens` of 600, and the reply held a thinking block and no text, with stop reason `max_tokens`. The checker then reported 0 kept numbers, which looked like a bad summary but was an empty one. The script now passes `thinking={"type": "disabled"}` and exits with a message if a reply has no text. I tested that this fixes the run. I did not test other models.
- **`ImportError` or odd errors after you name a file `numbers.py`.** `numbers` is the name of a module in Python's standard library. A file with that name in your project can replace it. This tutorial's checker is called `numcheck.py` for that reason.
- **`ANTHROPIC_API_KEY is not set`.** The variable is not in the terminal you are running from. Run `set -a; source .env; set +a` in that terminal again.
- **A number shows as missing but is in the summary.** Check the form. The checker does not read number words, and it does not convert "1.3 million" into 1300000.

## Frequently asked questions

**Why do LLM summaries change numbers?**

A summary is short, so the model chooses what to keep, and it may round or write a figure another way. In the runs for this tutorial the merged summary kept 35 of 72 numbers at 163 words and 12 at 55 words. No number was changed in those runs, and the hand-written summary showed what a change looks like to the checker.

**How do I summarise a text longer than the context window?**

Split it on paragraph breaks into chunks, summarise each chunk, and merge the chunk summaries with one more call. `chunks.py` and `summarize.py` do this. The report here was short enough for one call, so the chunking was shown but a text over the limit was not tested.

**How do I check a summary automatically?**

Extract the numbers from the source and the summary with a regular expression, and compare the two sets. `numcheck.py` reports numbers kept, numbers missing, and numbers in the summary that are not in the source. It does not read number words or convert units.

## What to try next

- Send the missing numbers back to the model and ask it to add the important ones, then run the check again.
- Compare numbers with their unit or label, so that a figure moved to the wrong sentence is caught.
- Handle number words such as "four" and forms such as "1.3 million".

## How this tutorial was tested

- Date: 11 November 2026. Python 3.14.6, `anthropic` 2.8.0, macOS. The model is `claude-haiku-5-5`, set in the `MODEL` constant.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. Model summaries differed between the two runs, as expected: in the replay the default run kept 14 numbers and the 50-word run kept 30, where the numbers above are from the saved evidence run.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run: Windows, Linux, Python versions other than 3.14.6, a text longer than a model's input limit, and models other than `claude-haiku-5-5`.
