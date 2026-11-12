---
title: "OpenAI Whisper tutorial: How to use Whisper to transcribe a YouTube video"
seo_title: "Transcribe a YouTube Video with OpenAI Whisper"
meta_description: "AI hackathon tutorial: download YouTube audio with Pytube and transcribe it with OpenAI Whisper in a few lines of Python."
---

## Unraveling Whisper: OpenAI's Speech Recognition System

[OpenAI Whisper](https://github.com/openai/whisper) is OpenAI's speech recognition solution, trained with 680,000 hours of web-sourced multilingual and multitask data. This extensive dataset bolsters increased resistance to accents, ambient noise, and technical jargon. Additionally, it supports transcribing in numerous languages and translating them into English. Distinct from DALLE-2 and GPT-3, Whisper is a free and open-source model. OpenAI delivers access to its models and codes, fostering the creation of valuable speech recognition applications.

## Mastering YouTube Video Transcription with Whisper

Throughout this Whisper tutorial, you'll gain expertise in utilizing Whisper to transcribe a YouTube video. We'll employ the Python package "Pytube" to download and convert the audio into an `MP4` file. Visit [Pytube's repository](https://github.com/pytube/pytube) for more information.

First, we need to install the Pytube Library. You can do this by running the following command in your terminal:

```bash
!pip install --upgrade pytube
```

For this tutorial I'll be using [this](https://www.youtube.com/watch?v=x7X9w_GIm1s) "Python in 100 Seconds" Video. 

Next, we need to import Pytube, provide the link to the YouTube video, and convert the audio to `MP4`:

```python
#Importing Pytube library
import pytube

# Reading the YouTube link
video = "https://www.youtube.com/watch?v=x7X9w_GIm1s"
data = pytube.YouTube(video)

# Converting and downloading as 'MP4' file
audio = data.streams.get_audio_only()
audio.download()
```

The output is a file named like the video title in your current directory. In our case, the file is named `Python in 100 Seconds.mp4`
Now, the next step is to convert audio into text. We can do this in three lines of code using whisper. First, we install and import 
whisper. Then we load the model and finally we transcribe the audio file.

### Installing Whisper libary
```bash
!pip install git+https://github.com/openai/whisper.git -q
```

```python
import whisper
```

Load the model. We'll use the "base" model for this tutorial. You can find more information about the 
models [here](https://github.com/openai/whisper/blob/main/model-card.md). Each one of them has tradeoffs between 
accuracy and speed (compute needed).

```python
model = whisper.load_model("base")
text = model.transcribe("Python in 100 Seconds.mp4")
```

And now we can print out the output.

```python
#printing the transcribe
text['text']
```

## Build it at an AI hackathon

Turning a video into text is a quick first step for many AI hackathon projects, such as summaries, search or captions. Here the whole pipeline is a few lines of Python in a notebook. To find an event to try it in, see the list of [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

### Which library downloads the YouTube audio?

The Python package Pytube, which downloads the audio and saves it as an `MP4` file.

### Which Whisper model does the tutorial use?

The "base" model. Each model has tradeoffs between accuracy and speed (compute needed), and the Whisper model card has more information.

### What does the download produce?

A file named like the video title in your current directory. In the example the file is `Python in 100 Seconds.mp4`.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build. None of the steps, code or commands was executed, and no output was checked. Running it needs: Python in a Jupyter notebook or Colab, the Pytube and Whisper packages, and a model download. No API key is used. None of these was used here, so versions, prices, model names and links may have changed. Check each one before you start.
