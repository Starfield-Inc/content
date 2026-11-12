---
title: "Google Colab tutorial: How to create your own AI image generator"
seo_title: "Build an AI Image Generator in Google Colab"
meta_description: "AI hackathon tutorial: build your own AI image generator in Google Colab with Stable Diffusion and the diffusers library in a few steps."
level: not stated
time: not stated
---

## Image Generators Uncovered: Crafting Visuals with AI

Image generators are algorithms designed to produce visuals from a blank canvas. The most common type of image generator is a graphics program that can create or modify images. Others include fractal and random number generators.

These tools have broad applications across art, science, and engineering. Artists use them to craft digital art like 3D models or 2D visuals, while scientists use them for simulating real-world phenomena, such as particle behavior. Engineers use image generators for designing products or structures.

In addition to generating new images, these tools can manipulate existing ones, like adding color to monochrome pictures or refining digital photos.

Many image generators cater to both personal and commercial use, with some available for free online or for purchase.

### Diffusers

The Diffusers library from Hugging Face is the image generator we use here. You can find the paper [here](https://arxiv.org/abs/2112.10752). In this tutorial, I will show you how you can use it. Please read about the license [here](https://bigscience.huggingface.co/blog/the-bigscience-rail-license).

In this tutorial, we will use [Google Colab](https://colab.research.google.com). This platform gives you access to a GPU. To turn it on, click Runtime, then change Runtime type, and choose GPU.

### Let's go!

In the beginning we are going to connect our [Google Colab](https://colab.research.google.com) with our Google Drive, to do that use
```python
from google.colab import drive
drive.mount('/content/drive')
```
 When you run this command, you will be able to log in to your drive.

 Now, we have to install all the needed requirements, we will do it with `pip`. If you want to see logs, please remove `> /dev/null 2>&1`

 ```python
!pip install diffusers==0.2.4 > /dev/null 2>&1
!pip install transformers scipy ftfy > /dev/null 2>&1
!pip install "ipywidgets>=7,<8" > /dev/null 2>&1
 ```

If everything is fine we can move to the next step and connect by a token with [Hugging Face](https://huggingface.co/settings/tokens). Just create an account and create a token (Settings -> Access Tokens -> New token). Keep the token private and do not paste it into shared notebooks.

```python
from google.colab import output
from huggingface_hub import notebook_login
output.enable_custom_widget_manager()
notebook_login()
```

The login widget asks for your token. We are almost ready to create an image!

If you want to create more than one photo I recommend creating a new folder.

```python
!mkdir "Saved data" 
```

We should also create a pipe
```python
pipe = pipe.to("cuda")
```

Finally, we can create images. We will create them with a `prompt`, that will be used in the loop to create `N` images.

```python
from torch import autocast

prompt = "cat is fighting with robots, digtal art"  # prompt to describe images to create
no_of_images = 100 # number of images to generate

for i in range(no_of_images):

  with autocast("cuda"):
    image = pipe(prompt, height=512, width=768, num_inference_steps=50)["sample"][0]

  image.save(f"Saved data/sample_{i}.png") # if you not create folder 
  
image
```

There are several arguments such as:

`height`, `width` - size of generated image

`num_inference_steps` - number of generation steps

More information you can find [here](https://huggingface.co/CompVis/stable-diffusion-v1-4)

### Result

The loop saves each generated image into the `Saved data` folder, and the last image is shown in the notebook.

If your purpose is to create images with the shape 300x300px you can generate images with bigger resolution and then resize them.

```python
import cv2
from glob import glob

# glob is reading all names of images in the folder Saved data
for i in glob("/content/Saved data/*.png"):  
    img = cv2.imread(i, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (300, 300))
    cv2.imwrite(i, img)
```

In the end, you can copy your folder to your Google Drive. 
```python
!sudo cp -r '/content/Saved data' /content/drive/MyDrive/
```

## The AI journey doesn't end here

Why stop here? You could build an AI app using image generation and many other models, for example an app that changes audio into an image. With AI the potential is wide open, so keep exploring.

## Use it at an AI hackathon

An image generator is a good building block for an AI hackathon project: it is quick to demo and easy for judges to understand. You can combine it with a text or audio model to turn a short idea into a working prototype within a hackathon weekend. To find an event to try it at, see the [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

**Which platform does this tutorial use, and how do I turn on the GPU?**
It uses Google Colab. Click Runtime, then change Runtime type, and choose GPU.

**What do I need besides Colab?**
A Hugging Face account and an access token (Settings -> Access Tokens -> New token), which you enter when `notebook_login()` runs.

**What if I need smaller images, such as 300x300 pixels?**
Generate images at a bigger resolution first, then resize them with the OpenCV loop shown in the Result section.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, and no step has been confirmed to work as written. To follow it you would need a Google account with Google Colab (a GPU runtime), optionally Google Drive, and a Hugging Face account with an access token. None of these was used here.
