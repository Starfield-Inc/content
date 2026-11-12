---
title: "Stable Diffusion tutorial: how to create video with text prompts"
seo_title: "Stable Diffusion Deforum: Video from Text Prompts"
meta_description: "AI hackathon guide to Stable Diffusion Deforum: turn text prompts into a video with the Google Colab notebook, from setup to rendering."
---

## What is Stable Diffusion Deforum?

Deforum Stable Diffusion is a version of Stable Diffusion focussing on creating videos and transitions of images created with Stable Diffusion. It is an open source and community driven tool. If you want to contribute and support the project, regardless of level of experience or field of expertise, you can reach out to the [developers](https://github.com/deforum-art/deforum-stable-diffusion).

In this tutorial I will show you how to create a video from text prompts to complement a music and create a music video, using the Stable Diffusion Deforum Google Colab notebook.

## Why this matters for an AI hackathon

Generating video from text is a good fit for an AI hackathon project that needs a striking visual demo. Running everything in a hosted notebook means you do not need your own GPU. When you are ready to build, see the [upcoming AI hackathons](/ai-hackathons/).

## Setting up the account for the first time

In this tutorial I will show you how to create a whole pipeline for Stable Diffusion Deforum video creation. We will run everything online, without needing to involve your GPU. In the future there are going to be tutorials on how to run Stable Diffusion locally, but that's not for now. Today, learn how to do it online, for free, without any advanced equipment, where passion for art and AI and imagination is all you have.

But, in the end, what else do you need?

For this tutorial you need to have:

* Google account and at least 6 GB space on your google drive
* Huggingface account
* A computer. Not anything fancy required
* Internet access

Let's go!

### Copy Deforum on your Google Drive

Go to [Deforum Stable Diffusion v0,5](https://colab.research.google.com/github/deforum/stable-diffusion/blob/main/Deforum_Stable_Diffusion.ipynb) and copy it on your google drive with the "Copy to Drive" button at the top of the notebook.

After pushing the button we will be redirected to the copied Google Colab notebook on our Google drive. Close the original one, you will not use it again.

### Running for the first time

Right now, you have full access to Google Colab and we need to connect it to an external GPU, using the Connect button at the top right of the notebook.

Note, that you have some free credits for Google Colab and if you run out of them you can either buy more of them or wait a day or two to get them refreshed.

### Google drive wants to access your google account

When you're successfully connected to the NVIDIA GPU (usually it is Tesla T4, 15360 MiB, 15101 MiB), you have to run the rest of the cells, but to do so, you need to give access to your Google Drive. If you want to use it, you have to grant access, but I encourage you to first read all of the terms and conditions and press the "allow" button only if you truly agree with them.

After you accepted the access, two folders will be created on your google drive:

ai/models and ai/stablediffusion.

In the ai/models folder all of your Stable Diffusion models, which you can use to generate videos, will be stored and in the ai/stablediffusion folder all of the output images will be stored.

### Setting up environment and python definitions

Run the next two cells. They are pretty straightforward. It takes a couple of minutes to connect, but that's all it takes.

### Select and Load Model

This one requires some action from us. As we run the cell, it will ask for our Hugging Face username and Hugging Face token. Enter them, then wait a couple of minutes while models, configs and more are downloaded. Treat the token like a password and do not share it.

## We're all set up

All of the previous steps we will have to repeat every time we start our Google Colab (except providing the Hugging Face username and token).

But right now we can just go and play around with the settings to have our AI generated video come to life.

We will take a closer look at the **animation setting**, where we set up all of the motion of the video / camera movement and other important factors.

We also need to provide **prompts**, so we can generate our videos from text.

Last part here will be running everything with the "**run**" section.

### Animation settings

They might look really overwhelming at first glance, but they are not. We will go through all of the important ones and explain them, so you will have a place to start and then play with it as much as you want.

If you choose the **2D** animation, you will use only angle and zoom from "motion parameters settings"

If you choose **3D** animation, you will also use the translation and rotation section.

**Video input** is for options where you want to alter your video with a Stable Diffusion model.

**None** option will create a single image. It's good to use to see if the initial image fits your vision.

In this tutorial we will make it simple with 2D generation.

Max frames settings means how many frames will be generated. I am always generating 24 frames per second, some people are generating 12 frames per second.

So for 10 seconds of video I would generate 240 frames.

And border sections has 2 options:

**Wrap**, which pulls pixels to the next image from the opposite side of the previous frame.

**Replicate**, which repeats the edge of the previous image and applies it to the next one.

I always use the wrap option.

### Motion parameters

As I previously mentioned angle and zoom are settings for 2D animations and translation, rotation and perspective flip is for 3D generation.

Example values from previous generations look like this.

Settings for angle with value: 0:(0), 95:(0), 96:(0.2) means that starting with frame 0 the video will not rotate. It will not rotate until frame 95, but with frame 96 it will rotate with every frame for 0.2 degrees with every picture.

Setting for zoom value 0:(1.00), 95:(1.00), 96:(1.02) means that starting with frame 0 there will be no zoom in the video, until frame 95, but with frame 96 it will zoom with every frame by 0.02.

Default value for angle is 0, which means that if you put 0.1 or -0.1 it will rotate clockwise or counterclockwise. For Zoom default value is 1, so when you set value at 0.99 it will zoom out slowly with every frame and with 1.01 it will zoom in slowly.

**Important note** - first start with smaller values and see how the video changes with them and then you can go wild as you get more confident.

Also use a comma to separate every frame setting and as you set up a value to a frame use full stop. Kind of confusing, but you will get used to it.

Last two parameters in this section that are very important are noise_schedule and strength_schedule.

As with angle or zoom you can set up a different value for different frames, you can do so with noise and strength.

Noise means how much grain you want to be added to every frame. It leads to more diffusion diversity. I usually go with 0.02 or 0.03.

Strength means how you want the next frame to be different from the previous one. If you set the value to 1 it means it will be absolutely different from the previous one. 0 means it will be the same as the previous one. I usually go with 0.62.

Contrast I always keep at 1.

### Rest of the animation settings

We can skip the 3D depth warping, as we're doing 2D animation right now.

Also Videoinput is for video to video settings, so we don't get into those details.

Interpolation is an interesting option - if you tag this option and give value 4 it means it will create every fourth image and melt all frames between them. It speeds up the animation process and might give a little bit of control over the video, but in the end it makes it more blurry. If you want to use this option, I would recommend value 2.

And the most important option in this section is Resume Animation. If for example your animation stopped in the middle because of a system crash, lack of internet or you simply run out of credits, you can continue from the place it stopped. Just tag this option and as value put the first 12 numbers of the name of any image file created.

### Prompts

These are the things we want to see in our animation. Prompt engineering, or the way we communicate with [Stable Diffusion models](https://stability.ai/) (or any other LLM), is a really important part of today's life. And I invite you to try other ways / commands / styles of communication. I prefer always to give a detailed description of what I want to see, some details about lighting or time of a day and an art style or cultural referral. I don't like using titles of works and names of certain artists, but I saw many great generations done with name dropping.

First option is if you generate just a single image, not a whole animation (so in animation settings you have chosen the "none" option).

Second option is the one we are interested in. You always need to give the first prompt. And if you want to have a different prompt on frame 131 just type

131:"and the prompt",

And that's it.

However I would recommend that you test the prompts out first, and use the ones you like in the final animation. Sometimes the surprises or artifacts are really interesting, but I would recommend you to go with the effects you accepted beforehand.

## Let's create the animation already

We're almost there, just the last setting and you're ready to start your adventure with Stable Diffusion models.

### Last settings

I would recommend always to have the override_with_file option tagged in. That way you will always have your settings saved and you can go back to them / reuse them or share them.

Image settings - if you're going for 9:16, I would recommend 448 x 706. For vertical 706 x 448 and for square 512 x 512.

For the sampling settings - if you already chose a seed you like, put it in the seed line. If you want to have it random, go for -1.

I would recommend you to have a value of 50 / 60 steps. It is an option how many generations Deforum will make of the image before it will choose the one to show you.

Scale value I would recommend between 7 and 12.

### One last touch before hitting "generate"

I didn't lie - in batch_name you just need to name the folder where you want all of your images to be saved and you can hit generate.

Enjoy your videos!

### But it generated only images

Sequences of images are called videos. So the last step you do after generating images is downloading them and putting them in a video editing tool and rendering out the video. That's simple.

I always use a free tool, which gives you a lot of possibilities, which is [DaVinci Resolve 18](https://www.blackmagicdesign.com/products/davinciresolve).

And that's it. Of course you can use the code from the "create video from frames" section, but it doesn't always work and you don't always have full control over the video. So I skipped this step.

## Last tips

### Okay, but how do I know when I want to change animation for the music

It's the human factor in the generation. For example you feel that you want to have a video moving for 10 seconds to the left, then 10 seconds to the right and after that moment you want it to stop turning and zoom in dynamically, because it would fit the music well. No problem. Just remember, that 1 second is 24 frames.

In angle just type 0:(1), 239:(1), 240(-1), 479:(-1), 480:(0)

And in zoom 0:(1), 479:(1), 480(1.03)

Easy.

If you want to have first prompt run for 10 seconds and then another one take over, you have to:

In strength_schedule type 0:(0.62), 239:(0.62), 240:(1), 241:(0.62)

And in animation prompt you just put

0:"prompt 1",

240:"prompt 2"

Easy, right?

### But images are too small and low quality

That's one of the reasons you should download them first and render them in an external tool. But this won't fix the problem, because they are just too small and they need to be upscaled. The tool I am using for upscaling is [chaiNNer](https://github.com/chaiNNer-org/chaiNNer), and it's also Open Source. Just download it, download a correct model to fit your needs and then put the upscaled images in a sequence into DaVinci Resolve.

Note: upscaling requires some GPU, so for that one you need a stronger PC, or make it run through the night or a few nights if video is bigger.

## Now it's just you, AI and imagination

I hope this tutorial will help you unleash your creative potential. I learned everything about creating with Stable Diffusion models and Deforum from YouTube videos, reddit posts and discord. Here, you have everything in one place and with some tips and tricks how to navigate through it.

And if you can't find a tool to create a certain thing, why not create it? Maybe during an upcoming AI hackathon.

## Frequently asked questions

**What is Stable Diffusion Deforum?**

Deforum Stable Diffusion is a version of Stable Diffusion focussing on creating videos and transitions of images created with Stable Diffusion. It is an open source and community driven tool.

**Do I need my own GPU to create a video with Deforum?**

No. The tutorial runs everything online in a Google Colab notebook connected to an external GPU. You need a Google account with at least 6 GB free on Google Drive, a Hugging Face account, an ordinary computer and internet access. Upscaling the images afterwards with chaiNNer does need a GPU.

**Why did the notebook generate only images and not a video?**

Deforum produces a sequence of images. After generating them you download the images, put them in a video editing tool such as DaVinci Resolve and render the video. The "create video from frames" cell in the notebook can also be used, but the author notes it does not always work.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, and no step in it has been tested here. To follow it you need a Google account with Colab (free credits run out, and extra use may be paid), Google Drive space, a Hugging Face account and token, and a Colab GPU. None of these accounts, GPUs or tokens was used for this write-up.
