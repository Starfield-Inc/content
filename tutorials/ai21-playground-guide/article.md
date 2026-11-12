---
title: "AI21 Labs tutorial: How to use the Playground"
seo_title: "AI21 Studio Playground Guide for AI Hackathons"
meta_description: "AI hackathon tutorial on the AI21 Studio Playground: presets, Jurassic-1 models, temperature, top p, the Rewrite and Summarize APIs."
---

## What is AI21 Studio?

An AI development platform called AI21 Studio was created to make it simpler and more economical for companies to build, train, and use Natural Language Processing (NLP) applications. AI21 Studio's simple drag-and-drop user interface makes it easy to develop AI models. Additionally, it gives users access to Jurassic-1, a sizable language model, allowing companies to swiftly put models into production. AI21 Studio also provides a range of capabilities, including automatic model versioning, model management, data exploration, and monitoring, to assist users in managing their models and data. Organizations can also cooperate on projects with their teams using AI21 Studio.

## What is an AI playground?

An intuitive, web-based interface is offered by the AI21 Studio Playground to assist developers in creating and testing their models. The interface has two principal sections: the main view and the sidebar. The code editor and model training output are both available in the main window, where programmers can write Python code and use the [AI21 Studio APIs](https://www.ai21.com/studio). Access to data sets, training materials, and documentation are all available on the sidebar to aid developers in making the most of the platform.

A number of tools are also available in the AI21 Studio Playground to aid developers in creating and testing their models. Users are able to build new data sets, conduct experiments, and monitor their development. To aid developers in understanding model performance, the platform also offers graphics like heatmaps and graph visualizations. Additionally, the Playground has an interactive debugger that aids developers in finding and fixing issues. The platform is often updated with new features and problem fixes.

## Using the Playground in an AI hackathon

A hosted playground lets a team compare models and prompts before writing any code, which saves time in an AI hackathon. You can then export a working preset to code and build on it. When you are ready to apply what you learn, see the [upcoming AI hackathons](/ai-hackathons/).

## How can I start?

You must first create an account and [sign up](https://studio.ai21.com/sign-up) for a free trial of AI21 Studio before using it. If you're unfamiliar with AI21 Studio, this will grant you access to the Playground, which is a good place to start. You may test out numerous platform models and features as well as the API in the playground. Before digging into the more advanced possibilities, you can use the playground to get acquainted with the platform and its features. When you feel comfortable using the platform, you may start making your own projects and experimenting with its more sophisticated features.

## Complete API

The Complete API gives access to Jurassic-1 (J1), the first generation in a series of AI21's language models.

- Playground: https://studio.ai21.com/playground/complete
- Docs: https://docs.ai21.com/docs/complete-api

### Using Presets

Presets are ready made templates/examples that you can use to get started with the API. AI21 provides many presets to get started with: Chat, Classification, Code, Info extraction, Long Form, Named entity recognition, Q & A, Rewrite, Short form, Summarize.

### Choosing a model

You can choose from 4 models that AI21 provided and additionally you can customize the Jurassic-1 model.
- j1-large (7.5B)
- j1-grande (17B)
- j1-grande-instruct (beta) (17B)
- j1-jumbo (178B)

These sizes are in billions of parameters.

### Maximum completion length

You can choose how long the completion should be. The default is 20 tokens. https://docs.ai21.com/docs/when-the-generation-stops#-set-completion-length-parameters

### Temperature

Temperature is a parameter that controls the randomness of predictions. Lowering the temperature results in less random completions. The default value is 0.8. https://docs.ai21.com/docs/sampling-from-language-models

### Top p

The percentile of probability from which tokens are sampled. We limit the total cumulative probability from which to sample.

### Stop sequence

Generation is terminated at the moment when the model generates any of the stop sequences. Choose it properly as it can help you avoid generating unnecessary tokens.

### Repetition penalties

Repetition penalties are used to stop the model from simply copying words from the prompt and repeating them over and over. This is done by adjusting the probability of certain words being generated so that words that have already been used are less likely to appear again.

- Repetition penalty: The penalty for repeating a word. The default value is 0
- Count penalty: Reducing probability of generating new tokens that appeared in the prompt or in the completion
- Frequency penalty: Reducing probability of generating new tokens that appeared in the prompt or in the completion, proportional to the appearance frequency.

## Rewrite API

AI21 Studio's Rewrite API gives you access to a paraphrasing technology. It was created for the purpose of paraphrasing and has been optimized for that purpose, which makes it simpler to incorporate into your systems than building the feature yourself.

This API takes a piece of text, rewrites it using different words, and returns a list of paraphrases that mean the same thing. It has specialized features to help you customize the output, like adjusting the tone, or rewriting only certain parts of the text while keeping the context.

Here there are also presets to get started with. You can even choose the tone you would like to use.

## Summarize API

It does what you would expect: it summarizes the text you give it. It is useful for people who want to read a lot of text but don't have the time to do so, or who want a quick overview of a text. It was fine-tuned for summarization and has been optimized for this purpose.

## Generating text, saving Presets, Export to code, Share Presets

In the bottom section of the Playground you can generate text, save presets, export to code and share presets. You can also use the API in your own code. You can also see how many tokens you used in your prompt.

## Summary

AI21 Playground lets users build and test models quickly. It offers a user-friendly interface that makes AI approachable with no prior programming skills. With the help of the Playground, developers can experiment with AI development and deploy their models. You don't always have to use a single provider's API everywhere - different AI can fit different needs. Give the AI21 Playground a try and see where it takes your project.

## Frequently asked questions

**What is the AI21 Studio Playground?**

It is an intuitive, web-based interface offered by AI21 Studio to help developers create and test their models. You can try the platform's models and features, and the API, in the Playground.

**How do I start using it?**

Create an account and sign up for a free trial of AI21 Studio. That gives you access to the Playground, where you can get acquainted with the platform before starting your own projects.

**Which models can I choose from in the Complete API?**

You can choose from four models: j1-large (7.5B), j1-grande (17B), j1-grande-instruct (beta, 17B) and j1-jumbo (178B). You can also customize the Jurassic-1 model.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, and no step in it has been tested here. To follow it you need an AI21 Studio account (free trial, later possibly paid). No account or API was used for this write-up.
