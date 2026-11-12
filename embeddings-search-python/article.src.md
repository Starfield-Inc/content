---
title: "Embeddings and Semantic Search in Python"
seo_title: "Embeddings and Semantic Search for AI Hackathon Projects"
meta_description: "Learn text embeddings and semantic search for AI hackathon projects: embed a small text set, find the closest match and see where it fails."
---

# Turn text into embeddings and find similar sentences in Python

You build a script that turns 20 sentences into vectors, then finds the three sentences closest in meaning to a question. You also run it on three questions where it goes wrong.

**Time:** about 40 minutes, most of it the first model download. **Level:** intermediate. **You need:** Python basics and Python 3.10 or newer. No API key. **Tested:** 11 November 2026 with Python 3.14.6, `fastembed` 0.9.1, `numpy` 2.5.4 and `onnxruntime` 1.31.1 on macOS.

Semantic search is behind many AI hackathon projects, from document question answering to recommendations. If you plan to build one, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A keyword search finds the words you typed. An embedding search finds text with a similar meaning, even when no word is shared. A model turns each text into a list of numbers, and texts with similar meaning get lists that point in a similar direction. Searching then means comparing lists of numbers.

Anthropic does not offer an embeddings API, so this tutorial runs a small open model on your own machine. No text leaves your computer, and no account is needed.

**The model.** `BAAI/bge-small-en-v1.5`, published under the MIT licence. The `fastembed` library (Apache-2.0) loads a quantized ONNX build of it from the Hugging Face repository `Qdrant/bge-small-en-v1.5-onnx-Q`, which is also marked MIT on its model page. The download is about 66 MB. On the test machine it took about 50 seconds the first time. The files are then kept in a `models/` folder inside the project, and later runs load them from there. It is an English model. Check the licence pages yourself before you use it in a product.

## See it running first

This is the finished search answering a question. The top sentence shares almost no words with the question: it says "ferry", the question says "boat".

{{shot:05-top3|Terminal output of search.py: the ferry sentence scores 0.605 for the question about a boat to the island}}

The rest of the tutorial builds it from scratch.

## Step 1: Set up the project

Make a folder, create a virtual environment and activate it. The commands from here on assume it is active.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt`:

{{file:requirements.txt}}

Install it:

{{cmd:02-install}}

{{shot:02-install|Terminal listing the installed versions of fastembed, numpy and onnxruntime}}

`fastembed` runs the model through `onnxruntime`, so there is no large machine-learning framework to install. On the test machine, wheels were available for Python 3.14.

## Step 2: Write the sentences

`sentences.txt` holds 20 sentences, one per line. They cover travel, cooking, pets, weather and hackathon life. Some are there on purpose to cause trouble later: two use the word "bank" in different ways, and one says the soup was *not* hot.

{{file:sentences.txt}}

## Step 3: Embed the sentences

`common.py` keeps the model name and the small helpers in one place. `cache_dir` points the download at a `models/` folder in the project, so the model is easy to find and delete.

{{file:common.py}}

`embed_sentences.py` embeds all 20 sentences at once and saves the result.

{{file:embed_sentences.py}}

Run it. The first run downloads the model.

{{cmd:03-embed}}

{{shot:03-embed|Terminal output of embed_sentences.py: 20 sentences, vector array shape (20, 384), and the progress of the model download}}

The shape `(20, 384)` means 20 vectors of 384 numbers each. One number alone means nothing. The meaning is in the direction of the whole list. In this run the model took 51.9 seconds to load, nearly all of it the download. A second run loads in a moment, because the files are already in `models/`. Your time depends on your connection.

## Step 4: Embed a question and compare it

To compare a question with a sentence, embed the question with the same model, then measure the angle between the two vectors. That measure is cosine similarity. It is 1.0 when two vectors point the same way and falls as they drift apart. A vector compared with itself gives exactly 1.0.

The code is the `cosine` function in `common.py` above. `compare.py` uses it on one question and three sentences.

{{file:compare.py}}

{{cmd:04-compare}}

{{shot:04-compare|Terminal output of compare.py: the ferry sentence scores 0.605, the cat sentence 0.286, the Python sentence 0.365, and the question against itself 1.000}}

The ferry sentence scores 0.605 and the two unrelated sentences score 0.286 and 0.365. These scores are not percentages. For this model, a good match tends to land around 0.6 to 0.8 and unrelated text around 0.3 to 0.5. Another model has another range, so look at your own numbers before you pick a threshold.

## Step 5: Show the top three

`search.py` embeds the question, scores it against every saved vector, sorts, and prints the top matches.

{{file:search.py}}

{{cmd:05-top3}}

{{shot:05-top3|Terminal output of search.py for the boat question: ferry 0.605, rain 0.518, train 0.497}}

The ferry sentence wins at 0.605. The second and third places, a weather sentence at 0.518 and a train sentence at 0.497, are weak matches. They are the next-closest of 20, not good answers. Remember that: a search always returns something.

Try a second question with a clearer answer:

{{cmd:06-top3-cook}}

{{shot:06-top3-cook|Terminal output of search.py for the onion question: the onion sentence scores 0.791}}

The onion sentence scores 0.791, well above the 0.524 of the runner-up. When the gap between first and second is large, you can trust the top result more.

## Step 6: See where embeddings fail

Embeddings are useful and they are wrong in predictable ways. Here are three, each from a real run.

**Failure one: negation.** The question says the soup was hot and the bread fresh. The sentence in the file says the opposite.

{{cmd:07-negation}}

{{shot:07-negation|Terminal output of search.py: the sentence saying the soup was not hot and the bread stale scores 0.845 for a question saying hot and fresh}}

It scores 0.845, the highest score in this tutorial. The two sentences talk about the same things (soup, bread, temperature, freshness), so their vectors are close, even though the meanings are opposite. If your project depends on yes versus no, an embedding score alone will not tell them apart.

**Failure two: a shared word pulls in the wrong topic.** The question asks where to sit by the water.

{{cmd:08-keyword}}

{{shot:08-keyword|Terminal output of search.py: rain scores 0.562, the plant watering reminder 0.525 and the picnic by the river 0.509}}

The sentence we wanted, the picnic on the river bank, comes third at 0.509. A weather sentence is first at 0.562, and a sentence about watering plants is second at 0.525. The scores are close together. With this small model and 20 sentences, a gap that small is a warning sign.

**Failure three: no answer in the text.** The question asks for the capital of France. None of the 20 sentences says anything about it.

{{cmd:09-no-answer}}

{{shot:09-no-answer|Terminal output of search.py for the capital of France: the top match is a train sentence at 0.405}}

The search still returns three sentences, with the top one at 0.405. It has no way to say "nothing here". It only ranks what it has.

## Step 7: Add a minimum score, and see its limit

A common fix is to hide anything below a minimum score. `search.py` takes `--min-score` for this (it is in the code above).

{{cmd:10-min-score}}

{{shot:10-min-score|Terminal output: no sentence scored 0.5 or higher for the capital of France}}

For the France question this works: the highest score was 0.405, so nothing passes. Now run the boat question with the same threshold:

{{cmd:11-min-score-leak}}

{{shot:11-min-score-leak|Terminal output: the ferry sentence at 0.605 and the weather sentence at 0.518 both pass a minimum score of 0.5}}

The weather sentence scores 0.518, so it passes the same threshold of 0.5. A fixed cut-off helps, and it does not separate good matches from bad ones cleanly. Pick a value by looking at scores for your own questions, and test it again if you change the model.

## Step 8: Check what a mistake looks like

Run `search.py` in a folder that has no `vectors.npy`:

{{cmd:12-missing}}

{{shot:12-missing|Terminal output: Cannot find vectors.npy, run embed_sentences.py first}}

You get a clear message and exit code 2 instead of a long error trace.

## Troubleshooting

- **The first run seems stuck.** It is downloading about 66 MB. The progress bar shows it. If it fails with a network error, run `python embed_sentences.py` again.
- **`ModuleNotFoundError: No module named 'fastembed'`.** The virtual environment is not active, or the install did not finish. Activate it and run `pip install -r requirements.txt` again.
- **A warning about unauthenticated requests to the Hugging Face Hub.** The model download does not need an account. The warning says only that you are not logged in, so you may see slower downloads. The scripts set `HF_HUB_VERBOSITY=error` in this tutorial's test runs to keep the screenshots short. You do not need to.
- **`vectors.npy does not match sentences.txt`.** You edited `sentences.txt` after embedding. Run `python embed_sentences.py` again.
- **Your scores differ slightly from the ones above.** Another version of `fastembed`, `onnxruntime` or the model files can change the numbers in the third decimal place or more. The order of the results should stay the same for these questions, but this was only checked on one machine.

## Frequently asked questions

**What are embeddings used for in AI hackathon projects?**

An embedding turns text into a list of numbers so a program can compare meaning. The most common use is search: embed your documents once, embed each question, and return the closest documents. In this tutorial 20 sentences became 20 vectors of 384 numbers, and the boat question found the ferry sentence at 0.605 without sharing a keyword.

**Do I need a vector database for a hackathon project?**

Not for a small set. Here the vectors sit in one NumPy array saved to `vectors.npy`, and the search compares the question with all 20 of them in a loop. A vector database becomes useful when a set is too big to compare one by one. This tutorial did not test where that limit is.

**How many documents can I search in a weekend project?**

This tutorial tested only 20 sentences, so it cannot give a limit. What it shows is that the model, not the count, set the quality: negation and shared words fooled the search with just 20 items. Test with your own text first, and add a minimum score and a manual check before you trust the results.

## What to try next

- Add 30 sentences of your own and see which questions start to fail.
- Compare `BAAI/bge-small-en-v1.5` with another model from the `fastembed` list on the same questions.
- Print the score gap between first and second place, and hide results when the gap is small.

## How this tutorial was tested

Every command and every screenshot above comes from one real run on 11 November 2026. The code in the blocks is copied from the project files, not retyped. The steps were then run again from an empty folder, and all of them passed with the same search results. The screenshots show the saved output of those commands in a terminal-style frame, rendered from the saved log. They are not captures of a window.

Not run: Windows and Linux, other Python versions than 3.14.6, a GPU, models other than `BAAI/bge-small-en-v1.5`, and sets of more than 20 sentences. The tutorial makes no call to the Anthropic API.
