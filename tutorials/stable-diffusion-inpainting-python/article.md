---
title: "Stable Diffusion tutorial: Prompt Inpainting with Stable Diffusion"
seo_title: "Prompt inpainting with Stable Diffusion and Clipseg"
meta_description: "AI hackathon tutorial: inpaint images with Stable Diffusion and Clipseg using text prompts instead of a hand-painted mask, in Google Colab."
---

## What is InPainting?

Image inpainting is an active area of AI research where AI has been able to come up with better inpainting results than most artists. 

It's a way of producing images where the missing parts have been filled with both visually and semantically plausible content. It can be quite 
useful for many applications like advertisements, improving your future Instagram post, edit & fix your AI generated images and it can even be used to repair old photos. 
There are many ways to perform inpainting, but the most common method is to use a convolutional neural network (CNN).

A CNN is well suited for inpainting because it can learn the features of the image and can fill in the missing content using these features and
there are many different CNN architectures that can be used for this.

## Short introduction to Stable Diffusion

Stable Diffusion is a latent text-to-image diffusion model capable of generating stylized and photo-realistic images. It is pre-trained on a subset of the LAION-5B dataset and the model can be run at home on a consumer grade graphics card, so everyone can create stunning art within seconds.

## How to do Inpainting with Stable Diffusion

This tutorial helps you to do prompt-based inpainting without having to paint the mask - using Stable Diffusion and Clipseg. A mask in this case is a
binary image that tells the model which part of the image to inpaint and which part to keep. A further requirement is that you need a good GPU, but 
it also runs fine on Google Colab Tesla T4.

It takes 3 mandatory inputs to perform InPainting.

1. Input Image URL
2. Prompt of the part in the input image that you want to replace
3. Output Prompt 

There are certain parameters that you can tune
1. Mask Precision
2. Stable Diffusion Generation Strength 

If you are using Stable Diffusion from Hugging Face 🤗 for the first time, You need to [accept ToS on the Model Page](https://huggingface.co/CompVis/stable-diffusion-v-1-4-original) and get your [Token from your user profile](https://huggingface.co/settings/tokens)

### So let's get started!

Install open source Git extension for versioning large files
```bash
! git lfs install
```

Clone the clipseg repository
```bash
! git clone https://github.com/timojl/clipseg 
```

Install diffusers package from PyPi
```bash
! pip install diffusers -q
```

Install some more helpers
```bash
! pip install transformers -q -UU ftfy gradio  
```

Install CLIP with pip
```bash
! pip install git+https://github.com/openai/CLIP.git -q
```

Now we move on to logging in with Hugging Face. For this simply run the following command:
```python
from huggingface_hub import notebook_login

notebook_login()
```

After the login process is complete, you will see the following output:
```bash	
Login successful
Your token has been saved to /root/.huggingface/token
```

```bash	
%cd clipseg
```
```bash	
! ls
```
```bash	
datasets	     metrics.py        supplementary.pdf
environment.yml      models	       Tables.ipynb
evaluation_utils.py  overview.png      training.py
example_image.jpg    Quickstart.ipynb  Visual_Feature_Engineering.ipynb
experiments	     Readme.md	       weights
general_utils.py     score.py
LICENSE		     setup.py
```

```python
import torch
import requests
import cv2 
from models.clipseg import CLIPDensePredT
from PIL import Image
from torchvision import transforms
from matplotlib import pyplot as plt

from io import BytesIO

from torch import autocast
import requests
import PIL
import torch
from diffusers import StableDiffusionInpaintPipeline as StableDiffusionInpaintPipeline
```

Load the model
```python
model = CLIPDensePredT(version='ViT-B/16', reduce_dim=64)
model.eval();
```

```python
model.load_state_dict(torch.load('/content/clipseg/weights/rd64-uni.pth', map_location=torch.device('cuda')), strict=False);
```
Non-strict, because we only stored decoder weights (not CLIP weights)


```python
device = "cuda"
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    revision="fp16", 
    torch_dtype=torch.float16,
    use_auth_token=True
).to(device)
```

Alternatively you can load an Image from an external URL like this:
```python
image_url = 'https://example.com/your-image.jpg'  # replace with a URL of an image you have rights to use

input_image = Image.open(requests.get(image_url, stream=True).raw)

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    transforms.Resize((512, 512)),
])
img = transform(input_image).unsqueeze(0)
```

Move back in directories
```bash
%cd ..
```

Convert the input image
```python
input_image.convert("RGB").resize((512, 512)).save("init_image.png", "PNG")
```

Display the image with the help of plt
```python
from matplotlib import pyplot as plt
plt.imshow(input_image, interpolation='nearest')
plt.show()
```

This will show your input image.
Now we will define a prompt for our mask, then predict and then visualize the prediction:
```python
prompts = ['shirt']
```
```python
with torch.no_grad():
    preds = model(img.repeat(len(prompts),1,1,1), prompts)[0]
```
```python
_, ax = plt.subplots(1, 5, figsize=(15, 4))
[a.axis('off') for a in ax.flatten()]
ax[0].imshow(input_image)
[ax[i+1].imshow(torch.sigmoid(preds[i][0])) for i in range(len(prompts))];
[ax[i+1].text(0, -15, prompts[i]) for i in range(len(prompts))];
```
Now we have to convert this mask into a binary image and save it as PNG file:
```python
filename = f"mask.png"
plt.imsave(filename,torch.sigmoid(preds[0][0]))

img2 = cv2.imread(filename)

gray_image = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

(thresh, bw_image) = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)

# For debugging only:
cv2.imwrite(filename,bw_image)

# fix color format
cv2.cvtColor(bw_image, cv2.COLOR_BGR2RGB)

Image.fromarray(bw_image)
```
Now we have a black-and-white mask of the shirt.

Now load the input image and the created mask
```python
init_image = Image.open('init_image.png')
mask = Image.open('mask.png')
```

And finally the last step: Inpainting with a prompt of your choice. Depending on your hardware, this will take a few seconds.
```python
with autocast("cuda"):
    images = pipe(prompt="a yellow flowered holiday shirt", init_image=init_image, mask_image=mask, strength=0.8)["sample"]
```

On Google Colab you can print out the image by just typing its name:
```python
images[0]
```

Now you will see that the shirt we created a mask for got replaced with our new prompt! 🎉

## AI hackathon ideas

Prompt-based image editing is a good fit for an AI hackathon: think product photo tools, photo repair or social media editors. Starfield Labs runs AI hackathons where you can build a prototype like this with a team. Browse the [upcoming AI hackathons](/ai-hackathons/) to join one.

### More resources
[InPainting Stable Diffusion (CPU) Demo](https://huggingface.co/spaces/fffiloni/stable-diffusion-inpainting)

[Full Code in Colab Notebook](https://colab.research.google.com/github/amrrs/stable-diffusion-prompt-inpainting/blob/main/Prompt_based_Image_In_Painting_powered_by_ClipSeg.ipynb)

## Frequently asked questions

**What inputs does prompt inpainting need?**
Three mandatory inputs: an input image URL, a prompt describing the part of the image to replace, and an output prompt. Mask precision and Stable Diffusion generation strength can be tuned.

**What hardware do I need?**
The tutorial says you need a good GPU, and that it also runs fine on a Google Colab Tesla T4.

**What do I need for Stable Diffusion from Hugging Face?**
For first-time use you need to accept the terms on the model page and get a token from your Hugging Face user profile.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, so no step has been tested here. Running it needs a GPU (for example a Google Colab T4 runtime), a Hugging Face account with an access token and accepted model terms, and downloads of the clipseg repository and model weights. None of these was used.
