---
title: "Classify Text with an LLM: AI Hackathon Tutorial"
description: "An AI hackathon tutorial on text classification with an LLM: label 50 reviews, count right and wrong, change the prompt once and measure again."
---

# Classify customer reviews with an LLM and check it on 50 examples

You will build a small Python tool that labels reviews as positive, negative or mixed with the Claude API, then counts how many labels match ones you wrote yourself. It takes about 45 minutes.

**Level:** Intermediate. **You need:** Python 3.10 or newer, a terminal, and an Anthropic API key. **Tested:** 10 November 2026 on macOS with Python 3.14.6 and `anthropic` 2.7.0, using the model `claude-haiku-5-5`. The Windows commands were not run.

Classification is a small project you can finish in an AI hackathon, and counting right and wrong labels shows whether a prompt change helped. See the [upcoming AI hackathons](/ai-hackathons/) if you want to try it with a team.

## Why check a prompt on labelled data

A prompt that looks right on three examples can fail on the fourth. If you write down the answers you expect for a set of examples, you can count the misses and see which kind of review causes them. You can then change the prompt and measure again, instead of guessing whether the change helped.

## See it running first

By the end you will compare two prompts on the same 50 reviews and get a summary like this:

{{shot:08-score-v2|Right and wrong counts for two prompts on 50 reviews, with the reviews whose label changed}}

Model output varies from run to run. Your counts may differ from the ones in this article. The rest of the tutorial builds the tool from scratch.

## Step 1. Create a virtual environment

A virtual environment keeps this project's packages apart from the rest of your machine. Make a folder, open a terminal in it, and run:

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Activate it. On macOS and Linux use `source .venv/bin/activate`. On Windows use `.venv\Scripts\activate`. Every command below assumes the environment is active.

## Step 2. Install the SDK and set your key

The only package is the official Anthropic Python SDK. List it in `requirements.txt`:

{{file:requirements.txt}}

Install it:

{{cmd:02-install}}

{{shot:02-install|Terminal after installing the anthropic package, showing the name and version}}

Create a file named `.env` in the project folder with your own key, or export the variable in your terminal. Never paste a key into code or share the file. The project ships a `.env.example` that shows the format:

{{file:.env.example}}

## Step 3. Write the labelled reviews

The check is only as good as the labels, so write them yourself. This tutorial uses 50 short reviews written for it: 17 positive, 18 negative and 15 mixed. Some are plain. Others are meant to be hard: sarcasm that sounds like praise, praise with a catch, and reviews with no opinion at all. The label column is the answer you expect, and `reviews.csv` is the file the rest of the code reads.

The script below counts the rows and the labels so you can catch a typo before you spend any API calls:

{{file:check_data.py}}

{{cmd:03-data}}

{{shot:03-data|Terminal showing 50 reviews and the count for each label}}

The file has 50 rows and 17, 18 and 15 reviews in the three labels. No row has an unknown label.

## Step 4. Write the prompt and classify one review

The prompt is a short instruction plus the review. It names the three labels and asks for one word, so the answer is easy to compare with your label. Both prompts used in this tutorial live in one file:

{{file:prompts.py}}

`classify.py` sends one review per call. It sets `max_tokens` to 10 because a label is one word, and it turns thinking off with `thinking={"type": "disabled"}`. Anthropic's model notes say this model thinks by default, and thinking tokens would count against the 10-token limit. Each call writes one line to `spend.log` with the input and output tokens from the response's `usage` field. Anything the model says that is not one of the three labels is stored as `invalid`.

{{file:classify.py}}

Try one review:

{{cmd:04-one}}

{{shot:04-one|Terminal showing one review and the predicted label mixed}}

The review praises the speed and complains about the lid, and the model said mixed.

## Step 5. Run the prompt on all 50 reviews

Now run prompt v1 over the whole file. This makes 50 calls, one per review, and saves every answer to `results_v1.csv`.

{{cmd:05-run-v1}}

{{shot:05-run-v1|Terminal showing that 50 reviews were classified with prompt v1}}

## Step 6. Count right and wrong

`score.py` compares the `predicted` column with your `label` column. It prints the totals, a count per label, and every wrong row with the model's raw answer. Looking at the wrong rows matters more than the total, because they tell you what to change.

{{file:score.py}}

{{cmd:06-score-v1}}

{{shot:06-score-v1|Terminal showing 47 right and 3 wrong for prompt v1, with the three wrong reviews}}

With prompt v1 the model matched 47 of 50 labels. The three misses are in the output above. Two reviews I labelled mixed got the answer "Neutral", which is not one of the three labels, so the script counted them as `invalid`. The third was review 32, where I wrote negative and the model said "Mixed". That one is a judgement call: the reviewer says the sound is fine "if you do not mind it cutting out", and a reader could argue for either label. Labels you write are opinions too, so keep that in mind when you read a score.

## Step 7. Change the prompt once and rerun

I wrote prompt v2 before I saw the v1 results. It does two things: it defines each label in a sentence, and it says that praise used as a joke still counts as negative. It still asks for one word. Run it:

{{cmd:07-run-v2}}

{{shot:07-run-v2|Terminal showing that 50 reviews were classified with prompt v2}}

Then score both runs together. With two files, `score.py` also lists the reviews whose prediction changed:

{{cmd:08-score-v2}}

{{out:08-score-v2}}

In this run v2 matched 50 of 50 labels, and the three reviews that changed are the three v1 misses. Be careful with that result. The 50 reviews are the same ones used to compare the prompts, so a perfect score here does not show the prompt will do as well on reviews it has not seen. A fair test of v2 needs new reviews that you did not look at while writing the prompt. Rerunning also gives a different answer sometimes, so one run is a sample, not a fixed number.

## Step 8. What a missing key looks like

If the key is not set, the script stops before it makes any call and says why. Here the step runs without a key on purpose:

{{cmd:09-no-key}}

{{shot:09-no-key|Terminal showing the message that ANTHROPIC_API_KEY is not set}}

The exit code is 2. If you see this message, create the `.env` file or export the variable in the same terminal you run the script from.

## Step 9. Check what it cost

Every call logged its token counts. `spend.py` adds the lines and turns the totals into a dollar estimate with the prices for this model, which were 0.10 dollars per million input tokens and 0.50 dollars per million output tokens when this was tested. Check the provider's price page for current prices.

{{file:spend.py}}

{{cmd:10-spend}}

{{shot:10-spend|Terminal showing 101 calls, the token totals and the estimated cost}}

The whole tutorial run made 101 calls: one for the single review, 50 for v1 and 50 for v2. The tokens and estimated cost are in the output above.

## Troubleshooting

**"ANTHROPIC_API_KEY is not set".** Add the key to `.env` in the folder you run the script from, or export it in the same terminal.

**Some answers are counted as `invalid`.** The model wrote a word that is not one of your labels, as it did with "Neutral" in Step 6. Either add the word to your prompt as a label or tell the prompt to choose only from the three.

**The score changes when I rerun.** Model output varies between runs. Run the same prompt more than once if the score decides something, and look at the wrong rows rather than only the total.

## Frequently asked questions

**How do I measure whether my prompt works?**

Write the expected labels yourself, run the prompt on every example and count the matches. Here, prompt v1 matched 47 of 50 labels, and prompt v2 matched 50 of 50 on the same reviews. Use new reviews to test a prompt fairly.

**How many labelled examples do I need?**

Not tested here. This tutorial used 50 reviews that we wrote. A perfect score on the same reviews used to write the prompt does not show how the prompt does on new ones.

**Can an LLM replace a trained classifier in a hackathon?**

Not tested here. The tutorial did not compare the LLM with a trained classifier. It shows only that the model matched 47 of 50 labels with prompt v1 on the 50 reviews.

## What to try next

- Write 50 more reviews and score v2 on them without changing the prompt.
- Add a fourth label and see which of your own labels the model disagrees with.
- Save the wrong rows from each run and compare them across three or four prompt versions.

## How this tutorial was tested

The tutorial was run on 10 November 2026 on macOS with Python 3.14.6, `anthropic` 2.7.0 and the model `claude-haiku-5-5`. The code blocks are copied from the project files, and the output blocks are the saved output of the real run. The steps were replayed from an empty copy of the folder. Screenshots are terminal-style images rendered from the saved output of each command. They are not captures of a terminal window. Not run: Windows and Linux, and any model other than `claude-haiku-5-5`.
