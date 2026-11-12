---
title: "Cohere tutorial: How to use Cohere Playground"
seo_title: "Cohere Playground tutorial: generate, embed, classify"
meta_description: "AI hackathon tutorial: a quick tour of the Cohere Playground, covering the Generate, Embed and Classify tabs, parameters and code export."
---

## Why should I use Cohere playground?

Hello! This is a Cohere tutorial on how to use the Cohere Playground. Co:here is a powerful neural network, which can generate, embed, and classify text.

If you just want to check something fast and don't want to create a new project on your computer, you can use the Playground. It's a great way to test out Cohere's features and see how they work, as well without spending too much time on setting everything up! And why not use the Cohere API to use tested solutions in your app?

## 🚀 Let's start!

First of all, register to [Cohere]( https://dashboard.cohere.ai/register)

After registration you need to head over to the [Cohere Playground](https://os.cohere.ai/playground)

On the top you will see the 3 main tabs: **Generate**, **Embed** and **Classify**.


On each main tab on the left side you will see Example presets. This is a big help from Cohere to get you started. You can use these examples to get a better understanding of how Cohere works, how prompts are working


## Generate

Let's take an example on the **Generate** tab. You can see example preset Blog Posts.


```python
This program will generate an introductory paragraph to a blog post given a blog title, audience, and tone of voice.
--
Blog Title: Activities in Toronto
Audience: Millennials
Tone of Voice: Lighthearted
First Paragraph: Looking for fun things to do in Toronto? When it comes to exploring a major Canadian city, there's an ever-evolving set of activities to choose from. Whether you're looking to visit a local museum or sample the city's varied cuisine, there is plenty to fill any itinerary. In this blog post, I'll share some of my favorite recommendations
--
Blog Title: Mastering Dynamic Programming
Audience: Developers
Tone: Informative
First Paragraph: In this piece, we'll help you understand the fundamentals of dynamic programming, and when to apply this optimization technique. We'll break down bottom-up and top-down approaches to solve dynamic programming problems.
--
Blog Title: How to use Cohere's Playground
Audience: Athletes
Tone: Enthusiastic
First Paragraph:
```
At the beginning we are giving two examples for the model to learn from separated by `--` stop sequence that we are setting on the right side.
We can change the blog title at the end to "How to use Cohere's Playground" and click Generate on the right bottom corner.


On the right side of the screen we have the **PARAMETERS** tab. Here we can choose what size of model we want to use. Smaller the model the faster the generation will be.
We can also choose the temperature of the model. The higher the temperature the more random the output will be.
We can also choose the number of tokens we want to generate.
Frequency penalty is a way to penalize the model for repeating the same words. The higher the frequency penalty the less likely the model will repeat the same words.


Code can be exported in many languages Python, node.js, go, curl, cli. So basically you can just copy the code into your project and you are good to go :)
You can also share your playground state with others, by clicking on the share button.
And on the bottom you can save the state for yourself

## Easy, right?

I hope you enjoyed this short introduction to Cohere's Playground.

## AI hackathon ideas

If you want to build a Cohere-based app in a couple of days, an AI hackathon is a good way to do it, with a team and a deadline. Starfield Labs runs AI hackathons for builders of all levels. Browse the [upcoming AI hackathons](/ai-hackathons/) to find one.

Thank you and have fun!

**You might want to read more :) :**
+ https://docs.cohere.ai/docs/playground-overview
+ https://docs.cohere.ai/docs/the-cohere-platform

## Frequently asked questions

**What are the main tabs in the Playground?**
Generate, Embed and Classify. Each tab has example presets on the left to help you get started.

**Which parameters can I change on the Generate tab?**
The model size, the temperature, the number of tokens to generate, and the frequency penalty. The tutorial says a higher temperature makes output more random and a higher frequency penalty makes repeated words less likely.

**Can I reuse what I build in the Playground?**
Yes. The tutorial says code can be exported in Python, node.js, go, curl and cli, and that the Playground state can be shared or saved.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, so no step has been tested here. Following it needs a Cohere account (the Playground may require an API key or usage limits). Nothing was registered or used. None of these was used.
