---
title: "Unlocking LLaMA 3 with Ollama: A Beginner's Guide"
seo_title: "Run LLaMA 3 with Ollama in Python: Beginner Guide"
meta_description: "AI hackathon tutorial: set up LLaMA 3 with Ollama and use it from Python for chat, streaming, text completion and SQL generation."
level: not stated
time: not stated
---

# Unlocking LLaMA 3 with Ollama: A Beginner's Guide

This tutorial is for anyone interested in generative models, especially those looking to build projects for hackathons. We use Ollama to make it easy to run a model locally. Let's dive into LLaMA 3, a generative model, and see how it can turn your ideas into reality.

## Objectives
By the end of this tutorial, you'll be able to:
- Set up and use the LLaMA 3 model via Ollama.
- Implement basic chat functionality using the LLaMA 3 model.
- Stream responses for real-time feedback.
- Maintain ongoing dialogue with context.
- Complete text prompts effectively.
- Generate SQL queries from text inputs.
- Create custom clients to interact with the Ollama server.

## Prerequisites
Before we get started, make sure you have the following:
- Basic knowledge of Python
- A code editor like Visual Studio Code (VSCode)
- A computer with internet access

## Instructions on How to Install LLaMA3
In this section, we walk through setting up **LLaMA 3** using Ollama. **LLaMA 3** is a generative model that can be used for various natural language processing tasks. We use Ollama to interact with **LLaMA 3** and run our Python scripts.

### Installation and Setup
First, you'll need to set up Ollama and install the required libraries. We use the Ollama app to interact with **LLaMA 3**.

1. **Download and Install Ollama**: Go to [Ollama's official website](https://www.ollama.com/) and download the desktop app. Follow the installation instructions for your operating system.

2. **Start the Ollama App**: Once installed, open the Ollama app. The app will run a local server that the Python library will connect to behind the scenes.

3. **Download LLama3 Locally**: Open your local terminal and run the following command to download the **llama3** 8 billion parameter 4-bit model locally, which we will use in our program.
    ```bash
   ollama pull llama3
   ```

4. **Install Ollama Python Library**: Still in your local terminal, run the following command to install the Ollama library for Python.
    ```bash
   pip3 install ollama
   ```


## Practical Applications
Create a Python file named `llama3_demo.py` or whatever you prefer, just make sure it has a `.py` extension. Copy and paste the following code snippets into your file to explore the practical applications of **LLaMA 3** with Ollama.

### Conversation Initiation
You can start a conversation with the **llama3** model with the `chat` function:

```python
import ollama

prompt = 'Create a product description for a new smartphone:'
response = ollama.chat(model='llama3', messages=[{
    'role': 'user',
    'content': prompt,
},
])
print(response['message']['content'])
```

### Streaming Responses
For applications requiring real-time feedback, you can enable streaming responses. This allows you to receive parts of the response as they are generated:

```python
import ollama

ollama_response = ollama.chat(
    model='llama3',
    stream=True,
    messages=[
        {
            'role': 'user',
            'content': 'Explain the Big Bang theory',
        },
    ]
)

for chunk in ollama_response:
    print(chunk['message']['content'], end='', flush=True)
```

### Ongoing Dialogue with Context
Maintaining context in a conversation allows for more natural interactions. Here's how you can manage ongoing dialogue:

```python
import ollama

chat_messages = []

def create_message(content, role):
    return {'role': role, 'content': content}

def chat():
    response = ollama.chat(model='llama3', stream=True, messages=chat_messages)
    assistant_message = ''
    for chunk in response:
        assistant_message += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)
    chat_messages.append(create_message(assistant_message, 'assistant'))

def ask(message):
    chat_messages.append(create_message(message, 'user'))
    print(f'\n\n--{message}--\n\n')
    chat()

ask('What is the capital of France?')
ask('How far is it from Paris to Berlin?')
```

### Text Completion
You can use Ollama with **Llama3** for text completion tasks, such as code generation or completing sentences, with the `generate` function:

```python
import ollama

response = ollama.generate(
    model='llama3',
    prompt='Once upon a time, in a faraway land,'
)
print(response['response'])
```

### Custom Clients
You can also create a custom client to interact with the Ollama server. Here's an example of a custom client:

```python
from ollama import Client

client = Client(host='http://your-ollama-server')
response = client.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': 'What is machine learning?',
    }
])
print(response['message']['content'])
```

If you point a client at a remote Ollama server, make sure that server is not open to the public internet without access control.

### Generating SQL from Text
Ollama can be used to generate SQL queries from natural language inputs. Here's how to set up a local instance and use it:

```python
from ollama import Client

client = Client(host='http://localhost:11434')

prompt = 'Get the top 10 most expensive products.'
response = client.chat(model='llama3', messages=[
    {
        'role': 'system',
        'content': """Here is the database schema that the SQL query will run on:
    CREATE TABLE products (
      product_id INTEGER PRIMARY KEY,
      name VARCHAR(50),
      price DECIMAL(10,2),
      quantity INTEGER
    );
    """,
    },
    {
        'role': 'user',
        'content': prompt,
    }
])
print(response['message']['content'])
```

## Running Your Python File
To run your Python file, open your terminal, navigate to the directory where your `llama3_demo.py` file is located, and run:

```bash
python3 llama3_demo.py
```

## Conclusion

In this tutorial, we explored the basics of **LLaMA 3**, how to set it up, and practical applications using Ollama. You learned how to implement chat functionality, streaming responses, maintain dialogue context, complete text, generate SQL, and create custom clients.

For more details, check out the Ollama Blog on [Python & JavaScript Libraries](https://ollama.com/blog/python-javascript-libraries).

## Use it at an AI hackathon

Running a model locally means no API bill and no rate limits during a short event, which suits an AI hackathon. You can build a chat app, a text tool or a natural-language database helper on top of these snippets. To find an event, see the [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

**Do I need a powerful computer or an API key?**
The tutorial uses the Ollama desktop app, which runs a local server, and downloads the llama3 8 billion parameter 4-bit model with `ollama pull llama3`. No API key is used.

**How do I keep context across several questions?**
Keep a `chat_messages` list, append each user and assistant message to it, and pass the whole list to `ollama.chat` on every call.

**How do I get SQL from a text request?**
Send a system message that contains the database schema, then a user message with the request, as in the SQL example above.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, and no step has been confirmed to work as written. To follow it you would need the Ollama desktop app, a local download of the llama3 model (several GB of disk) and Python with the `ollama` package. No account or API key is required and none was used here.
