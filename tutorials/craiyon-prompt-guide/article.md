---
title: "Craiyon tutorial: text-to-image generation prompt guide"
seo_title: "Craiyon Tutorial: Text-to-Image Prompt Guide"
meta_description: "AI hackathon tutorial: learn how Craiyon turns text into images and how style, composition and mood words improve your prompts."
---

## Introducing Craiyon: Revolutionizing AI-Driven Image Generation

In the realm of AI image creation, OpenAI's DALL·E sparked a wave of innovation. Craiyon (formerly Dalle-e Mini) represents an open-source endeavor to replicate these impressive results. Accessible and free, this trailblazing model has no limitations on image generation, rendering visual wonders at craiyon.com.

## How does Craiyon work? - simple explanation

Basically Craiyon looks at millions of images from the internet with their associated captions and determines repeating and identity-forming patterns from these images. (The AI determines what is common to all images.) Over time, Craiyon then determines what makes up these images. Once Craiyon has completed this,it can create its own new images, since it now knows what constitutes a word or phrase. Here it must be said, of course, that Craiyon  does not really understand the words entered, but only tries to reproduce the essence of the words in images.
Several models are combined together to achieve these results: [detailed resource](https://wandb.ai/dalle-mini/dalle-mini/reports/DALL-E-Mini-Explained-with-Demo--Vmlldzo4NjIxODA)
- an image encoder that turns raw images into a sequence of numbers with its associated decoder
- a model that turns a text prompt into an encoded image
- a model that judges the quality of the images generated for better filtering 

## Craiyon in action

Go to www.craiyon.com. There you will find an input field for your prompts. Type in something interesting like “spaceship flying to mars”, click generate and you will get the generation results about 20 seconds later. 

In order to get better results you can use the following prompt tips: 

### Add art style descriptions

There are a million different art styles out there, each with their own unique flair. Some are realistic, while others are more abstract. Some are calm and serene, while others are chaotic and wild. It's up to you, the artist, to decide what style you want to use for your piece. 

- Artist style like “Picasso”, “Van Gogh”
- Tools used like “watercolors”, “oil painting”
- Styles: “Impressionism”, “Expressionism”, “Abstract”

### Add composition descriptions

Composition refers to the overall physical arrangement of objects in the artwork. In other words, composition refers to how the various elements of the painting are arranged within the picture frame.

- “aerial view” or “long shot” or “portrait” or “wide-angle” or “fish-eye lens” or “extreme close-up” or “macro” or “bokeh.”
- Merge objects: 
“looks like” or “in the shape of” , “inside of” or “next to” 

### Add atmosphere/mood descriptions

The atmosphere or mood of an artwork can be just as important as the subject matter. After all, how the artist chooses to portray the subject can have a big impact on how the viewer perceives it.
- “dark” or “colorful” or “futuristic” or “vintage” or “abstract” or “soothing” or “foggy” or “early morning” or childish.”

If you want to learn more about how to structure your prompt to get better results, these are two resources on prompt engineering: 

- [Dalle-2 prompt engineering guide - Google Docs](https://docs.google.com/document/d/11WlzjBT0xRpQhP9tFMtxzd0q6ANIdHPUBkMV-YB043U/edit)
- [Prompt book - Slideshow](https://pitch.com/v/DALL-E-prompt-book-v1-tmd33y)

## Wrapping Up: Unleashing the Power of Craiyon

Craiyon dazzles as an accessible and user-friendly solution for transforming text into captivating visuals. Throughout this engaging Craiyon tutorial, we've showcased image generation techniques, prompt structures for optimal results, and invaluable tips in prompt engineering. Now it's your chance to conjure spectacular creations.

### More resources

- https://github.com/borisdayma/dalle-mini
- https://huggingface.co/spaces/dalle-mini/dalle-mini

## Build it at an AI hackathon

Prompt practice pays off quickly under a deadline, and an AI hackathon is a good place to try image generation ideas with a team. Starfield Labs lists [upcoming AI hackathons](/ai-hackathons/) where you can put these prompt tips to use.

## Frequently asked questions

**How does Craiyon work?**

Craiyon looks at millions of images from the internet with their captions and finds repeating patterns in them. It then uses that to create new images from a prompt. It does not really understand the words entered; it only tries to reproduce the essence of the words in images.

**How long does a generation take?**

After you type a prompt on craiyon.com and click generate, the tutorial says you get the results about 20 seconds later.

**How can I get better results from my prompts?**

Add art style descriptions (an artist, a tool such as watercolors or oil painting, or a style such as Impressionism), composition descriptions (such as aerial view or macro) and atmosphere or mood descriptions (such as foggy or vintage).

## How this tutorial was tested

This tutorial was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, so no step in it has been tested here.

To follow it you would need: access to the Craiyon website in a browser. No account, API key, GPU or wallet is named in the tutorial. None of these was run or used for this build.
