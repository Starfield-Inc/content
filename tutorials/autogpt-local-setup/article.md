---
title: "AutoGPT tutorial: How to set up AutoGPT"
seo_title: "AutoGPT Setup Guide for AI Hackathon Builders"
meta_description: "AI hackathon guide to AutoGPT: install it on your computer, add an OpenAI key, run it with Docker, and give the agent a voice and images."
---

Are you ready to dive into the world of AutoGPT and generative models? By the end of this tutorial, you'll be well-versed in setting up AutoGPT and understanding its relationship with generative models, no matter your field of expertise.

## What is AutoGPT and how is it related to Generative Agents?

So, what's the deal with AutoGPT? Simply put, it's an AI model designed for various tasks like text generation, translation, and other wonders. It works its magic using a technique called Generative Pre-trained Transformer (GPT), which is a type of generative model.

Now, let's talk about generative models. They're AI models that can generate new data based on the patterns they've learned from existing data. Think of them as the master artists of the AI world, creating new, never-before-seen masterpieces.

In a nutshell, AutoGPT and generative models are like PB&J. They work together to bring forth the power of AI, enabling us to tackle a wide array of problems.

Setting up AutoGPT is much like assembling a jigsaw puzzle - you need to get all the pieces in the right place. First, you'll need to acquire a pre-trained GPT model, which you can do by browsing popular repositories like GitHub. Once you have the model, you can customize it according to your specific task by fine-tuning its parameters.

## AutoGPT in an AI hackathon

An autonomous agent that plans and acts toward a goal is a natural fit for an AI hackathon project. Setting AutoGPT up locally gives you a working agent to experiment with before you build your own. When you are ready to test your skills, see the [upcoming AI hackathons](/ai-hackathons/).

## Prerequisites

Before starting with AutoGPT, you need to install:

1. **Python**: Download from the official [Python website](https://www.python.org/downloads/). During installation, remember to check the box that adds Python to PATH.

2. **Git** (Optional): Git is used for cloning the AutoGPT repository. To install Git, download it from its official [website](https://git-scm.com/downloads). If you prefer not to use Git, you can manually download the repository as a .zip file. (Refer to **Step 1 Option B** for this)

## Installation Guide for AutoGPT

### Step 1: Obtain the AutoGPT repository
#### Option A: Cloning with Git (Recommended)
For Git users, start by going to your the Windows terminal or the Mac/Linux Terminal. Navigate to the folder where you want to clone the AutoGPT repository. You can clone the repository by using the following git command:

```bash
git clone https://github.com/Significant-Gravitas/Auto-GPT.git
```
#### Option B: Download and extract the .zip file
If you chose not to install Git, navigate to the [AutoGPT repository](https://github.com/Significant-Gravitas/Auto-GPT) on your web browser. Click on `Code` and then `Download ZIP`. Once the zip file is downloaded, extract it and place the contents into your preferred directory.

`Note`: Download the latest [stable release](https://github.com/Significant-Gravitas/AutoGPT/releases/latest). The master branch is under heavy development and may often be in a broken state.

### Step 2: Navigate to the AutoGPT directory

Navigate to the newly created AutoGPT directory with the following command:

```bash
cd Auto-GPT
```

### Step 3: Install the required packages

AutoGPT requires several Python packages, including Transformers and Torch. Use the `requirements.txt` file in the AutoGPT directory to install these packages:

```bash
pip install -r requirements.txt
```

If any permission-related errors occur, use the `--user` tag:

```bash
pip install -r requirements.txt --user
```

### Step 4. Give AutoGPT access to your API keys

For AutoGPT to work it needs access to GPT-4 (GPT-3.5 can also work but will return less favorable results and has a higher tendency to hallucinate). To configure the settings for AutoGPT you need to set it up with your own API key. If you don't have one you can get it from [OpenAI's website](https://platform.openai.com/account/api-keys). For this you will need to create a new account (if you don't have one already) and click "Create new secret key".

You can then give a name to your key, something like AutoGPT, and click create.

Remember to keep your key safely stored since you won't be able to see it after this (you can always create a new one and change it in the configurations file). Never commit the `.env` file to Git or share it, and keep an eye on your usage, because an autonomous agent can make many paid API calls.

### Step 5: Configure `env.template`

The `env.template` primarily contains commented (inactive) lines. One of the active lines says `SMART LLM MODEL` followed by `Default: gpt-4.`. Change `gpt-4` to `gpt-3.5`, save the file and rename it to `.env`.

### Step 6: Start AutoGPT

Now, you can start AutoGPT using the command:

```bash
python -m autogpt
```

## Using Docker

Preferring Docker? Here's how to prepare your environment:

```bash
docker build -t autogpt .
```

This command builds a Docker image. Once completed, run:

```bash
docker run -it --env-file=./.env -v $PWD/auto_gpt_workspace:/app/auto_gpt_workspace autogpt
```

If you've installed Docker Compose, use these commands:

```bash
docker-compose run --build --rm auto-gpt
```
Or

```bash
docker-compose run --build --rm auto-gpt --gpt3only --continuous
```

Now that the agent is running, you have to give it a name (or by default it will be named "Entrepreneur-GPT"), define the role of the AI and the goals it wishes to accomplish one by one, and there you have it.

## Give your Agent a voice

AutoGPT can even speak. Let's see how to set up this feature.

## Step 1: Get your API key from ElevenLabs

Head to ElevenLabs and create a free starter account. At the top right click your profile image, then select Profile. Locate your API key on that page and copy it.

### Step 2: Give access to your Agent to its new found voice

Open your .env file and replace "your-elevenlabs-api-key" with the API key you just copied and "your-voice-id-1" with either the name of the voice you wish to use (e.g. "premade/adam"). You can find a list of the available voices on ElevenLabs' Speech Synthesis page. You can also use the ID of a voice instead, which you can get from the voice list on that page. The values to replace are in the ElevenLabs lines of your .env file.

## Step 3: Run the speak command

The last step to hear your Agent speak, you just need to run the following command in your terminal

```
python -m autogpt --speak
```

But there is one more feature. An agent that can remember things and also speak can also generate images.

## How to give your Agent the ability to generate images

## Step 1: Set your image provider
The most straightforward option to set up is DALL-E, so go to your .env file and make sure that IMAGE_PROVIDER is set to "dalle".
You can also set the image size to different values, your options are 256, 512 and 1024. Just change the value of IMAGE_SIZE in your .env file.

Finally, sit back and watch your agent create some content.

That covers setting up AutoGPT and its relationship with generative models. Keep exploring.

## Frequently asked questions

**What do I need to install before setting up AutoGPT?**

You need Python, with the box that adds Python to PATH checked during installation. Git is optional, because you can download the repository as a .zip file instead.

**Which model does AutoGPT need, and how do I give it access?**

AutoGPT needs access to GPT-4. GPT-3.5 can also work but returns less favorable results and hallucinates more. Create your own API key on OpenAI's website, put it in the `.env` file (renamed from `env.template`), and keep it stored safely.

**Can I run AutoGPT with Docker?**

Yes. Build the image with `docker build -t autogpt .`, then run it with `docker run -it --env-file=./.env -v $PWD/auto_gpt_workspace:/app/auto_gpt_workspace autogpt`. Docker Compose commands are also shown above.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, and no step in it has been tested here. To follow it you need Python, optionally Git and Docker, a paid OpenAI API key, and optionally an ElevenLabs account and API key for the voice feature. None of these was used and no command was run for this write-up.
