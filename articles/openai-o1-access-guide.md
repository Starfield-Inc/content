---
title: "How to Access OpenAI's o1 Models and Who Can Use Them"
summary: "A short guide to who can use OpenAI's o1-preview and o1-mini models, what they cost through OpenAI and a third-party provider, how reasoning tokens count, and what the models could not do at launch."
byline: Starfield Labs
seo_title: "How to Access OpenAI's o1 Models and Who Can Use Them"
meta_description: "AI hackathon builders: see who can access OpenAI's o1 models, the pricing and limits at launch, and how reasoning tokens count."
---

# How to Access OpenAI's o1 Models and Who Can Use Them

The release of OpenAI's **o1 model** represents a breakthrough in AI's reasoning capabilities, designed to tackle complex tasks like advanced coding, scientific problem-solving, and algorithmic reasoning. In this guide, we’ll explain how you can access this model, who qualifies, and outline important pricing information from third-party providers.

## What is the OpenAI o1 Model?

Released in **September 2024**, the OpenAI o1 series includes **o1-preview** and **o1-mini** models, both of which are optimized for reasoning-heavy tasks. These models are ideal for:
- **Mathematical problem-solving**: Solving complex equations and performing high-level calculations.
- **Scientific research**: Tackling complex queries in healthcare, quantum computing, and more.
- **Coding and debugging**: Generating complex workflows and multi-step algorithms for developers.

### Key Features:
- **Reasoning tokens**: These tokens enable deeper reasoning capabilities, which help the model excel at tasks that involve multi-step logical processes.
- **Large context window**: The models support large context windows (128k tokens), ideal for processing detailed information in one go.
- **Cost-effective options**: o1-mini is designed for speed and efficiency, making it more affordable for developers focusing on coding tasks.
## Who Can Access the OpenAI o1 Models?

Access to the o1 models is restricted based on **subscription tiers**, **API usage**, and **third-party providers**.

### 1. **ChatGPT Plus and Team Users**
   - Users subscribed to **ChatGPT Plus** or **Team** can access the o1 models directly in the ChatGPT interface.
   - Weekly usage limits are set at **30 messages for o1-preview** and **50 messages for o1-mini**, but these limits are expected to expand in the future as OpenAI broadens access.

### 2. **Enterprise and Educational Users**
   - Enterprise and educational accounts enjoy unrestricted access to both o1-preview and o1-mini. This is especially valuable for research-intensive industries like healthcare, where AI-assisted problem-solving can save significant time and resources.

### 3. **Developers via API Access**
   Developers who meet the criteria for **tier 5 API access** (having spent $1,000+ in the past 30 days on OpenAI API) are granted access to the o1 models via the **Chat Completions API**. The pricing is as follows:
   
  **o1-preview** 
   - **$15.00 per million input tokens**
   - **$60.00 per million output tokens**
   
   **o1-mini** 
   - **$3.00 per million input tokens**
   - **$12.00 per million output tokens**
   
   These models have rate limits of **500 requests per minute** for **o1-preview** and **1,000 requests per minute** for **o1-mini**. While these models are highly capable, developers should note that some features such as **function calling**, **streaming**, and **batch calls** are not available at this time.

### 4. **Third-Party Providers Like AI/ML API**
   For those who do not qualify for OpenAI's tier 5 API access, third-party providers such as **AI/ML API** offer access to the o1 models with varying pricing tiers. The pricing for **AI/ML API** is based on usage:

   - **o1-preview**:
     - **$0.01575 per 1,000 input tokens**
     - **$0.063 per 1,000 output tokens**

   - **o1-mini**:
     - **$0.00315 per 1,000 input tokens**
     - **$0.0126 per 1,000 output tokens**

   This makes AI/ML API a valuable alternative for developers looking for cost-effective ways to use the o1 models. Below are examples of how to access these models using via AI/ML's API.

### Example in Python

```py
import os
from openai import OpenAI

user_content = """
how many Rs are there in the word strawberry
think step by step
"""

client = OpenAI(
    api_key=aiml_api_key,
    base_url="https://api.aimlapi.com/",
)

chat_completion = client.chat.completions.create(
    model="o1-mini",
    messages=[
        {"role": "user", "content": user_content},
    ],
    max_tokens=2000,
)

response = chat_completion.choices[0].message.content
print("Response:\n", response)
```

## Important Considerations: Reasoning Tokens

When working with the o1 models, it’s important to note the concept of reasoning tokens. These are tokens that are processed during the model’s internal reasoning but are not visible in the API responses. However, these tokens still count towards the output token limit. In the ChatGPT interface, you may see these intermediate reasoning steps, but they remain invisible in API calls, which is crucial to keep in mind when budgeting for token usage.

By using the o1 models, whether directly through OpenAI or via third-party providers like AI/ML API, you can access advanced reasoning capabilities that are pushing the boundaries of AI-driven solutions.

## Limitations and Future Enhancements

While the o1 models are powerful, there are a few limitations:
- **No browsing support**: The o1 models currently cannot access real-time web data.
- **No file uploads**: Uploading external data for processing is not yet supported in the API.
- **No system messages**: The API only supports user and assistant messages, limiting some advanced customizations.

However, OpenAI is actively working on expanding these features, so future iterations will likely support more robust functionality, such as **streaming**, **system messages**, and **file handling**.

## Build it at an AI hackathon

Reasoning models are well suited to an AI hackathon, where a single hard problem such as planning or code generation can be the whole project. Starfield Labs lists [upcoming AI hackathons](/ai-hackathons/) if you want a deadline and a team.

## Frequently asked questions

**Who can access the OpenAI o1 models?**

At the time of writing, ChatGPT Plus and Team users, Enterprise and educational users, developers with tier 5 API access (more than $1,000 spent on the OpenAI API in the past 30 days), and users of third-party providers such as AI/ML API.

**What are reasoning tokens?**

Reasoning tokens are processed during the model's internal reasoning but are not visible in API responses. They still count towards the output token limit, which matters when you budget for token usage.

**What limitations did the o1 models have?**

The article lists no browsing support, no file uploads in the API, and no system messages, with OpenAI said to be working on streaming, system messages and file handling.

---

**Some Useful Information**:

- [Introducing OpenAI o1 | OpenAI](https://openai.com/index/introducing-openai-o1-preview/)
- [Access o1 via AI/ML API](https://aimlapi.com/models/openai-o1-preview-api)
