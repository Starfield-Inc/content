---
title: "Build a Summariser Command-Line Tool in Python with Claude"
seo_title: "Python Summariser CLI with Claude for AI Hackathons"
meta_description: "Build a Python command-line summariser for your AI hackathon project: bullet summary, headline, chosen length, chunking for long text and an input guard."
description: "Build a Python command-line summariser for your AI hackathon project: bullet summary, headline, chosen length, chunking for long text and an input guard."
---

# Build a summariser command-line tool in Python with Claude

You build a small Python command that reads a text file or pasted text and prints a one-line headline and a bullet summary. You choose how long the summary is, and the tool refuses input that is too large.

**Time:** about 30 minutes. **Level:** beginner. **You need:** Python 3.10 or newer, basic comfort with a terminal, and an Anthropic API key. **Tested:** 12 November 2026 with Python 3.14.6 and the `anthropic` package 2.8.0 on macOS.

Model replies differ from run to run. Your wording will not match the output below. The shape of the output will.

A summariser is one of the quickest useful features to add to an AI hackathon project, and a command-line version is easy to test and reuse. If you are looking for a place to use it, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

Most text you want to summarise is longer than you want to read, and sometimes longer than you want to pay to send. Three small decisions make a summariser usable: how long the result should be, what to do when the text is long, and when to say no. This tutorial makes each one a plain piece of code you can read.

## See it running first

This is the finished tool summarising a made-up news item of about 3,400 characters. It splits the text, collects notes on each part, then writes one headline and eight bullets.

{{shot:09-long-text|Terminal output of summarize.py on long.txt: three parts done, then a headline and eight bullet points}}

The rest of the tutorial builds it from nothing.

## Step 1: Set up the project

Create a virtual environment. The commands from here on assume it is active (`source .venv/bin/activate`).

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt` with one line:

{{file:requirements.txt}}

{{cmd:02-install}}

{{shot:02-install|Terminal: the last lines of pip install, ending with Successfully installed}}

Check the version that was installed:

{{cmd:02b-version}}

{{shot:02b-version|Terminal: pip show prints the anthropic package name and version}}

Put your key in a file named `.env`. Copy the placeholder file and edit it:

{{file:.env.example}}

Never paste a real key into code, a screenshot or a chat. Load the file into your terminal session on macOS or Linux:

```bash
set -a; source .env; set +a
```

## Step 2: The text to summarise

The project has two made-up texts, written for this tutorial. `article.txt` is a news item about a library reopening, 1,121 characters long. `long.txt` is a longer item about a town changing its buses, 3,384 characters long. Any plain text file works.

## Step 3: The whole tool

`summarize.py` has four jobs. It reads the input from a file, or from standard input when you pass `-`. It checks the size before it does anything that costs money. It splits long text into parts. It asks the model for a headline and a fixed number of bullets.

Length is a word you choose: `short` gives 3 bullets, `medium` gives 5 and `long` gives 8. The tool puts the number in the prompt. A bullet count is easier to check than a word count, and it is easy to read at a glance.

{{file:summarize.py}}

Two details are worth noting. The model is called with thinking turned off. With thinking on, a small `max_tokens` can be used up before any text appears, and the reply comes back empty (see Troubleshooting). The `anthropic` import sits after the guards, so a refused or empty input fails fast.

## Step 4: See how the text will be split, for free

The `--dry-run` flag reports how the text would be split and sends nothing. It needs no key. Run it on the short text:

{{cmd:03-dry-short}}

{{shot:03-dry-short|Terminal output: 1121 characters, 1 part, nothing was sent}}

It is 1 part. Now the longer text:

{{cmd:04-dry-long}}

{{shot:04-dry-long|Terminal output: 3384 characters, 3 parts, nothing was sent}}

The split is on blank lines. Whole paragraphs are packed into parts of up to 1,500 characters, and a paragraph is only cut if it is longer than that by itself. The 3,384 characters here came out as 3 parts. The number comes from the dry run, not from a model, so it will be the same for you.

## Step 5: The input-size guard

A tool that accepts anything can send a very large file by mistake. `--max-input` sets a limit in characters, and the default is 20,000. The check happens before the key is read and before any call. Lower the limit to see it work:

{{cmd:05-too-big}}

{{shot:05-too-big|Terminal output: input is 3384 characters, over the limit of 2000, nothing was sent}}

The message gives both numbers and says nothing was sent. The exit code is 1, so a script that calls the tool can tell it stopped. The limit counts characters, not tokens. It is a rough guard against accidents, not a cost cap. The 20,000 default is a choice for this tutorial, not a model limit.

## Step 6: What a missing key looks like

Run the tool in a terminal where the key is not set:

{{cmd:06-no-key}}

{{shot:06-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

## Step 7: Summarise a file

Load your key and run the tool on the short text. The default length is `medium`:

{{cmd:07-summarize}}

{{shot:07-summarize|Terminal output of summarize.py on article.txt: a headline, five bullet points and the call count}}

The headline comes first, then 5 bullets. The last line is for you: how many characters went into the final call, how many parts there were, and how many model calls the run made. A short text is 1 call.

## Step 8: Choose a shorter length

{{cmd:08-short}}

{{shot:08-short|Terminal output of summarize.py with the short length: a headline and three bullet points}}

Same text, 3 bullets. The model picks which facts to keep, so the three bullets are not the first three of the longer list.

## Step 9: A text that needs chunks

The long text is 3 parts, so the tool does something different. It asks for the 3 main facts in each part, joins those notes, and asks for the headline and bullets from the notes. That is 3 calls for notes and 1 for the summary.

{{cmd:09-long-text}}

{{out:09-long-text}}

The run made 4 model calls, and the final call received 1,723 characters of notes instead of 3,384 characters of text. The size of each call stays small however long the input is, up to the guard. The cost is detail: the summary is built from notes, not from the original wording. Something a note did not mention cannot appear in the summary. This tutorial did not test a text near the 20,000-character default limit.

## Step 10: Summarise pasted text

Pass `-` instead of a file name and the tool reads standard input. That works with a pipe, or you can type text and press Ctrl-D on macOS and Linux.

{{cmd:10-pasted}}

{{shot:10-pasted|Terminal output of summarize.py reading piped text: a headline and three bullets about a pool closing}}

## Step 11: What a mistake looks like

Name a file that does not exist:

{{cmd:11-missing-file}}

{{shot:11-missing-file|Terminal output: Cannot find notes.txt}}

The tool stops with one line and a non-zero exit code.

## Troubleshooting

- **The tool prints "The model returned no text (stop reason: max_tokens)".** This happened while building this tutorial, on the first run of the long text. With thinking left on, the reply budget was spent before any text. The script now turns thinking off and uses a `max_tokens` of 600. I tested that this fixes the run on `claude-haiku-5-5`. I did not test other models.
- **`ANTHROPIC_API_KEY is not set`.** The variable is not in the terminal you are running from. Run `set -a; source .env; set +a` in that terminal again.
- **The number of bullets is not what you asked for.** The model follows the count in the prompt closely but nothing enforces it. If it matters, count the lines that start with `- ` and ask again.
- **A fact is missing from the summary of a long text.** Chunked summaries are built from notes, so a fact that no note kept is gone. Raise the notes from 3 facts per part to more.

## Frequently asked questions

**How do I control the length of an LLM summary?**

Put a count in the prompt. This tool maps `short`, `medium` and `long` to 3, 5 and 8 bullets, and the model followed those counts in the runs for this tutorial.

**How do I summarise a text that is too long for one call?**

Split it on paragraph breaks, take notes on each part, then summarise the notes. For the 3,384-character example that was 3 note calls and 1 summary call.

**How do I stop a command-line tool from sending huge files?**

Check the size before the API call and exit with a clear message. `--max-input` does this in characters, and the check runs before the key is even read.

## What to try next

- Read a whole folder of `.txt` files and write each summary to its own file.
- Add a `--language` option and ask for the summary in another language.
- Count tokens before sending, so the guard measures what you pay for.

## How this tutorial was tested

- Date: 12 November 2026. Python 3.14.6, `anthropic` 2.8.0, macOS. The model is `claude-haiku-5-5`, set in the `MODEL` constant.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls.
- Every step was run from a clean folder, then replayed from an empty copy with no virtual environment. The replay passed. Model wording differed between the two runs, as expected. The character counts and part counts did not.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run: Windows, Linux, Python versions other than 3.14.6, input near the 20,000-character default limit, texts other than the two made-up examples, and models other than `claude-haiku-5-5`.
