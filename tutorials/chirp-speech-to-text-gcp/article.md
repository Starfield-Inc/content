---
title: "Chirp Tutorial: How to use Google's Chirp speech-to-text AI model on Google Cloud console."
seo_title: "Chirp speech-to-text tutorial on Google Cloud console"
meta_description: "AI hackathon tutorial: set up Google's Chirp speech-to-text model in the Google Cloud console and transcribe an audio file step by step."
---

## Introduction
[Chirp](https://cloud.google.com/blog/products/ai-machine-learning/bringing-power-large-models-google-clouds-speech-api) is Google Cloud's 2B-parameter speech model built via self-supervised training on millions of hours of audio and [28 billion sentences of text spanning 100+ languages](https://ai.googleblog.com/2023/03/universal-speech-model-usm-state-of-art.html). Chirp delivers 98% speech recognition accuracy in English and over 300% relative improvement in several languages with less than 10M speakers. 

## What we are going to do?
In this tutorial, we will learn how to effortlessly set up Google Cloud console to leverage the powerful Chirp speech-to-text AI model. This comprehensive tutorial provides step-by-step guide for an easy setup process and a quick start to use Chirp speech-to-text AI model. Sit back, relax, enjoy the tutorial and don't forget to make a cup of coffee ☕️.

### Learning outcomes
- How to use Google Cloud console.
- How to set up Google's Chirp speech-to-text AI model on Google Cloud console.

### We will cover the following steps:

1. Creating a Google Cloud account.
2. Creating a new project on the Google Cloud console.
3. Enabling the Speech API.
4. Creating an STT (Speech-to-Text) Recognizer using the Chirp model.
5. Creating a new Workspace for the project.
6. Performing a transcription on an audio file.
7. Viewing and downloading the transcription results.

### Prerequisites
Nothing! Just a cup of coffee ☕️ and a laptop 💻.

## Getting started

### Step 1: Create a Google Cloud account

First, we need to create a Google Cloud account. If you already have one, you can skip this step and [go here](https://cloud.google.com/). If you don't have one, you can create a free account [go here](https://cloud.google.com/free).

### Step 2: Create a new project

Next, we need to create a new project. On the top left corner click on the `project dropdown menu` > `New Project`.

Give your project a name and click `Create`.

### Step 3: Enable API

Go to [Speech](https://console.cloud.google.com/speech) in Google Cloud console. Click `ENABLE API`.

### Step 4: Create an STT Recognizer

Go over left sidebar navigation and click `Recognizers` > `CREATE RECOGNIZERS`. 

Give your recognizer a name `chirp-recognizer`. Select `Chirp` as the model. Select the language `en-US` in our case, leave the rest of the settings as default and click `Save`.

### Step 5: Create a new Workspace

Now, we need to create a new Workspace for our project. Go to `Workspace dropdown menu` and click `New Workspace`. You should see a sidebar pops up on the right side of your screen. 

From the Create a new workspace navigation sidebar, click `Browse` > `Create a new bucket`. Give your bucket a name `chirp-bucket` and click `Continue`.

Note: Rest of the settings are optional, you can leave them as default. 

Click `Create` and you should see that the new bucket is created.

Then, click `Select` > `Continue` > `Create` to finish creating your workspace for the speech-to-text UI.

Perfet! Now, we have a workspace for our speech-to-text UI. Let's move on to the next step.

### Step 6: Create a new Transcription

Let's perform a transcription on our actual audio file. 

Go over left sidebar navigation and click `Transcription` > `New Transcription`. From the `New Transcription` page, select your audio file through either uploading audio files `Local upload` or specifying an existing Cloud Storage file `Cloud storage`. 

In this tutorial, we will use the `Local upload` option with a short English audio file of your own.

Note: The UI will assess your audio file parameters automatically, and you can also specify them manually.

Click `Continue`. 

By default API version is set to `V1`, change it to `V2`, specify the language `English (United States) - en-US` in our case spoken in the audio file from the `dropdown menu`, then choose `Chirp` as transcription model and our newly created `chirp-recognizer` as the recognizer.

Click `Submit` and wait for a few seconds.

### Step 7: View Transcription Results and Download

To see the transcription results, click `the name of your transcription`.

You may also download the transcription results in 4 different formats: `JSON`, `TXT`, `SRT`, and `CSV`. Let's download the transcription results in `TXT` format. Click `Download` > `TXT` > `Download.

## Wrapping Up

This comprehensive guide has led you through implementing Google Chirp's speech-to-text AI model on the Google Cloud console. With step-by-step directions, you can now tap into Chirp's capabilities for precise speech recognition.

This AI tutorial aimed to provide a user-friendly, detailed roadmap for newcomers and experienced Google Cloud users alike.

Upon completing this tutorial, you should have the know-how required to apply Google Chirp's speech-to-text AI model effectively. Dive into Chirp's potential, incorporating it into projects and applications, and experiment with various languages and audio files.

## AI hackathon ideas

Speech-to-text is a common starting point for AI hackathon projects such as voice notes, meeting summaries and captioning tools. Put your newfound knowledge to the test at one of the [upcoming AI hackathons](/ai-hackathons/) from Starfield Labs.

## Frequently asked questions

**What does the tutorial cover?**
It covers creating a Google Cloud account and project, enabling the Speech API, creating a Chirp recognizer, creating a workspace, running a transcription on an audio file, and downloading the results.

**Which output formats can I download?**
The tutorial lists four: `JSON`, `TXT`, `SRT`, and `CSV`. It downloads `TXT`.

**Which API version and model settings does it use?**
It changes the API version from `V1` to `V2`, selects `Chirp` as the model, and uses the `chirp-recognizer` it created, with the language set to `en-US`.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, so no step has been tested here. Following it needs a Google Cloud account with a project, the Speech API enabled, and a Cloud Storage bucket, which may require billing to be set up. None of these was used.
