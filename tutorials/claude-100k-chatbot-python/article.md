---
title: "Anthropic tutorial: how to create a 100 000 token context AI chatbot"
seo_title: "Build a 100K Token Context Chatbot with Claude"
meta_description: "AI hackathon tutorial: build a simple Python chatbot with a 100 000 token context Claude model and a per-message cost readout."
level: not stated
time: not stated
---

## Is Claude good for chatbots?

Anthropic's Claude has been designed to be a chatbot. First, safety was a priority as it was being built. Second, its large 100 000 token context window helps with long conversations, and its ability to generate long texts suits chatbots. It also lets us give the model additional context, so it can extract more information and be more accurate in its responses. Let's see how to build a simple chatbot with Claude. With this knowledge you can build many more Anthropic applications.

_Getting early access to Anthropic Claude was described in a previous tutorial._

## Coding

### Dependencies

We can proceed to create the project. Let's start by creating the main folder.

```bash
mkdir chatbot-claude

cd chatbot-claude
```

Now we can create a virtual environment and install the necessary libraries.

```bash
python3 -m venv venv

# Linux/Mac OS
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

pip install anthropic python-dotenv
```

The last step will be to create a `main.py` file and import the libraries.

```python
import os

import anthropic
from dotenv import load_dotenv

load_dotenv()
```

### Chatbot

We follow the template of an OpenAI chat endpoint boilerplate project. As there, we display the cost of generating a response after each message. This matters because we do not want to overshoot the amount of money used to generate the response.

First we initialize the Anthropic client, the context, and prepare constants with prices for generating one token (in USD).

```python
anthropic_client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

# you can put some context here, to specialize the Model
context = ""

# Anthropic Claude pricing (May 2023 price sheet)
PRICE_PROMPT = 1.102e-5
PRICE_COMPLETION = 3.268e-5
```

Let the next step be preparation of a function to count the number of tokens in the prompt and response. Then it returns text with information about the tokens used.

```python

def count_used_tokens(prompt, completion):
    prompt_token_count = anthropic.count_tokens(prompt)
    completion_token_count = anthropic.count_tokens(completion)

    prompt_cost = prompt_token_count * PRICE_PROMPT
    completion_cost = completion_token_count * PRICE_COMPLETION

    total_cost = prompt_cost + completion_cost

    return (
        "🟡 Used tokens this round: "
        + f"Prompt: {prompt_token_count} tokens, "
        + f"Completion: {completion_token_count} tokens - "
        + f"{format(total_cost, '.5f')} USD)"
    )
```

The final step is to run a chat loop, retrieve text from the user, collect context and generate a response.

```python
while True:
    user_inp = input("You: ")

    current_inp = anthropic.HUMAN_PROMPT + user_inp + anthropic.AI_PROMPT
    context += current_inp

    prompt = context

    completion = anthropic_client.completion(
        prompt=prompt, model="claude-v1.3-100k", max_tokens_to_sample=1000
    )["completion"]

    context += completion

    print("Anthropic: " + completion)
    print(count_used_tokens(prompt, completion))
```

### Let's test it

Our app is ready. Run it with:

```bash
python main.py
```

## Quick and easy to set up

The chatbot answers each message and prints the token cost of the round. It is worth testing it with more examples, and most importantly, checking the context. The context window here is large: 100k tokens.

## Use it at an AI hackathon

A chatbot with a large context window is a practical starting point for an AI hackathon project, for example a bot that answers questions over long documents. Building it with other people in a short time, with help from mentors, is a good way to turn the idea into a demo. To find an event, see the [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

**Why is Claude described as a good fit for chatbots?**
Safety was a priority as it was built, and its 100 000 token context window helps with long conversations and long generated texts.

**How does the chatbot show what each message costs?**
`count_used_tokens` counts the tokens in the prompt and the completion, multiplies them by the price constants and prints the total in USD after every reply.

**How does the bot remember the conversation?**
The loop appends each user input and each completion to `context`, and sends the whole context as the prompt on every turn.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, and no step has been confirmed to work as written. To follow it you would need a paid Anthropic account with an API key (stored in a `.env` file as `ANTHROPIC_API_KEY`), and access to the 100k-context model named in the code. No API key or paid service was used here.
