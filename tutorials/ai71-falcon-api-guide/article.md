---
title: "Comprehensive Guide to AI71's API Hub"
seo_title: "AI71 API Hub Guide: Falcon Models and SDKs"
meta_description: "AI hackathon tutorial: use the AI71 API Hub with Falcon models through the Python SDK, OpenAI SDK, LangChain and curl."
level: not stated
time: not stated
---

# Comprehensive Guide to AI71's API Hub
Whether you're an AI developer, software engineer, or just starting your coding journey, this tutorial is designed to help you navigate AI71's API Hub. We'll explore how to interact with the Falcon models, customize their settings, and manage your projects efficiently.

Let's dive in.

## Introduction to AI71’s API Hub
**AI71's API Hub** is a platform that provides access to AI models. It is meant to simplify the integration of AI capabilities into your applications, offering a range of models and tools.

## Features and Functionalities
### Home Page Overview
When you first land on the AI71 platform's home page, you'll see three main options to interact with the API:

1. AI71 Python SDK
2. OpenAI Python SDK
3. Curl

### Choosing a Model
AI71 offers several models to choose from:

- Falcon 180B
- Falcon 11B
- Falcon 11B VLM

**Note**: At the time of writing, only `tiiuae/falcon-180b-chat`, `tiiuae/falcon-11b`, and `tiiuae/falcon-11b-vlm` models are operational. The other models were listed as coming soon.

You can select any of these models right from the home page, making it easy to start your AI project with the right tools.

### Token Calculator
You'll find a handy token calculator at the right of the home page. Simply input the amount in dollars, and it will automatically calculate the number of tokens you can get. This helps you manage your budget and plan your usage.

Each option includes an example to help you get started quickly. You can choose the method that fits your workflow.


## Sandbox Page
The sandbox page is where you can interact with all the **Falcon** models in real-time. Here, you can:

1. **Select a Model**: Choose from the available models.
2. **Customize the System Prompt**: Tailor the prompt to fit your needs.
3. **Adjust Maximum Output Length**: Set the output length between 3 and 2048 tokens, depending on the model.
4. **Tweak the Temperature**: Adjust the temperature between 0 and 2 to control the randomness of the output.
5. **Adjust Top P**: Control the cumulative probability of token sequences.
6. **Adjust Top K**: Limit the next token selection to the top K tokens.
7. **Set Frequency Penalty**: Penalize new tokens based on their existing frequency in the text.
8. **Define Stop Sequences**: Specify sequences where the output should stop.

*Maximum output length will differ based on each model.*


This flexibility allows you to experiment and find settings that suit your use case.

## Documentation Page
The documentation page provides detailed instructions on how to use the supported models via different methods:

1. AI71 Python SDK
2. OpenAI SDK
3. LangChain SDK
4. Curl

Each method comes with a brief description and a usage example to help you get started quickly. Other OpenAI-supported SDKs may work if there is an option to change the Base URL and API key.


### Supported Models
AI71 supports several models, each with its specific use case and API call format:

- **tiiuae/falcon-180B-chat**: A 180B parameters causal decoder-only model fine-tuned on Ultrachat, Platypus, and Airoboros datasets.
- **tiiuae/falcon-11b**: A 11B parameters causal decoder-only model.
- **tiiuae/falcon-11b-vlm**: A 11B parameters visual language model.

For more details, refer to the AI71 documentation.


## Organization Page
The organization page allows you to create and manage your organization. Here, you can:

- Create an Organization: Set up your organization, invite one or more members.

- Manage API Keys: Create and manage API keys.

- Support: Create and manage support tickets.
- Usage: View the usage of created API keys.

This suits teams collaborating on AI projects, providing a central place to manage access and resources.

## Use Cases
AI71's API Hub can be applied in various scenarios, such as:

- **Customer Support**: Implementing chatbots that can handle customer inquiries and provide support.
- **Content Creation**: Generating content for blogs, social media, and marketing campaigns.
- **Data Analysis**: Automating the analysis of large datasets to derive insights.
- **Personal Assistants**: Developing virtual assistants to help with scheduling, reminders, and information retrieval.

## Implementations
### Using the AI71 Python SDK
Here's a quick example of how to use the AI71 Python SDK:

First, install the SDK using pip:
```bash
pip install ai71
```

Then, you can import the library and interact with any of the models in the Python file you wish to use it in:

```python
from ai71 import AI71

AI71_API_KEY = "your AI71 API key"
client = AI71(AI71_API_KEY)

# Simple invocation
print(client.chat.completions.create(
    model="tiiuae/falcon-180B-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Artificial Intelligence?"},
    ],
))
```
> Note: Replace `your AI71 API key` with your actual API key. Keep the key private and out of public repositories. You can find or create your API key in **Api Keys** under the **Organization** section.

### Using Curl
You can also interact with the API using Curl from the terminal:

```bash
curl -X POST https://api.ai71.ai/v1/chat/completions -d \
    '{
        "model": "tiiuae/falcon-180B-chat",  
        "messages": [
            {"role":"system", "content":"You are a helpful assistant."}, 
            {"role":"user", "content":"How do I tie a tie?"}
        ]
    }' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <your AI71 API key>"
```

### Using Langchain SDK
To interact with the Falcon models using the langchain sdk,

First, install the SDK using pip:
```bash
pip install langchain_openai
```

Then you can import the library and interact with any of the models in the Python file you wish to use it in:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = "YOUR_AI71_API_KEY"

chat = ChatOpenAI(
    model="tiiuae/falcon-180B-chat",
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
    streaming=True,
)

# for single use
base = chat.invoke([
    SystemMessage(content="You are MathTutor, an AI designed to help students with math problems. Provide clear, step-by-step solutions and explanations."),
    HumanMessage(content="Hi tutor, can you help me solve this quadratic equation: x^2 - 5x + 6 = 0?"),
])
print(base.content)


# for streaming in real time
# for chunk in chat.stream("Explain Newtown's Third Law"):
# print(chunk.content, end="", flush=True)
```

### Using OpenAI SDK
You can also use the OpenAI SDK to interact with the Falcon models.

First, install the SDK using pip:
```bash
pip install openai
```

Then you can import the library and interact with any of the models in the Python file you wish to use it in:

```python
from openai import OpenAI

AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = "YOUR_AI71_API_KEY"

client = OpenAI(
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
)

completion = client.chat.completions.create(
  model="tiiuae/falcon-11b",
  messages=[
    {"role": "system", "content": "You are EduTutor, an AI designed to assist with educational questions. Provide clear and helpful explanations."},
    {"role": "user", "content": "Hi Tutor, explain pythagoras theorem"}
  ]
)

print(completion.choices[0].message)
```

## Best Practices
- **Experiment with Settings**: Use the sandbox to test different models and settings to find the right fit for your application.
- **Monitor Usage**: Utilize the token calculator and usage page to keep track of your consumption and manage costs effectively.
- **Leverage Documentation**: Refer to the detailed documentation to understand the capabilities and limitations of each model.

## Conclusion
With this guide, you're ready to explore the AI71 platform. From selecting and customizing models to managing your organization's resources, AI71 provides a set of tools for your AI projects. Happy coding!

## Use it at an AI hackathon

An OpenAI-compatible endpoint like this one lets you switch models by changing the base URL and key. You could use it for a support chatbot, a content tool or a tutor app within a hackathon weekend. To find an event, see the [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

**Which models does the guide cover?**
`tiiuae/falcon-180b-chat`, `tiiuae/falcon-11b` and `tiiuae/falcon-11b-vlm` were the operational models at the time of writing.

**Which ways can I call the API?**
The AI71 Python SDK, the OpenAI Python SDK, the LangChain SDK and curl. Other OpenAI-supported SDKs may work if you can change the base URL and API key.

**Where do I find my API key?**
In Api Keys under the Organization section of the AI71 platform.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, and no step has been confirmed to work as written. To follow it you would need an AI71 account with an organization and an API key, paid token credit, and Python with `ai71`, `openai` or `langchain_openai`. No account, key or paid service was used here.
