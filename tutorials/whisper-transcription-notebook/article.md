---
title: "OpenAI Whisper tutorial: How to use OpenAI Whisper"
seo_title: "OpenAI Whisper Tutorial: Transcribe Audio in Python"
meta_description: "AI hackathon tutorial: install OpenAI Whisper, load the base model and transcribe an audio file in a Jupyter notebook."
---

## Introducing Whisper: OpenAI's Groundbreaking Speech Recognition System

Whisper stands tall as OpenAI's cutting-edge speech recognition solution, expertly honed with 680,000 hours of web-sourced multilingual and multitask data. This robust and versatile dataset cultivates exceptional resilience to accents, ambient noise, and technical terminology. Furthermore, it supports seamless transcription in various languages and translation into English. OpenAI graciously unveils models and codes, paving the way for ingenious developers to construct valuable applications that harness the remarkable potential of speech recognition.

## How to use Whisper

The whisper model is available on GitHub. You can download it with the following command directly in the Jupyter notebook:

```bash
!pip install git+https://github.com/openai/whisper.git 
```

Whisper needs `ffmpeg` installed on the current machine to work. Maybe you already have it installed, 
but its likely your local machine needs this program to be installed first. 

OpenAI refers to multiple ways to install this package, but we will be using the Scoop package manager.
 [Here](https://www.wikihow.com/Install-FFmpeg-on-Windows) is a tutorial
how to do it manually

In the Jupyter Notebook you can install it with the following command:

```bash
irm get.scoop.sh | iex
scoop install ffmpeg
```

After the installation a restart of is required if you are using your local machine.

Now we can continue. Next we import all necessary libraries:

```python
import whisper
import os
import numpy as np
import torch
```

Using a GPU is the preferred way to use Whisper. If you are using a local machine, you can check 
if you have a GPU available. 
The first line results `False`, if Cuda compatible Nvidia GPU is not available and `True` if it 
is available. The second line of 
code sets the model to preference GPU whenever it is available.

```python
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
```

Now we can load the Whisper model. The model is loaded with the following command:

```python
model = whisper.load_model("base", device=DEVICE)
print(
    f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
    f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
)
```

Please keep in mind, that there are multiple different models available. You can find all of them 
[here](https://github.com/openai/whisper/blob/main/model-card.md).
Each one of them has tradeoffs between accuracy and speed (compute needed). We will use the 
'base' model for this tutorial.

Next you need to load your audio file you want to transcribe. 

```python
audio = whisper.load_audio("audio.mp3")
audio = whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio).to(model.device)
```

The `detect_language` function detects the language of your audio file:

```python
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")
```

We transcribe the first 30 seconds of the audio using the DecodingOptions and the decode command. 
Then print out the result:

```python
options = whisper.DecodingOptions(language="en", without_timestamps=True, fp16 = False)
result = whisper.decode(model, mel, options)
print(result.text)
```

Next we can transcribe the whole audio file.
  
```python
result = model.transcribe("../input/audiofile/audio.mp3")
print(result["text"])
```

This will print out the whole audio file transcribed, after the execution has finished.

## But how can I leverage this knowledge?

Now it's up to you to create your own Whisper application. Get creative and have fun!  
I'm sure you will find a lot of useful applications for Whisper. A good way is to identify a problem around you and craft a solution to it.

## Build it at an AI hackathon

A speech-to-text project is a practical thing to build in an AI hackathon, where a working demo matters more than polish. Starfield Labs lists [upcoming AI hackathons](/ai-hackathons/) if you want a deadline and a team for your Whisper idea.

## Frequently asked questions

**Do I need a GPU to run Whisper?**

A GPU is the preferred way to use Whisper, but it is not required. The code sets the device to "cuda" when a CUDA-compatible Nvidia GPU is available and to "cpu" otherwise.

**Why does Whisper need ffmpeg?**

Whisper needs `ffmpeg` installed on the machine to work. The tutorial installs it with the Scoop package manager on Windows and points to other ways to install it.

**Which Whisper model does the tutorial use?**

It uses the 'base' model. There are several models, each with a tradeoff between accuracy and speed (the compute needed), and they are listed in the Whisper model card.

## How this tutorial was tested

This tutorial was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, so no step in it has been tested here.

To follow it you would need: Python and a Jupyter notebook, `ffmpeg`, an audio file, and optionally an Nvidia GPU. No API key or paid service is named. The Scoop installer and pip packages were not installed or run. None of these was run or used for this build.
