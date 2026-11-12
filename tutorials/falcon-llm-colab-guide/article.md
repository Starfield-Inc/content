---
title: "Falcon LLMs: In-depth Tutorial."
seo_title: "Falcon LLMs Tutorial: Run Falcon 7B, 40B and 180B"
meta_description: "AI hackathon tutorial on Falcon LLMs: use cases, features and running Falcon 7B, 40B and 180B with Hugging Face Transformers."
---

Falcon Large Language Models (LLMs) are versatile and powerful tools in the field of Natural Language Processing (NLP), capable of excelling in a broad spectrum of tasks that helps advance applications and use cases to future-proof our world.

Built on top of the massive English web dataset such as [RefinedWeb](https://huggingface.co/datasets/tiiuae/falcon-refinedweb) by [The Technology Innovation Institute (TII)](https://www.tii.ae/), a global research center. 
See the [paper on arXiv](https://arxiv.org/abs/2306.01116) for more details.

[Falcon 40B](https://huggingface.co/tiiuae/falcon-40b) is **Falcon-7B's** bigger sibling, a multilingual open-source AI model. It was offered royalty-free with weights.

[Falcon 180B](https://huggingface.co/tiiuae/falcon-180B) is a language model with 180 billion parameters, trained on 3.5 trillion tokens and up to 4,096 A100 40GB GPUs, using a 3D parallelism strategy (TP=8, PP=8, DP=64) combined with `ZeRO`. It is available for both research and commercial use.

**Falcon 180B** is described as performing well in tasks like reasoning, coding, proficiency, and knowledge tests.

*Quick Note: You will need at least `400GB of memory` to swiftly run inference with **Falcon 180B**.*

## Falcon LLMs Use Cases

Here is a more detailed breakdown of the various NLP tasks that `Falcon LLMs` can be employed for:

- Text generation
**Falcon LLMs** are proficient at generating coherent and contextually relevant text. This can be applied to tasks such as content generation, creative writing and more.

- Summarization
**Falcon LLMs** can effectively generate concise and coherent summaries of longer texts, making them invaluable for automated document summarization, news article summarization, and content abstraction.

- Translation
**Falcon LLMs** can be utilized for machine translation tasks, enabling the translation of text from one language to another. Fine-tuning the model on specific language pairs can enhance translation accuracy.

- Question-Answering
**Falcon LLMs** are adept at answering questions posed in natural language. By providing context and a question, They can generate relevant answers, making them suitable for chatbots, virtual assistants, FAQ systems and more.

- Sentiment analysis
**Falcon LLMs** can be fine-tuned to classify the sentiment of text, such as determining whether a given piece of text is positive, negative, or neutral. This is widely used in social media monitoring, product reviews analysis, and customer feedback analysis.

- Information Retrieval
**Falcon LLMs** can be used to develop intelligent search engines that understand user queries and retrieve relevant documents or information from large datasets.

**Falcon LLMs** can be adapted and fine-tuned to excel in a wide array of NLP tasks, making them a valuable asset for businesses and researchers seeking to leverage the power of natural language understanding and generation in various applications. 
The adaptability of these models allows for customization to specific tasks and datasets, leading to improved performance and tailored solutions.

## Key Features of Falcon LLMs

**Falcon** offers several key features that make it a prominent and valuable resource in the field of NLP.

- Multiple Model Variants
**Falcon** offers a range of model variants, including Falcon 180B, 40B, 7.5B, and 1.3B, each with different parameter sizes to cater to different use cases and computational resources.

- High-Quality Datasets
Falcon is trained on high-quality datasets, including the RefinedWeb dataset.

- Multilingual Support
**Falcon LLMs** supports multiple languages, including `English`, `German`, `Spanish`, `French`, `Italian`, `Portuguese`, `Polish`, `Dutch`, `Romanian`, `Czech`, and `Swedish`. This multilingual capability broadens its applicability across various language-specific NLP tasks.

- Open-Source and Royalty-Free
**Falcon LLMs** are open-source and offered royalty-free, making it accessible to a wide range of users and contributing to the democratization of AI technology.

- Performance
**Falcon 180B** performs well in reasoning, coding, proficiency, and knowledge tests.

## Getting Started with Falcon LLMs

### Set-up Google Colab

Go to [Google Colab](https://colab.research.google.com/) and create a new notebook.

Rename it to something simple and clear, for ex: `Falcon-LLMs-Tutorial.`.

### Change Runtime Type

Click `Runtime` in the menu bar and select `Change runtime type`. 

From there, select `T4 GPU` and click `Save`.

### Install Hugging Face Transformers and Accelerate

Let's install the `transformers` and `accelerate` library. 

Add new `code cell`. Enter the following code and run it.

```python
!pip install transformers
!pip install accelerate
```

Click `Run` button or `CMD/CTRL + Enter` to run the single `code cell`.

Wait until the installation is complete.

Perfect! Now you're ready to start with Falcon LLMs.

### Let's give Falcon 7B a test!

**Falcon 7B** was trained on 384 A100 40GB GPUs, using a 2D parallelism strategy (PP=2, DP=192) combined with ZeRO.

We will use the transformers pipeline API to load the 7B model like this.

Add new `code cell`. Copy/paste the following code and run it.

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

model = "tiiuae/falcon-7b"  # use "tiiuae/falcon-7b-instruct" for instruction model

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",  # To automatically distribute the model layers across various cards
)
```

And then, you'd run text generation using code like the following:

```python

sequences = pipeline(
   "Girafatron is obsessed with giraffes, the most glorious animal on the face of this Earth. Giraftron believes all other animals are irrelevant when compared to the glorious majesty of the giraffe.\nDaniel: Hello, Girafatron!\nGirafatron:",  # try to be creative here
    max_length=200,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")
```

Click `Run` or `CMD/CTRL + Enter`.

It takes around 3-4 minutes depending on your internet connection. If everything goes well, the generated text is printed below the cell.

### Falcon 40B - Falcon 7B's big brother

**Falcon 40B** was trained on 384 A100 40GB GPUs, using a 3D parallelism strategy (TP=8, PP=4, DP=12) combined with ZeRO.

Running the 40B model is challenging because of its size: it doesn't fit in a single A100 with 80 GB of RAM. Loading in 8-bit mode, it is possible to run in about 45 GB of RAM, which fits in an A6000 (48 GB) but not in the 40 GB version of the A100.
Here is the same process for Falcon 40B, just change the model name to `tiiuae/falcon-40b`.

Add new `code cell`. Copy/paste the following code and run it.

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

model = "tiiuae/falcon-40b"  # use "tiiuae/falcon-40b-instruct" for instruction model

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",  # To automatically distribute the model layers across various cards
)
sequences = pipeline(
   "Girafatron is obsessed with giraffes, the most glorious animal on the face of this Earth. Giraftron believes all other animals are irrelevant when compared to the glorious majesty of the giraffe.\nDaniel: Hello, Girafatron!\nGirafatron:",  # try to be creative here
    max_length=200,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")

```

Click `Run` or `CMD/CTRL + Enter`.

If you face an error like `No space left on device`, you can try to run it on Google Colab Pro or Google Colab Pro+.

Try Falcon 40B [here](https://huggingface.co/spaces/HuggingFaceH4/falcon-chat).

### Falcon 180B - The larger sibling of Falcon 40B

**Falcon 180B** was trained on up to 4,096 A100 40GB GPUs, using a 3D parallelism strategy (TP=8, PP=8, DP=64) combined with ZeRO.

Add new `code cell`. Copy/paste the following code, change the model name to `tiiuae/falcon-180b` and run it again.

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

model = "tiiuae/falcon-180b"  # use "tiiuae/falcon-180b-chat" for chatbot model

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",  # To automatically distribute the model layers across various cards
)
sequences = pipeline(
   "Girafatron is obsessed with giraffes, the most glorious animal on the face of this Earth. Giraftron believes all other animals are irrelevant when compared to the glorious majesty of the giraffe.\nDaniel: Hello, Girafatron!\nGirafatron:",  # try to be creative here
    max_length=200,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")
```

Click `Run` or `CMD/CTRL + Enter`.

If you face an error like `No space left on device`, you can try to run it on Google Colab Pro or Google Colab Pro+.

## Falcon 180B Demo showcases

You may also try Falcon 180B demo [here](https://huggingface.co/spaces/tiiuae/falcon-180b-demo). It opens experimental preview of the model in Hugging Face Spaces to showcase an early finetuning of Falcon 180B, to illustrate the impact (and limitations) of finetuning on a dataset of conversations and instructions.

Falcon LLMs are available on Hugging Face Spaces:
- [Falcon 7B](https://huggingface.co/tiiuae/falcon-7b).
- [Falcon 7B instruct](https://huggingface.co/tiiuae/falcon-7b-instruct).
- [Falcon 40B](https://huggingface.co/tiiuae/falcon-40b).
- [Falcon 40B instruct](https://huggingface.co/tiiuae/falcon-40b-instruct).
- [Falcon 40B Demo](https://huggingface.co/spaces/HuggingFaceH4/falcon-chat) experimental preview.
- [Falcon 180B](https://huggingface.co/spaces/tiiuae/falcon-180b).
- [Falcon 180B Chat](https://huggingface.co/spaces/tiiuae/falcon-180b-demo).
- [Falcon 180B Demo](https://huggingface.co/spaces/tiiuae/falcon-180b-demo) experimental preview.

## Conclusion

In this tutorial, we have covered the basics of Falcon LLMs, including their use cases, key features, and how to get started with them. We have also demonstrated how to run inference with Falcon LLMs using the Hugging Face Transformers library.

Thank you for following along with this tutorial.

## Build it at an AI hackathon

An open model you can run yourself is a useful option in an AI hackathon when you cannot or do not want to call a hosted API. The Falcon models here are loaded through the Hugging Face Transformers pipeline in a notebook. To find an event to try it in, see the list of [upcoming AI hackathons](/ai-hackathons/).

## Frequently asked questions

### How much memory does Falcon 180B need?

At least 400GB of memory to run inference quickly, according to the quick note in the tutorial.

### Which Colab runtime does the tutorial select?

Open `Runtime`, then `Change runtime type`, select `T4 GPU` and click `Save`.

### What if I get a "No space left on device" error?

The tutorial suggests trying Google Colab Pro or Google Colab Pro+.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build. None of the steps, code or commands was executed, and no output was checked. Running it needs: a Google Colab account (Colab Pro or Pro+ is mentioned), a T4 GPU runtime for the 7B model, and very large GPU memory for the 40B and 180B models. The models download from Hugging Face. None of these was used here, so versions, prices, model names and links may have changed. Check each one before you start.
