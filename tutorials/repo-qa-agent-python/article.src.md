---
title: "Build a Read-Only Agent for an AI Hackathon"
seo_title: "Build a Read-Only Agent for an AI Hackathon"
description: "AI hackathon agent guide: answer questions about a GitHub repo. Give it read tools, answer with file paths and limit what it can read."
meta_description: "AI hackathon agent guide: answer questions about a GitHub repo. Give it read tools, answer with file paths and limit what it can read."
---

# Build an agent that answers questions about a code repo in Python

You build an agent that reads files from a small code repository and answers questions about it with file names. It has three read-only tools. Every path it asks for is checked against one folder, and a request to read outside that folder is refused by your code.

**Time:** about 45 minutes. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, and an Anthropic API key. **Tested:** 11 November 2026 with Python 3.14.6 and the `anthropic` package 2.8.0 on macOS.

Model replies differ from run to run. Your wording, and which tools the agent calls first, will not match the output below exactly. The shape of the output will.

Agents are popular in AI hackathons, and an agent that can only read is a safe place to start. If you plan to build one, see the [upcoming AI hackathons](/ai-hackathons/). The project here uses a small repo that lives inside the tutorial folder, so you need no GitHub login or token. The same code works on a folder you cloned yourself.

## Why this matters

An agent is a loop. The model asks for a tool, your code runs it and sends the result back, and the model decides what to do next. The model never touches your disk. Your code does, so your code decides what is allowed. This tutorial gives the agent a read tool and then limits it, because the limit is the part that is easy to get wrong.

## See it running first

This is the finished agent answering a question about a sample repo. It lists and reads files, then names the file that holds the answer.

{{shot:07-ask-files|Terminal output of agent.py: four tool calls, then an answer that names shelf/storage.py}}

The rest of the tutorial builds it from nothing.

## Step 1: Set up the project

Make a folder, create a virtual environment and activate it. The commands from here on assume it is active.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt` with one line:

{{file:requirements.txt}}

Install it. The output below shows the version used for this tutorial.

{{cmd:02-install}}

{{shot:02-install|Terminal output of pip: the anthropic package, version 2.8.0}}

Put your key in a `.env` file. Copy the placeholder file and edit it. Never paste a real key into code or a screenshot.

{{file:.env.example}}

Load it into your terminal session (macOS and Linux) with `set -a; source .env; set +a`.

## Step 2: Write a tiny repo to ask about

The agent needs something to read. `sample_repo/` is a small library called `shelf` that keeps a reading list in a JSON file. It is written for this tutorial, so there is no third-party code in it. It has six files:

{{file:sample_repo/shelf/storage.py}}

{{file:sample_repo/shelf/books.py}}

The other four files are `README.md`, `shelf/__init__.py`, `shelf/cli.py` and `tests/test_books.py`. There is also a folder next to the repo, `private/`, with a file called `notes.txt`. It is outside the repo on purpose. It stands for anything on your machine the agent should not see.

## Step 3: Give the agent read tools

`repo_tools.py` holds three tools: `list_files`, `read_file` and `search_text`. All of them are read-only. None can write, delete or run anything.

The check that matters is `_safe`. It joins the requested path to the repo folder, resolves it (that follows `..` and symlinks), and refuses the result if it is not inside the folder. `list_files` and `search_text` skip files whose real location is outside the folder too. The tool returns the refusal as text, so the model can read it and explain.

{{file:repo_tools.py}}

Before any model is involved, try the tools by hand. `check_tools.py` calls them directly, including four read requests, three of which should be refused:

{{cmd:03-tools}}

{{shot:03-tools|Terminal output of check_tools.py: the file list, a search result, README.md read, and three refused paths}}

The file list has six files. The search finds `MAX_TITLE_LENGTH` on lines 3 and 9 of `shelf/books.py`. `README.md` is read. A parent-folder path, an absolute path and a path that goes into `shelf/` and back out are all refused.

## Step 4: Test that the sandbox holds

A check you only tried by hand is a check you will break later. `test_sandbox.py` has five tests. Two of them cover cases a short check often misses: a symlink inside the repo that points outside it, and a sibling folder whose name starts with the repo's name (`repo-private` next to `repo`). Comparing path text with `startswith` lets that second one through. `is_relative_to` does not.

{{file:test_sandbox.py}}

{{cmd:04-sandbox-tests}}

{{shot:04-sandbox-tests|Terminal output of the five sandbox tests, all ok}}

All five pass.

## Step 5: Write the agent loop

`agent.py` sends the question and the tool definitions. While the reply asks for a tool (`stop_reason` is `tool_use`), it runs each tool, sends the results back and asks again. It stops when the model answers, or after `MAX_TURNS` rounds so a confused model cannot loop forever. Each tool call is printed, so you can see what the agent looked at.

The system prompt asks the agent to name file paths, so the answers point to files. It also has a sentence that tells the agent it can only read inside the repo. Step 7 removes that sentence on purpose.

{{file:agent.py}}

Run it without a key first, to see the message:

{{cmd:05-no-key}}

{{shot:05-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

## Step 6: Ask a question and get file names

Ask where a rule lives:

{{cmd:06-ask-search}}

{{shot:06-ask-search|Terminal output: the agent searches, lists files, and answers that MAX_TITLE_LENGTH is 80 in shelf/books.py}}

The agent made two tool calls and answered with `shelf/books.py`, the constant name and the limit of 80. The first search for `title` matched the README, which is not where the rule is. The agent then listed the files and answered. Each printed tool line shows only the first line of the result, cut to 70 characters.

Ask a question that needs more than one file:

{{cmd:07-ask-files}}

{{out:07-ask-files}}

The agent listed the files, searched for `json`, then read `shelf/storage.py` and `shelf/books.py`. That is four tool calls. It named `shelf/storage.py` as the file to change. Check the line numbers it quotes against the files. Models can get a line number wrong, and this tutorial does not test for that.

## Step 7: Ask it to read outside the folder

This is the step to read twice. Ask for the private file:

{{cmd:08-outside}}

{{shot:08-outside|Terminal output: the agent says it cannot read ../private/notes.txt because it is outside the repo folder}}

The agent refused. In this run it refused without calling a tool at all, because the system prompt told it the rule. That is the model following instructions. It is not a safety control. Prompts get ignored, argued around or injected by text inside the files the agent reads.

To see what your code does by itself, run the same request with `--no-guard`, which removes that one sentence from the system prompt:

{{cmd:09-outside-no-guard}}

{{shot:09-outside-no-guard|Terminal output: the agent calls read_file on ../private/notes.txt and the tool returns refused}}

This time the agent tried. The line starting `[tool] read_file` shows the request, and the result is `refused: ... is outside the repo folder`. The code stopped it. The run also checked that the code word stored in `private/notes.txt` did not appear anywhere in the output. Keep the check in code, and treat the prompt as a hint to the model.

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set`.** The variable is not in the terminal you are running from. Load `.env` again in that terminal.
- **The agent stops with `[stopped: too many tool calls]`.** It used all eight rounds. Raise `MAX_TURNS`, or ask a narrower question.
- **A file is cut off.** `read_file` returns at most 4000 characters and adds `[truncated]`. Raise `MAX_FILE_CHARS` for longer files.
- **A reply has no text.** A reply can hold blocks that are not text, such as a thinking block, and a low `max_tokens` can cut the text off. `text_of` joins only the text blocks. `MAX_TOKENS` is 2000 here.
- **The agent cites the wrong line.** Open the file and check. The tools return the text, and the model reports it in its own words.

## Frequently asked questions

**What is an AI agent in a hackathon project?**

A loop around a model. The model asks for a tool, your code runs it, and the result goes back to the model until it can answer. In this project the tools were `list_files`, `read_file` and `search_text`, and one question took up to four tool calls.

**How do I limit what an agent can do?**

Limit it in the tools, not in the prompt. Here every path is resolved and checked against one folder, and the tools can only read. With the prompt rule removed, the agent still asked for `../private/notes.txt` and the tool refused.

**Do I need a framework to build an agent?**

No. The loop in `agent.py` is about 20 lines and uses only the `anthropic` package. A framework can help with larger projects, and this tutorial did not test one.

## What to try next

- Point `RepoTools` at a repository you cloned, and check that `list_files` still skips what it should.
- Add a size limit on how many files `search_text` reads, for large repos.
- Add a test that sends the agent a prompt-injection line stored inside a repo file, and check that the tools still refuse.

## How this tutorial was tested

- Date: 11 November 2026. Python 3.14.6, `anthropic` 2.8.0, macOS. The model is the one in the `TUTORIAL_MODEL` setting, `claude-haiku-5-5`. `agent.py` falls back to that name if the setting is absent.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls and real runs of the tools.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. Model replies differed between runs, as expected.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- This is a teaching example, not a security audit. The sandbox was tested against `..` paths, absolute paths, a symlink and a sibling folder with a similar name. Not run: Windows paths, hard links, files that change while the agent runs, a prompt-injection test, GitHub repositories cloned from the internet, Linux, and Python versions other than 3.14.6.
