---
title: "Add Chat Memory to Your AI Hackathon Chatbot"
description: "AI hackathon chatbot tip: learn how chat memory works and add it to a Python chatbot. Includes token counts and trimming old messages."
---

# Build a chatbot that remembers the conversation in Python

You build a terminal chatbot that keeps the chat history between turns, prints a token count for every call, and trims old messages when the history gets long.

**Time:** about 30 minutes. **Level:** beginner. **You need:** Python basics, Python 3.10 or newer, and an Anthropic API key. **Tested:** 10 November 2026 with Python 3.14.6 and the `anthropic` package 2.7.0 on macOS.

Model replies differ from run to run. Your words and token counts will not match the output below exactly. The shape of the output will.

A chatbot that forgets the last question is easy to spot in a demo, and memory is a small change. If you plan to build a chatbot, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A language model API does not remember anything between calls. Each call sees only the messages you send in it. A chatbot that seems to remember is a program that sends the earlier messages again each turn. That has a cost: every turn sends more input tokens than the one before. Trimming old messages is how you keep that cost in check, and it is also how a bot forgets.

## See it running first

This is the finished bot answering four scripted lines. The last line asks for the name given in the first line.

{{shot:05-memory|Terminal output of chat.py: four turns, the message count grows from 1 to 7 and the bot answers that the name is Maya}}

The rest of the tutorial builds it from nothing.

## Step 1: Set up the project

Make a folder, create a virtual environment and activate it. The commands from here on assume it is active.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt` with one line:

{{file:requirements.txt}}

Install it. The output below shows the version used for this tutorial.

{{cmd:02-install}}

{{out:02-install}}

## Step 2: Store the key outside the code

Put your key in a file named `.env` in the project folder. Copy the placeholder file and edit it:

{{file:.env.example}}

Never paste a real key into code, a screenshot or a chat. Add `.env` to `.gitignore` if you use git. Then load the file into your terminal session (macOS and Linux):

```bash
set -a; source .env; set +a
```

You can also run `export ANTHROPIC_API_KEY=...` in the terminal yourself. The scripts below read the variable from the environment, and the SDK reads it too.

If the variable is missing, the script stops with a clear message. This is what the message looks like when you run `chat.py` (built in Step 4) in a terminal where the variable is not set:

{{shot:03-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

## Step 3: Make a call, and see that it forgets

`forgetful.py` makes two separate calls. The first says a name. The second asks for it. The second call sends only its own message. The `MODEL` and `MAX_TOKENS` constants sit at the top so you can change them in one place.

{{file:forgetful.py}}

Run it:

{{cmd:04-forgetful}}

{{shot:04-forgetful|Terminal output of forgetful.py: the bot greets Maya, then says it does not know the name}}

The second call has no way to know the name. Nothing was stored between the calls.

## Step 4: Keep a message list

The fix is a Python list. Each turn you append the user's message, send the whole list, and append the reply. The API takes a list of `{"role": ..., "content": ...}` items. Roles are `user` and `assistant`, and a `system` string sets the bot's manner.

`chat.py` also prints a line after each reply. It shows how many messages were sent, a letter per message (U for user, A for assistant), and the input and output token counts. These come from `response.usage`, which the API returns with each reply.

A real chatbot waits for you to type. To make this tutorial repeatable, the questions come from a file, `script.txt`, piped into the program. When input is piped, a terminal does not show the lines, so the program prints each one.

{{file:script.txt}}

{{file:chat.py}}

Run it with the script as input. In your own terminal you can run `python chat.py` and type the lines yourself.

{{cmd:05-memory}}

{{out:05-memory}}

Read the lines that start with `[sent`. The message count goes 1, 3, 5, 7. The input tokens go 46, 109, 170, 259. Input grows because the whole list is sent again each turn, and each reply is added to it. The output tokens depend on how long each reply is, so they do not grow in a pattern. At the end the bot answers with the name from the first line. Totals for the session were 584 input tokens and 190 output tokens.

## Step 5: Trim old messages

A list that only grows will cost more every turn, and it will eventually exceed the model's input limit. The simplest fix is to keep only the last few messages. The `trim` function in `chat.py` does that. It keeps the last N messages, then drops a leading assistant message if there is one, because the list should start on a user turn.

Run the same script with `--keep 4`:

{{cmd:06-trim}}

{{out:06-trim}}

The bot reports `[trimmed 2 old messages]` before the third and fourth turns. From the third turn on, only three messages are sent each time, so the input stays near 100 tokens. The cost is that the bot no longer has the first line. When the script asks for the name in the last turn, the bot has nothing to answer from. Check your own output: the exact words differ per run.

One reply in this run stops mid-sentence. That is the `MAX_TOKENS` limit of 150 doing its job. Raise it if you want longer replies.

Dropping old messages is the blunt method. Two common alternatives are to keep the first message pinned, or to ask the model to summarise old messages into one. Neither is built here.

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set`.** The variable is not in the terminal you are running from. Run the `set -a; source .env; set +a` line again in that terminal.
- **`AttributeError: ... has no attribute 'text'`.** In one of my test runs the reply held a block of another type before the text, and `response.content[0].text` failed. I did not find out why it appeared in that run. The scripts here join only the blocks whose type is `text`, which avoids the error.
- **An authentication error from the API.** The key is wrong or has been revoked. Create a new one in your Anthropic account and update `.env`.
- **The bot answers as if it forgot.** Check that you append the reply to the list after each call. Without it, the model never sees its own earlier answers.

## Frequently asked questions

**How does a chatbot remember a conversation?**

The API remembers nothing between calls. The program keeps a list of messages and sends the whole list again each turn. In the test, the bot answered with the name from the opening line.

**How much memory can a chatbot keep?**

The tutorial did not find a limit. It kept every message in one run, and with `--keep 4` it sent only three messages per turn. The model's input limit was not tested here.

**Does chat memory raise API cost in a hackathon?**

Yes. Input tokens rose from 46 to 109, 170 and 259 over four turns, and the session used 584 input tokens. Trimming keeps the input near 100 tokens, but the bot then forgot the name.

## What to try next

- Pin the first message so it is never trimmed.
- Trim by token count, using the `input_tokens` value, instead of by message count.
- Ask the model to summarise the messages you are about to drop, and keep the summary as the first message.

## How this tutorial was tested

- Date: 10 November 2026. Python 3.14.6, `anthropic` 2.7.0, macOS. The model is `claude-haiku-5-5`, set in the `MODEL` constant.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. Model replies differed between the two runs, as expected.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run: Windows, Linux, and Python versions other than 3.14.6. The `source .env` line is for macOS and Linux shells.
