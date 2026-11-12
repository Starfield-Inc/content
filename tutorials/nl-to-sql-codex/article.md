---
title: "OpenAI Codex tutorial: Natural language to SQL query with OpenAI Codex"
seo_title: "Natural Language to SQL with OpenAI Codex"
meta_description: "AI hackathon tutorial: turn plain-English requests into SQL queries with OpenAI Codex and a short Python script."
level: not stated
time: not stated
---
## Unraveling the OpenAI Codex

OpenAI Codex is an AI model from OpenAI that interprets natural language and responds with generated code. It powers GitHub Copilot. Codex is an offshoot of OpenAI's GPT-3 model, fine-tuned for coding applications. OpenAI has released an API for Codex, at the time of writing in closed beta.

You can explore Codex in the [OpenAI playground](https://platform.openai.com/playground).

## Natural language to SQL

Imagine transforming natural language into a SQL query. Say you need to fetch all users above 25 years old. You simply state:

>Fetch all users above 25 years old

And the model generates the corresponding SQL query:

>SELECT * FROM users WHERE age > 25

This lets you generate SQL queries without knowing SQL syntax, which helps non-technical people who need to query a database.

## Let's get started!

Make sure you have access to Codex. If you do not, you can join the Codex waitlist here: https://openai.com/blog/openai-codex/. Getting accepted usually takes a few days.
Before we write any code, you can do some testing first in the OpenAI playground: https://beta.openai.com/playground. 
I recommend testing first, because it helps you understand how the model works.  

First, we need to install the OpenAI library:

```python
!pip install openai
```

You can find the full documentation of this library here: https://github.com/openai/openai-python

Then, we need to import the library and set the API key

```python
import openai

openai.api_key = "YOUR_API_KEY"
```

Do not commit a real API key to a public repository. Load it from an environment variable instead.

Now, we can start writing some code. We will start by creating a function that will generate a SQL query from natural language. We will use the `openai.Completion.create` function to generate the SQL query. We will pass the following parameters:

- `engine`: The engine that will be used to generate the SQL query. We will use `davinci-codex` for this tutorial.
- `prompt`: The natural language that will be used to generate the SQL query.
- `max_tokens`: The maximum number of tokens that will be generated.
- `temperature`: The temperature of the model. The higher the temperature, the more random the text will be. Lower temperature results in more predictable text.
- `top_p`: The cumulative probability for top-p sampling. 1.0 means no restrictions. Lower top_p results in more random completions.
- `frequency_penalty`: The cumulative probability for top-p sampling. 1.0 means no restrictions. Lower top_p results in more random completions.
- `presence_penalty`: The cumulative probability for top-p sampling. 1.0 means no restrictions. Lower top_p results in more random completions.
- `stop`: The sequence of tokens that will stop the generation.

```python
def generate_sql_query(prompt, max_tokens=100, temperature=0.5, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=["\n"]):
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    return response.choices[0].text
```

Now, we can test our function. We will use the following prompt:

> Get all the users that are older than 25 years old

```python
generate_sql_query("Get all the users that are older than 25 years old")
```

The model will generate the following SQL query:

```sql
SELECT * FROM users WHERE age > 25
```

Now we put it all together in one file and add input via the console.

```python
import openai

openai.api_key = "YOUR_API_KEY"

def generate_sql_query(prompt, max_tokens=100, temperature=0.5, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return response.choices[0].text

prompt = input("Enter your prompt - What data do you need?: ")
print(generate_sql_query(prompt))
```

Now run the file, enter your prompt and get back the SQL query.

## Wrapping up

We generated SQL queries from natural language and used the OpenAI library to call Codex.

You can improve this project by integrating a database and a user-friendly web interface. To guide the model more accurately, consider adding more prompts to the request.

For precision, you could include your database schema in the prompt. For instance:

```
USER: ID (INT), NAME (VARCHAR), AGE (DATE)
POST: ID (INT), TITLE (VARCHAR), BODY (VARCHAR), USER_ID (INT)
COMMENT: ID (INT), BODY (VARCHAR), POST_ID (INT), USER_ID (INT)
```

## Use it at an AI hackathon

A natural-language database query tool is a compact AI hackathon project: the idea is easy to explain and the demo is short. You could add a web interface and a real database over a weekend. To find an event, see the [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

**What is OpenAI Codex?**
An AI model from OpenAI that interprets natural language and responds with generated code. It is a GPT-3 offshoot fine-tuned for coding, and it powers GitHub Copilot.

**How can I make the generated SQL more accurate?**
Add more prompts to the request, and include your database schema in the prompt, for example the table and column definitions shown above.

**What can I add to this project?**
Integrate a database and a user-friendly web interface.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, and no step has been confirmed to work as written. To follow it you would need an OpenAI account with an API key and access to a Codex model, plus Python with the `openai` package. No API key or paid service was used here.
