---
title: "Build a Personal Assistant with LangChain and Claude in Python"
seo_title: "LangChain Claude Assistant in Python: AI Hackathon Guide"
meta_description: "Build an AI hackathon assistant in Python with LangChain and Claude: a prompt template, chat memory, a calculator tool and a notes reader."
description: "Build an AI hackathon assistant in Python with LangChain and Claude: a prompt template, chat memory, a calculator tool and a notes reader."
---

# Build a personal assistant with LangChain and Claude in Python

You build a command-line assistant that follows a prompt template, remembers the conversation, does arithmetic with a calculator tool and answers questions from a notes file.

**Time:** about 40 minutes. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, and an Anthropic API key. **Tested:** 12 November 2026 with Python 3.14.6, `langchain` 1.5.0, `langchain-anthropic` 1.7.10 and `langgraph` 1.2.20 on macOS.

Model replies differ from run to run. Your wording will not match the output below. The tool calls and the memory behaviour should.

An assistant that can use tools and keep context is a common starting point for an AI hackathon project. If you are planning one, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A model on its own cannot do exact arithmetic reliably, cannot see your files, and forgets everything between calls. Tools fix the first two. Memory fixes the third, for as long as the process runs. LangChain 1.x gives you one function, `create_agent`, that wires these together. Older tutorials use `ConversationBufferMemory` and `initialize_agent`. This one uses the current approach, where memory is a LangGraph checkpointer.

## See it running first

This is the finished assistant over four turns in one conversation. It reads the notes, uses the calculator, and recalls a name from the first turn.

{{shot:05-chat|Terminal output of assistant.py: four turns, with read_notes and calculator tool calls and the name Sam recalled}}

The rest builds it from scratch.

## Step 1: Set up the project

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt`:

{{file:requirements.txt}}

{{cmd:02-install}}

{{shot:02-install|Terminal output listing langchain 1.5.0, langchain-anthropic 1.7.10 and langgraph 1.2.20}}

Put your key in a file named `.env`. Copy the placeholder file and edit it:

{{file:.env.example}}

Never paste a real key into code, a screenshot or a chat. Load it into your terminal on macOS or Linux:

```bash
set -a; source .env; set +a
```

## Step 2: Write the two tools

A tool is a plain Python function with a type-annotated signature and a docstring. The `@tool` decorator turns the docstring into the description the model reads when it decides which tool to call, so write it for the model.

The calculator does not use `eval`. The model controls the input, and `eval` would run whatever it sent. Instead the code parses the expression into a syntax tree and allows only numbers and the operators `+ - * / **`. It also caps the exponent, because an expression like `9 ** 9 ** 9` would otherwise run for a very long time. Errors come back as text, so the model can read them and try again.

The notes tool takes no arguments and returns the whole file. That works for a short file. A long file would need search or chunking.

{{file:tools.py}}

Test the tools without a model first. A failure here is yours, not the model's.

{{cmd:03-tools}}

{{shot:03-tools|Terminal output of tools.py: calculator results, three error messages and the notes text}}

The calculator returns 1730 for `1250 + 480`. Division by zero, a call to `__import__` and the huge exponent each return an error string and do not run.

## Step 3: Write the prompt template and the agent

The system prompt is a `ChatPromptTemplate` with two variables, `assistant_name` and `today`. `format_messages` fills them in and returns a system message, which goes to `create_agent` as `system_prompt`. A template earns its place when the prompt changes per user or per day. For a fixed prompt a plain string does the same.

Memory is the `checkpointer`. `InMemorySaver` stores the message history of each conversation under a `thread_id` that you pass in the call's config. Calls with the same `thread_id` continue one conversation. A different `thread_id` starts a new one. The `ask` function sends only the new question each time, because the checkpointer already holds the earlier messages.

The model is `claude-haiku-5-5` through `ChatAnthropic`, with `max_tokens=300`. The script prints each tool call so you can see what the model chose to do.

{{file:assistant.py}}

First, see what a missing key looks like:

{{cmd:04-no-key}}

{{shot:04-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

## Step 4: Chat with memory and tools

Each command-line argument is one turn, and all turns share one thread. The four questions test the pieces in order: a fact to remember, a tool that reads a file, a tool that does arithmetic on a number from the previous reply, and a recall of the fact from turn one.

{{cmd:05-chat}}

{{out:05-chat}}

Read the output in three parts. In turn two the model called `read_notes` and then `calculator` with `1250 + 480`, and answered 1730. In turn three it wrote `1730 / 5` without being told the number, so it took "that total" from the saved history, and the calculator returned 346. In turn four it knew the name Sam.

The tool lines print before the `You:` line of the same turn, because the script prints them first. In turn one the model also said it could not remember your name "for later". That is true of this script too, as the next step shows.

## Step 5: See where memory stops

`InMemorySaver` keeps history in the Python process. Run the script again with a new question and the history is gone:

{{cmd:06-new-thread}}

{{shot:06-new-thread|Terminal output of a second run: the assistant reads the notes and cannot find the name}}

The assistant looked in the notes for a name and found none. To keep history across runs, swap `InMemorySaver` for a database-backed checkpointer from the LangGraph packages. This tutorial did not test one.

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set`.** The variable is not set in the terminal you are using. Run `set -a; source .env; set +a` again there.
- **You find `ConversationBufferMemory` or `initialize_agent` in older guides and the import fails.** Those belong to older LangChain versions. In `langchain` 1.5.0 use `create_agent` with a checkpointer, as above.
- **The assistant forgets the earlier turn.** Check that every call passes the same `thread_id` and that you did not build a second agent object for each question. The checkpointer belongs to the agent.
- **The model does its own sums instead of calling the calculator.** The prompt tells it to use the calculator for arithmetic, but nothing forces it. Check the `[tool]` lines to see whether it did.

## Frequently asked questions

**How do I add memory to a LangChain agent?**

Pass a checkpointer, such as `InMemorySaver`, to `create_agent`, and pass a `thread_id` in the config of each call. The checkpointer stores the messages of that thread, so you send only the new question. In this tutorial the assistant recalled a name from turn one in turn four.

**Can Claude call my own Python functions in LangChain?**

Yes. Decorate a function with `@tool`, give it a clear docstring, and pass it in the tools list to `create_agent`. The model returns a tool call, LangChain runs your function and sends the result back. The calculator and `read_notes` here worked that way.

**Does the assistant remember me after I close the script?**

Not with `InMemorySaver`. The second run in Step 5 had no memory of the name. You need a persistent checkpointer for that, which this tutorial did not test.

## What to try next

- Replace `InMemorySaver` with a persistent checkpointer and run the Step 5 test again.
- Add a tool that appends a line to `notes.txt`.
- Make `read_notes` return only the lines that match a search word.

## How this tutorial was tested

- Date: 12 November 2026. Python 3.14.6, `langchain` 1.5.0, `langchain-anthropic` 1.7.10, `langgraph` 1.2.20, macOS. The model is `claude-haiku-5-5`, set in the `MODEL` constant.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls.
- Every step was run from a clean folder, then replayed from an empty copy with no virtual environment. The replay passed. Model wording differed between the two runs, as expected, but the same tools were called with the same arguments.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run: Windows, Linux, other Python versions, a persistent checkpointer, streaming, and models other than `claude-haiku-5-5`.
