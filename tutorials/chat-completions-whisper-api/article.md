---
title: "ChatGPT tutorial: How to integrate ChatGPT and Whisper API into your project"
seo_title: "ChatGPT and Whisper API Integration Tutorial"
meta_description: "AI hackathon tutorial: move from GPT-3 completions to chat completions and send audio to the Whisper endpoint from a React app."
---

# ChatGPT tutorial: How to integrate ChatGPT and Whisper API into your project

## ChatGPT and Whisper API are out!

Drumroll please... OpenAI finally (1.03.2023) released an official ChatGPT/Chat Completion and Whisper API endpoint! If you missed the news you can read it on their blog
page [OpenAI Blog](https://openai.com/blog/introducing-chatgpt-and-whisper-apis). 

But long story short ChatGPT is a large language model trained by OpenAI to generate human-like text in a conversational style. It is a variant of the GPT-3 model, which was specifically designed to be used to generate text in response to user input. Whisper is a general-purpose speech recognition model trained on a large dataset of diverse audio and is also a multi-task model that can perform multilingual speech recognition as well as speech translation and language identification.

## What does it mean for us developers?

Regarding ChatGPT we can finally implement Chat Completion in our projects without some hacks and workarounds. We can use `gpt-3.5-turbo` and `gpt-3.5-turbo-0301` models. We can leverage the cutting edge text to text and audio to text technology into our projects in no time!

Regarding Whisper it means that we don't have to worry anymore about the infrastructure, how to deploy the model and how to scale it, and about the costs of
running a Virtual Machine with GPU all the time. We can just use the endpoint that is provided by OpenAI and we can start building right away.

But straight to the point - let's add OpenAI's technology to our project!

### How to implement ChatGPT/Chat completion endpoint into our project?

ChatGPT is using the gpt-3.5-turbo model. Because in this model the price of the token is 10% of the price of gpt-3 even OpenAI advises to use it instead of GPT-3.
If you already have an implementation of GPT-3 it is pretty easy to migrate to GPT-3.5. Only thing that you need to keep in mind that GPT-3.5 is available in 
chat model. Chat models are taking a series of messages as input instead of a single prompt.  
The chat format is explained more in details [here](https://platform.openai.com/docs/guides/chat/introduction)  

Instead of adding a prompt to your request body you need to add a messages array.
for example in Python with openAI library it will look like this:

```python
import openai

openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a very kind helpdesk agent."},
        {"role": "user", "content": "How can I fix my computer if it is not turning on?"},
        {"role": "assistant", "content": "Did you try to turn it off and on again?"},
        {"role": "user", "content": "Yes, I did. What can be the problem?"}
    ]
)
```

Messages variable must be an array of objects with 2 keys: `role` and `content`. Role can be `user` or `assistant` and `system`

The `system` role message is helping setting the behavior of the assistant.  

### How can we change gpt-3 completion into gpt-3.5 chat completion?

Very easy. For example if before we were doing hashtag creation with gpt-3 the prompt looked like this:

```python
Create hashtags for the following text: "{text}"
```

Now we need to change it to:

```python
[
  {"role": "system", "content": `You are an assistant that creating hashtags for a text`},
  {"role": "user", "content": `Create hashtags for the following text: "{text}"`}
]
```
or  

```python
[
  {"role": "user", "content": `Create hashtags for the following text: "{text}"`}
]
```

Super easy!

### How can you implement Whisper OpenAI endpoint into your project?

If you already had this model deployed on your own infrastructure you can just change the endpoint to the OpenAI endpoint :)  
Jokes aside, if you are just planning to implement this endpoint into your project you can use OpenAI library for [Python](https://github.com/openai/openai-python)
and also for [Javascript](https://www.npmjs.com/package/openai) or you can create the requests by yourself.

### Modifying our React Frontend  boilerplate to use OpenAI Whisper endpoint

This assumes you already have a React frontend that sends an audio file to a Whisper endpoint, with the endpoint set in a `WHISPER_ENDPOINT` variable in `App.js`.

Few things we need to do to make this work.
We need to change the App.js file `WHISPER_ENDPOINT` variable to the OpenAI endpoint https://api.openai.com/v1/audio/transcriptions.

We need to change some variables
```javascript
    const formData = new FormData();
    formData.append("file", file);
    formData.append("model", "whisper-1");
```

We need to add the `Authorization` header with the `Bearer` token. You can get the token from the  
[OpenAI dashboard](https://platform.openai.com/account/api-keys)

```javascript
    const data = await fetch(WHISPER_ENDPOINT, {
      headers:{
        "Authorization": "{PASTE_YOUR_TOKEN_HERE}"
        "Content-Type": "multipart/form-data",
      }
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        return result;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
```

And that's it! You can now use the OpenAI Whisper endpoint in your previously created project to create transcription of audio files.
Keep in mind if you want to create a production ready application you will have to hide your API key.

## Build it at an AI hackathon

Chat completions and speech-to-text are two of the most common pieces in an AI hackathon project, and both are a few lines of code once you have a key. You can add them to a project in the first hours and spend the rest of the time on your idea. To find an event to build in, see the list of [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

### What changes when I move from a GPT-3 completion to a chat completion?

Instead of adding a prompt to the request body you add a `messages` array, where each message is an object with a `role` and a `content` key.

### Which roles can a message have?

The role can be `user`, `assistant` or `system`. The `system` message helps set the behavior of the assistant.

### How do I call the Whisper endpoint from a React frontend?

Set `WHISPER_ENDPOINT` to `https://api.openai.com/v1/audio/transcriptions`, append the file and the model `whisper-1` to the form data, and add an `Authorization` header with your bearer token.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build. None of the steps, code or commands was executed, and no output was checked. Running it needs: an OpenAI API key and billed API usage, plus an existing React frontend that uploads audio. None of these was used here, so versions, prices, model names and links may have changed. Check each one before you start.
