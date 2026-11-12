---
title: "Stable Diffusion tutorial: Text-guided image-to-image generation with Stable Diffusion"
seo_title: "Stable Diffusion Image-to-Image with Diffusers"
meta_description: "AI hackathon tutorial: build a Diffusers pipeline for text-guided image-to-image generation with Stable Diffusion v1-4."
---

This tutorial shows how to create a custom diffusers pipeline for text-guided image-to-image generation with the Stable Diffusion model using the 🤗 Hugging Face Diffusers library.

After reading, you will be able to create beautiful AI generated Artworks from a simple sketch.

## Short introduction to Stable Diffusion 

Stable Diffusion is a text-to-image latent diffusion model created by the researchers and engineers from CompVis, 
Stability AI and LAION. It's trained on 512x512 images from a subset of the LAION-5B database. This model uses a 
frozen CLIP ViT-L/14 text encoder to condition the model on text prompts. With its 860M UNet and 123M text encoder, 
the model is relatively lightweight and runs on most GPUs.

## Lets get started

```bash
!nvidia-smi
```

You need to accept the model license before downloading or using the weights. In this tutorial we'll use model version v1-4, 
so you'll need to visit [its card](https://huggingface.co/CompVis/stable-diffusion-v1-4), read the license and tick the checkbox 
if you agree.

You have to be a registered user in 🤗 Hugging Face Hub, and you'll also need to use an access token for the code to work. For 
more information on access tokens, please refer [to this section of the documentation](https://huggingface.co/docs/hub/security-tokens).

```bash
!pip install diffusers==0.3.0 transformers ftfy
!pip install -qq "ipywidgets>=7,<8"
```

Now we will login into 🤗 Hugging Face. You can use the `notebook_login` function to login.
```python
from huggingface_hub import notebook_login

notebook_login()
```

After this we will get started with the Image2Image pipeline.
```python
import inspect
import warnings
from typing import List, Optional, Union

import torch
from torch import autocast
from tqdm.auto import tqdm

from diffusers import StableDiffusionImg2ImgPipeline
```

Load the pipeline.
```python
device = "cuda"
model_path = "CompVis/stable-diffusion-v1-4"

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_path,
    revision="fp16", 
    torch_dtype=torch.float16,
    use_auth_token=True
)
pipe = pipe.to(device)
```

Download an initial image and preprocess it so we can pass it to the pipeline.

```python
import requests
from io import BytesIO
from PIL import Image

url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

response = requests.get(url)
init_img = Image.open(BytesIO(response.content)).convert("RGB")
init_img = init_img.resize((768, 512))
init_img
```

Define the prompt and run the pipeline.

```python
prompt = "A fantasy landscape, trending on artstation"
```

Here, strength is a value between 0.0 and 1.0, that controls the amount of noise that is added to the input image. Values that approach 1.0 allow for lots of variations but will also produce images that are not semantically consistent with the input.

```python
generator = torch.Generator(device=device).manual_seed(1024)
with autocast("cuda"):
    image = pipe(prompt=prompt, init_image=init_img, strength=0.75, guidance_scale=7.5, generator=generator).images[0]
```

In Colab you can print out the image by just typing:
```python
image
```
And there you have it! A beautiful AI generated artwork from a simple sketch.

Futhermore, you can tune the parameters and test what works for your usecase. When using a lower value for strength, the generated image is closer to the original `init_image`.

## Build it at an AI hackathon

Image-to-image tools are a good fit for an AI hackathon, where you can turn a rough sketch into a working demo quickly. Starfield Labs lists [upcoming AI hackathons](/ai-hackathons/) if you want a deadline and a team to try it with.

## Frequently asked questions

**What do I need before downloading the model?**

You need to accept the model license on the model card for version v1-4, be a registered user of the Hugging Face Hub and use an access token for the code to work.

**What does the `strength` value do?**

Strength is a value between 0.0 and 1.0 that controls the amount of noise added to the input image. Values near 1.0 allow lots of variation but produce images that are not semantically consistent with the input; a lower value keeps the result closer to the original image.

**What does the tutorial use to run the pipeline?**

It checks for a GPU with `nvidia-smi`, sets the device to "cuda", and loads the Stable Diffusion v1-4 weights in half precision (fp16) with the Hugging Face Diffusers library.

## How this tutorial was tested

This tutorial was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, so no step in it has been tested here.

To follow it you would need: a Hugging Face account and access token, acceptance of the Stable Diffusion v1-4 model license, and an Nvidia GPU runtime such as Google Colab. None of these was run, and the model weights were not downloaded.
