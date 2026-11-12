---
title: "Vectara Hackathon Guide"
seo_title: "Vectara RAG Guide for AI Hackathon Projects"
meta_description: "AI hackathon guide to Vectara: build question answering, chat and semantic search on your own data with a RAG platform."
---

# Vectara Hackathon Guide

## Vectara Overview

Vectara is a GenAI platform. It's designed to make it easy for you to build and deploy GenAI applications that can generate text-based answers using your particular data 
(this type of application flow is also known as RAG or retrieval-augmented-generation). 
You just ingest your data and then build apps using the Query and Summarization APIs. It's that simple.

Use-cases include:

- **Question Answering**: provide direct answers to specific questions based on the data.
- **Conversational AI / Chat**: chatbots that can hold a full conversation with a human, with back-and-forth exchanges.
- **Semantic (Neural) Search**: build applications powered by fast and powerful semantic search that finds documents by matching to the user intent.

## Getting started with Vectara

You can get to know Vectara’s features in 5 minutes:

1. [Sign up](https://console.vectara.com/signup/) for a free Vectara account.
2. [Log in](https://console.vectara.com/login) and take the 5-minute walk-through.

We have more resources to help you build apps with Vectara:

- The [Quick Start guide](https://docs.vectara.com/docs/quickstart) shows you how to use the Vectara Console.
- Read the [API recipes](https://docs.vectara.com/docs/api-recipes) for common patterns with our APIs.
- Our [API playground](https://docs.vectara.com/docs/rest-api/) shows you how Vectara’s API requests and responses are structured.
- See “Additional resources”, below, for a comprehensive list.

General guidelines:

- Vectara provides a free plan (suited to a hackathon) with up to 50MB of text and 15K monthly queries.
- Use the [Indexing API](https://docs.vectara.com/docs/api-reference/indexing-apis/indexing) to ingest data into your Vectara corpus.
- Use the [File Upload API](https://docs.vectara.com/docs/api-reference/indexing-apis/file-upload/file-upload) to upload files such as PDF, PPT or DOC.
- Use the [Search API](https://docs.vectara.com/docs/api-reference/search-apis/search) to run queries against the data ingested.
- The [Console](https://console.vectara.com/login) provides a unified view of information about your Vectara account, corpora and their characteristics. You can also run example queries directly from the console for quick experimentation.

## Frequently asked questions

### What should I do if I need to go over the free plan limits?

Vectara’s free plan provides up to 50MB of text and 15K queries a month. This should be sufficient for many use-cases, including in a hackathon setting.

To get additional capacity, you can add a credit card to the account and buy additional [bundles](https://vectara.com/pricing/), or [transition](https://vectara.com/contact-us/) to our Scale plan.

### Should I use RAG and not fine-tuning?

Our experience shows that “Fine-tuning is for Form, and RAG is for facts” as discussed [here](https://www.anyscale.com/blog/fine-tuning-is-for-form-not-facts) and [here](https://vectara.com/fine-tuning-vs-grounded-generation/).

## Additional resources

| API docs | https://docs.vectara.com/docs/ |
| --- | --- |
| API playground | https://docs.vectara.com/docs/rest-api/ |
| Getting help | Join our [Discord](https://discord.gg/GFb8gMz6UH) server or [Discussion forums](https://discuss.vectara.com/) if you have questions. If you have any feedback for us, we would be glad to hear it - please let us know in the forums or our Discord channel.|
| Open source |We have created two useful open source projects to help:|
|| - [vectara-ignest](https://github.com/vectara/vectara-ingest) helps with data ingestion - crawling data sources and indexing them into Vectara.|
|| - [vectara-answer](https://github.com/vectara/vectara-answer) is a user interface for question answering - demonstrates a UI concept.|
|| - [React-search](https://github.com/vectara/react-search) is a React package that allows you to integrate Vectara semantic search in any React app with just a few lines of code.|
|| - [React-chatbot](https://github.com/vectara/react-chatbot) is a React package that allows you to integrate Vectara Chat in any React app with just a few lines of code.|
|| - [Create-UI](https://github.com/vectara/react-chatbot) is a fast way to generate a Vectara-powered sample codebase for a range of user interfaces.|
| Sample applications | We have quite a few "sample applications" hackers can take a look at https://vectara.com/demos/. Additionally, we published some sample code in these [jupyter notebooks](https://github.com/vectara/example-notebooks).|
| Blog posts | [A reference architecture for RAG](https://vectara.com/a-reference-architecture-for-grounded-generation/)|
|| [What is vector search?](https://vectara.com/vector-search-what-is-vector-search-and-how-does-it-work/) |
|| [RAG done right: chunking](https://vectara.com/grounded-generation-done-right-chunking/) |
|| [RAG done right: retrieval](https://vectara.com/blog/retrieval-augmented-generation-rag-done-right-retrieval/) |
|| [RAG done right: databases](https://vectara.com/blog/retrieval-augmented-generation-rag-done-right-database-data/) |
|| [Vectara Chat](https://vectara.com/blog/vectara-chat-revolutionizing-chat-development-for-the-modern-business/) |
|| [Vectara and Airbyte](https://vectara.com/blog/vectara-and-airbyte/) |
|| [Vectara and Unstructured](https://vectara.com/blog/building-genai-applications-with-vectara-and-unstructured/) |
| Youtube | Flowise + Vectara [Tutorial](https://youtu.be/OJK-jdFYn6I) |
|| Langflow + Vectara [Tutorial](https://www.youtube.com/watch?v=VP0NDf2C3Kg) |
|| Ask LangChain [video](https://youtu.be/ACQaSAJxoBs) |
|| More [here](https://www.youtube.com/channel/UCoP_hcyjJRLQr0CV050bfMg) |
| Integrations | LangChain: https://blog.langchain.dev/langchain-vectara-better-together/ |
|| LlamaIndex: https://vectara.com/llamaindex-vectara/ |
|| Vectara and Airbyte: https://vectara.com/blog/vectara-and-airbyte/ |
| Startup program | https://vectara.com/startups |

Happy Hacking!

## About Boomerang and HHEM

### What is the Boomerang embedding model?

Boomerang is the name of an embedding model from Vectara. This model encodes text from your data as “vector embeddings” and is used to power the high performance retrieval process that is part of the RAG pipeline.

Read more about [Boomerang](https://vectara.com/introducing-boomerang-vectaras-new-and-improved-retrieval-model/), and [the importance of using a good retrieval model](https://vectara.com/retrieval-augmented-generation-rag-done-right-retrieval/) for getting good results from RAG.

### Where is my customer ID / corpus ID / API key?

Here’s some info on [how to find your customer ID](https://docs.vectara.com/docs/quickstart#view-your-customer-id).

To get a corpus ID, view a corpus in the Console. The corpus ID is at the top of the screen, e.g. “Corpus ID: XXX”.

To create API Keys - follow this [guide](https://docs.vectara.com/docs/common-use-cases/app-authn-authz/api-keys).

### What is HHEM?

- HHEM stands for the “Hughes Hallucination Evaluation Model” and is an open source model created by Vectara, which can evaluate the likelihood a foundation model will hallucinate. 
It was named for Simon Hughes.
- Model card: https://huggingface.co/vectara/hallucination_evaluation_model
- Blog: https://vectara.com/blog/cut-the-bull-detecting-hallucinations-in-large-language-models/ 
- Leaderboard: https://huggingface.co/spaces/vectara/leaderboard

## Build it at an AI hackathon

Retrieval-augmented generation is a common pattern in an AI hackathon project that has to answer questions from your own data. With Vectara you ingest your data and then build apps with the Query and Summarization APIs, so more of the event goes to your idea. To find an event to try it in, see the list of [upcoming AI hackathons](/ai-hackathons/).

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build. None of the steps, code or commands was executed, and no output was checked. Running it needs: a Vectara account (a free plan is described, more capacity is paid), plus the customer ID, corpus ID and API key from that account. None of these was used here, so versions, prices, model names and links may have changed. Check each one before you start.
