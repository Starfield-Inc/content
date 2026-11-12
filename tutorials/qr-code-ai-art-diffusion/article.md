---
title: "Stable Diffusion tutorial: How to make an AI art with QR code"
seo_title: "Stable Diffusion QR code art tutorial with ControlNet"
meta_description: "AI hackathon tutorial: make AI art that still scans as a QR code, using Stable Diffusion WebUI and two ControlNet models in five steps."
---


## AI art is improving!

AI art is getting increasingly popular, but despite its visual aspect, there are not many options for how you can utilize it. Of course, you can adopt it into your business Social Medias or blogposts to improve the user experience of interacting with your content or to make it more eye-catching, but… what else you can do with it? Of course, we saw trending videos of [Balenciaga](https://www.youtube.com/watch?v=iE39q-IKOzA), a great example of viral marketing, but what else?

Sure, there are Tik-Tok trends with video transforming into AI-generated ones, but I want to focus more on text-to-image and image-to-image generation. Of course, examples I know for using text-to-image generation are for interior design or any other used for health-related fields. 

But what about other industries? Well, last week I saw on [reddit](https://www.reddit.com/r/StableDiffusion/comments/141hg9x/controlnet_for_qr_code/) an excellent new technique of generating AI art which might be really useful for brand communication or even merch production - a new way to utilize QR codes, which are… not that popular.

So without any further ado, let’s learn how to generate AI art with a readable QR code!

## Let’s do it!

Okay, for this tutorial you will learn how to make AI art with a readable QR code with Stable Diffusion WebUI. In the future, I will write a tutorial on how to make one with Google Colab, but not today!

### 1. Download and install Stable Diffusion WebUI

So, first, download the Stable Diffusion WebUI repo from [Automatic1111 github](https://github.com/AUTOMATIC1111/stable-diffusion-webui) and install it following the instruction in the link. 

### 2. We need also ControlNet extension

As you you have installed the WebUI, go to the “extensions tabs” and then to the “available” tab. Find “ControlNet”, click “install” and then restart your WebUI.

Now, as you go to the bottom of the page you should see “controlnet” section.

If you can't see them go to the “settings” tab on the top of the page, then find “ControlNet” on the left and click on it.  

You will see “Multi ControlNet: Max models amount”, drag it into position “2” and restart.

### 3. Let’s generate a QR code

We won't use AI to generate a QR code, but we will use an existing one as an input image. There are many free websites, I am using [this one](https://dnschecker.org/qr-code-generator.php) and you can use which one you prefer. Choose “error correction level:L” and image size 250x250 and download the generated image.

### 4. Download 2 models

Download those 2 models: \
From [this link](https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main) download “control_v11p_sd15_lineart.pth”

And from [this one](https://huggingface.co/ioclab/ioc-controlnet/tree/main/models) “control_v1p_sd15_brightness.safetensors”

And install them.

### 5. Everything’s set up, let's generate!

You remember, that we needed to have 2 control net windows. So we will need to upload our QR codes into both “controlNet Unit 0” and “controlNet Unit 1” tabs, and in each of them tag the field “enable”.

Now for both of them choose preprocessor “inpaint_global_harmonious” and for the first one choose Model “control_v11p_sd15_lineart.pth” and for the second one “control_v1p_sd15_brightness.safetensors”

For the first one (the one with control_v1p_sd15_brightness.safetensors model), choose Control weight 0.35, Starting Control Step 0 and Ending control Step 1.

For the second one (the one with control_v11p_sd15_lineart.pth model), choose Control weight 0.65, Starting Control Step 0.35 and Ending control Step 0.75..

Change the sampling method to “DPM++2M Karras” or “Euler A”.

Choose the “text2img” tab, insert your prompt (and negative one), press generate and… here you are :)

## Summary!

So as you saw it's not that hard and you can play a lot with it! QR codes can have a second life, so why not come up with a new solution using Stable Diffusion or any other AI API?

## AI hackathon ideas

Branded QR art, merch and event materials are all ideas you could take further at an AI hackathon: identify a problem and build a solution to it using AI. Starfield Labs runs AI hackathons you can join. Browse the [upcoming AI hackathons](/ai-hackathons/) to find one.

I hope you liked the tutorial.

## Frequently asked questions

**What do I need to install?**
The Stable Diffusion WebUI from the Automatic1111 GitHub repository and the ControlNet extension, plus two ControlNet models downloaded from Hugging Face.

**How is the QR code created?**
The tutorial does not use AI for it. You generate a QR code with any free online generator (error correction level L, image size 250x250) and use the image as input to both ControlNet units.

**Which sampling methods does it suggest?**
"DPM++2M Karras" or "Euler A".

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, so no step has been tested here. Following it needs a local Stable Diffusion WebUI install (a GPU is likely needed), large model downloads from Hugging Face, and a QR code generator website. No paid service, wallet or API key is required by the text, and none was used. None of these was used.
