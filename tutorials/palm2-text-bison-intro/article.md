---
title: "PaLM2 Tutorial: Create your own AI-powered Virtual Assistant"
seo_title: "PaLM2 tutorial: build an AI virtual assistant"
meta_description: "AI hackathon tutorial: build a chat-style virtual assistant with Google's PaLM2 API and a Streamlit app in Python, step by step."
---


## Introduction

PaLM2 is a large language model from Google. The original tutorial describes it as outperforming previous models, including PaLM, in various reasoning tasks such as code and math, classification, question answering, translation, and natural language generation.


## Prerequisites
To use Google’s PaLM2 API you should [join the waitlist](https://developers.generativeai.google/products/palm)
To deploy our app on Streamlit, we need create an account. Go to [Streamlit](https://streamlit.io/) and create an account. It's also free! 🎉. I recommend, to use your GitHub account to create an account on Streamlit, so later you can deploy your app on Streamlit Sharing Cloud.


## Getting Started

### 0. Create a new project directory

Create a new project directory and navigate to it in your terminal:

```bash
mkdir palm2-tutorial
cd palm2-tutorial
```

Create and activate virtual environment:

```bash
MacOS/Linux:
python3 -m venv .venv
source venv/bin/activate

Windows:
py -3 -m venv .venv
.venv\Scripts\activate
```

Install Streamlit and Google's PaLM API dependencies:

```python
pip install streamlit
pip install streamlit_chat
pip install google-generativeai
```

### 1. Create a new Streamlit app

Create a new file called `app.py`. Import Streamlit and Google's PaLM API packages:


```python
import streamlit as st
from streamlit_chat import message
import google.generativeai as palm
```

Add a title to the app:

```python
st.title("PaLM Tutorial")
```

Initialize the messages state:

```python
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Say something to get started!"}]
```

Now, let's create a form to get user input and sent it to the Google’s PaLM API. We will use Streamlit's `st.form()` to create a form and `st.columns()` to create two columns. The first column will be used for user input, and the second column `Send` button.

```python
with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])

    user_prompt = a.text_input(
        label="Your message:",
        placeholder="Type something...",
        label_visibility="collapsed",
    )

    b.form_submit_button("Send", use_container_width=True)
```

Make user input at the left side of the screen, so it looks like a chat app:

```python
for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")  # display message on the screen
```

Configure Google's PaLM API with your API key and get response from the API:


```python
if user_prompt and palm_api_key:

    palm.configure(api_key=palm_api_key)  # set API key

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    message(user_prompt, is_user=True)

    response = palm.chat(messages=[user_prompt])  # get response from Google's PaLM API

    msg = {"role": "assistant", "content": response.last}  # we are using dictionary to store message and its role. It will be useful later when we want to display chat history on the screen, to show user input at the left and AI's right side of the screen.

    st.session_state.messages.append(msg)  # add message to the chat history

    message(msg["content"])  # display message on the screen
```


Optionally, implement function to clear the chat history:

```python
def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]

if len(st.session_state.messages) > 1:
    st.button('Clear Chat', on_click=clear_chat)
```

### 2. Run the app

Run the app:

```bash
streamlit run app.py
```

You should see a simple chat interface in your browser.

Perfect! Now, let's deploy our app on Streamlit Sharing Cloud. See the Streamlit documentation for a detailed guide to deploying your app on Streamlit Community Cloud.


## Conclusion

In this tutorial, we learned how to build AI-powered Virtual Assistant using Google's PaLM2 model. We used Streamlit to build the app, it lets you build apps using pure Python.

Thank you for following along with this tutorial.

## AI hackathon ideas

A chat assistant like this is a common starting point for AI hackathon projects. Starfield Labs runs AI hackathons where you can turn a prototype into a working app with a team. Browse the [upcoming AI hackathons](/ai-hackathons/) to find one.

## Frequently asked questions

**What does the app do?**
It is a Streamlit chat app that sends your message to Google's PaLM API and shows the reply, with an optional button to clear the chat history.

**What do I need before starting?**
Access to the Google PaLM2 API (the text says to join the waitlist) and a free Streamlit account for deployment, ideally created with your GitHub account.

**Which packages does it install?**
`streamlit`, `streamlit_chat` and `google-generativeai`.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, so no step has been tested here. Following it needs Google PaLM API access and an API key, and a Streamlit account for deployment. None of these was used. None of these was used.
