---
title: "Exploring the Power of Google AI Studio: A Comprehensive Guide"
seo_title: "Google AI Studio Guide: Prompts, Tuning and Gemini API"
meta_description: "AI hackathon prototyping guide to Google AI Studio: prompt types, model tuning, the Get Code button and the Gemini Cookbook."
---

# 🚀 Exploring the Power of Google AI Studio: A Comprehensive Guide

## Introduction

Welcome, fellow AI enthusiasts! 👋 Let's dive into [**Google AI Studio**](https://aistudio.google.com/), Google's very own browser-based IDE designed for prototyping with generative models. Whether you're a beginner or a seasoned developer, this tool allows you to experiment with various models and prompts and then export your projects to code via the Gemini API. Talk about making life easier, right?

### Key Features:
- **Prototyping with Generative Models:** Easily try out models and prompts.
- **Code Export:** Export projects directly to your preferred programming language.
- **Customization & Fine-tuning:** Tailor your model to your needs.

In this guide, I'll walk you through the awesome features of Google AI Studio, including prompt creation, model fine-tuning, and the potential applications of the Gemini models.

## API Key & Pricing

First things first, you'll need API keys for Gemini models. To get one, you just need to click the "Create an API key" button in the middle of the screen, select an existing Google project or create a new one, and you'll have your key ready in no time.
There is also a **free tier** to start with.

### **Gemini 1.5 Pro**:
- 2 RPM (Requests per minute)
- 32k TPM (Tokens per minute)
- 50 RPD (Requests per day)

### **Gemini 1.0 Pro**:
- 15 RPM
- 32k TPM
- 1500 RPD

For a free tier, this is pretty good if managed properly. If you outgrow these limits, there's a [**pay-as-you-go**](https://ai.google.dev/pricing) model:
- **Gemini 1.5 Pro:** $7 per million input tokens, $21 per million output tokens.
- **Gemini 1.0 Pro:** $0.5 per million input tokens, $1.5 per million output tokens.

> 💡 **Tip:** Use the higher limits of Gemini 1.0 Pro for broader testing, then refine your prompts and fine-tune with Gemini 1.5 Pro for more advanced results.

## 🌟 Main Features of Google AI Studio

Google AI Studio offers three main ways to experiment with prompts and fine-tune models, with seamless integration to save experiments in your Google Drive.

### 1. Create a New Prompt

Let's start with the prompt creation page, which is the playground for your imagination! You can choose from three types of prompts:

#### **Chat Prompt**
Simulate back-and-forth conversations with models in a chat interface. The options include:
- System prompt definition
- Model selection (Gemini 1.0 Pro, Gemini 1.5 Pro, or fine-tuned models)
- Temperature and top-P parameters (not available for Gemini 1.5)
- JSON format response option
- Adjust safety settings (e.g., harassment, hate, explicit content)

The safety settings are particularly cool, allowing you to block categories of sensitive content ranging from "Block None" to "Block Most." This feature is crucial for regulating potentially dangerous prompts that could lead to undesirable behavior in your application.

Google AI Studio lets you customize these safety settings according to your needs. Whether you want to block specific content entirely or relax restrictions for testing purposes, having this level of control makes Google AI Studio incredibly versatile and user-friendly.

> **Note:** Using Gemini 1.5 Pro, you can insert images, videos, audio, and files, which the model can interpret. For instance, ask questions about different parts of an image or analyze video content. I had a blast using this feature!

#### **Freeform Prompt**
Got a creative idea and want to see how the model handles it? The Freeform prompt option lets you write a prompt (with support for media insertion for Gemini 1.5 Pro) and then lets the model auto-continue. 

This feature is perfect for creative text generation, storytelling, and even interactive fiction! I've experimented with writing short stories and brainstorming blog topics using this prompt type, and it's incredibly versatile.

#### **Structured Prompt**
Want to give your model more direction? The structured prompt feature is a good choice. It allows you to create complex prompts in a tabular form, providing the model with a few-shot example set using input/output pairs.

This approach is fantastic for tasks like classification (e.g., categorizing user reviews) or predicting sentiment. It's like a trial run before fine-tuning, helping you gauge the model's behavior with up to 500 examples. If fine-tuning feels like overkill, this prompt form can keep the few-shot examples within the structure.

### 2. Tune Models

**Model Tuning** is where Google AI Studio really shines. You can refine a model using structured prompts and import datasets via CSV files or Google Sheets directly from your Drive.

Before training starts, you can set advanced settings like:
- **Epochs:** Number of times the dataset is used (default: 5). A higher number means the model will learn more from your data but could lead to overfitting if too high.
- **Learning Rate Multiplier:** Affects how quickly the model adapts (default: 1). Too high a rate might lead to unstable training, while too low may result in slow learning.
- **Batch Size:** Number of samples per gradient update (default: 4). Larger batches can lead to faster training but require more memory.

After training, you can review performance metrics specifically loss per epoch. Once tuning is complete, your model will be available for use in Freeform and Structured Prompts.

In my experience, tuning models with a few dozen examples drastically improved the output quality for my use cases, like sentiment analysis and classification tasks.

### 3. 🖼️ Prompt Gallery
Not sure where to start? The **Prompt Gallery** is your friend! This is a treasure trove of pre-set prompts that you can use to kickstart your experiments. With just a few clicks, you'll have ready-made prompts covering various tasks and domains.

### 🔍 A Useful Feature: "Get Code" Button

> 🗒️ **Fun Fact:** Some warnings can be displayed in the model output. When clicked these are labelled as: "Probability of Unsafe Content - Sexually Explicit - Warning: Medium." Interestingly, nothing in the model's output seems to fall within this category, suggesting that the model is either extra careful or freely issues these warnings even when not entirely applicable. It's a helpful feature, providing insight into how the model evaluates safety.

At the top right of each prompt interface is the **"Get Code"** button. When you click it, you'll receive the full configuration of your prompt, including all settings, system prompts, chat history, or examples, depending on the prompt type. 

And it's all in code, ready to be added to your project in any of the following languages:

- **cURL**
- **JavaScript**
- **Python**
- **Android Kotlin**
- **Swift**

I found this feature incredibly useful, as it allows you to seamlessly transition from experimentation to implementation. It makes sharing your prompts with other developers or replicating them in your projects super easy.

## 📚 The Gemini Cookbook
The [**Gemini Cookbook**](https://github.com/google-gemini/cookbook) is a collection of guides and examples for the Gemini API. It includes quickstart tutorials for writing prompts, exploring different features, and examples of applications you can build.

### Examples:
- **Classification and Labeling**
- **Summarization and Extraction**
- **Conversational Agents**
- **Interactive Data Exploration**

## Conclusion
**Google AI Studio** is a fantastic tool for experimenting with generative models. Combined with the **Gemini Cookbook**, it enables rapid prototyping and application development with Gemini models. Whether you're building chatbots, classifiers, or creative applications, this IDE offers everything you need to get started. 🌟

In my experience, Google AI Studio is more than just a tool—it's part of an entire ecosystem that Google has built with products like Vertex AI platform and the Gemini Model Family, to enable AI developers to quickly test, refine, and bring their ideas to life. This, together with other Google assets like GCP, gives you everything you need to build amazing applications and ideas, from prototyping to production-grade solutions.

So what are you waiting for? Give it a spin and unleash your creativity! 🚀

## Build it at an AI hackathon

Google AI Studio lets you try prompts in the browser before you write any code, which suits the short build time of an AI hackathon. You can test a prompt, export it with the Get Code button and drop it into your project. To find an event to build in, see the list of [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

### How do I get a Gemini API key?

Click the "Create an API key" button in the middle of the screen, select an existing Google project or create a new one, and the key is ready.

### What are the three prompt types?

Chat prompts simulate a back-and-forth conversation, Freeform prompts let you write a prompt and have the model auto-continue, and Structured prompts give the model input/output example pairs in a table.

### How do I move a prompt into my project?

Use the "Get Code" button at the top right of each prompt. It returns the full configuration as code in cURL, JavaScript, Python, Android Kotlin or Swift.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build. None of the steps, code or commands was executed, and no output was checked. Running it needs: a Google account, a Google project and a Gemini API key (a free tier exists and a pay-as-you-go tier is described), and Google Drive to save experiments. None of these was used here, so versions, prices, model names and links may have changed. Check each one before you start.
