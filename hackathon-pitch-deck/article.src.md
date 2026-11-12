---
title: "Make an AI Hackathon Pitch Deck in Five Slides"
seo_title: "Make an AI Hackathon Pitch Deck in Five Slides"
meta_description: "Make an AI hackathon pitch deck in five slides from your repo: problem, demo, how it works, what is next and team. Includes a timing guide."
description: "Make an AI hackathon pitch deck in five slides from your repo: problem, demo, how it works, what is next and team. Includes a timing guide."
---

# Make a hackathon pitch deck from your repo in five slides

You build a Python tool that reads your project README, asks a model to tighten it into five slides with speaker notes, draws the architecture picture, and checks that the talk fits a time limit.

**Time:** about 30 minutes. **Level:** beginner. **You need:** Python 3.10 or newer, an Anthropic API key, Google Chrome (only to take the screenshot of the deck), and a project with a README. **Tested:** 11 November 2026 with Python 3.14.6 and the `anthropic` package 2.8.0 on macOS.

An AI hackathon pitch is short, so each slide has one job, and most of what you need is already in your README. If you plan to enter, see the [upcoming AI hackathons](/ai-hackathons/).

The model's wording changes on every run. Your slide text and token counts will not match this page exactly. The shape of the output will.

## Why this matters

A short pitch with one idea per slide is easier to follow than a long deck. A README that already names the problem, the steps and the team gives you the raw material. This is a design choice of this tutorial, not a tested claim about judges. Building the deck from the README also keeps the deck and the repo from telling two different stories.

## See it running first

This is the finished deck for a small example project called Action Catcher, which lists who agreed to do what in a meeting. The people in its README are made up.

{{shot:07-view|Five slides in a grid: the problem, a demo terminal, a four-box flow picture with three bullets, what is next, and the team}}

The rest of the tutorial builds it from scratch.

## Step 1: Set up the project

Create a virtual environment. The commands from here on assume it is active.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt` with one line:

{{file:requirements.txt}}

Install it. The output shows the version used for this tutorial.

{{cmd:02-install}}

{{shot:02-install|Terminal after installing the anthropic package, showing version 2.8.0}}

The tool also needs your API key in the `ANTHROPIC_API_KEY` environment variable. Put it in a `.env` file that is listed in `.gitignore`, and never paste it into a script. A `.env.example` with the variable name and no value is safe to share:

{{file:.env.example}}

## Step 2: Write the README the deck is built from

The deck can only say what the README says. The tool looks for five headings: Problem, Demo, How it works, What is next and Team. It also looks for one line in How it works that starts with `Flow:` and lists boxes separated by `->`. That line becomes the architecture picture.

{{file:sample-repo/README.md}}

Add a short demo to the project. Slide two needs a real screenshot of your project running, so there is something to take a picture of. The example reads a notes file and prints one line per task.

{{file:sample-repo/demo.py}}

Run it. This output is the demo screenshot that goes on slide two.

{{cmd:03-demo}}

{{shot:03-demo|Terminal output of demo.py listing four tasks with owners}}

The output shows four tasks. It also shows a rough edge: the line "Priya to do the slides for Friday" becomes "the slides for Friday". The tool is a demo, not a product, and a pitch can show that honestly.

## Step 3: Pull the parts out of the README

Before any model call, split the README into sections with plain code. A pitch built from a model's guess about your project would drift from what the repo says. Splitting first also tells you what is missing.

{{file:readme_parts.py}}

Run it on the example.

{{cmd:04-parts}}

{{shot:04-parts|Terminal output listing the word count of each README section and four flow boxes}}

The Problem section has 52 words, far too many for a slide. That is why the next step asks a model to shorten it. The flow line gave four boxes.

### What a mistake looks like

A README with only a Problem section has nothing to build four of the slides from. The script reports each missing heading and exits with code 1, so you fix the README before you spend an API call.

{{cmd:05-missing}}

{{shot:05-missing|Terminal output saying the Demo, How it works, What is next and Team sections are missing}}

## Step 4: Build the five slides

This script sends the five sections to the model once and asks for JSON: one sentence for the problem, a caption for the demo, three short bullets each for how it works and what is next, the team lines, and speaker notes for each slide. The prompt tells the model to use only facts from the README and to add no numbers.

The script then writes `deck/index.html`, with the demo screenshot and the flow picture drawn as inline SVG from the `Flow:` line, and `deck/deck.json`, which holds the slide text and notes.

{{file:build_deck.py}}

One setting needed care. The first attempt used `MAX_TOKENS = 900` and failed with a JSON error. The reply contained only a thinking block that used all 900 tokens, with no text in it. Raising the limit to 4000 fixed it. If you see "Expecting value: line 1 column 1" from `json.loads`, check `response.stop_reason` and the block types before you change the prompt.

Run it. The second argument is the demo image from Step 2.

{{cmd:06-deck}}

{{out:06-deck}}

{{shot:06-deck|Terminal output of build_deck.py listing the five slides and the token counts}}

This run sent 558 input tokens and received 3236 output tokens. Your counts will differ.

## Step 5: Look at the deck

Serve the folder and open it in a browser. The page shows all five slides in a grid so you can check them at once.

{{cmd:07-view}}

{{shot:07-view|The five-slide deck in a browser}}

Check each slide against the README. Slide one has one sentence. Slide two has the demo screenshot. Slide three has three bullets and the four-box flow. Slide four has three next steps taken from the README list. Slide five has the three team lines. If a slide says something your README does not, fix the README or the text, not the check.

## Step 6: Time the talk

Speaker notes are written for speaking, so the time is the word count divided by the speaking rate. The script uses 130 words per minute, a slow, clear pace. It is an assumption, so practise once with a timer and change the number to your own pace.

{{file:timing.py}}

Run it with a three-minute limit.

{{cmd:08-time}}

{{shot:08-time|Terminal output showing seconds per slide and a total of 82 seconds}}

The five notes add up to 82 seconds, so a three-minute slot has room for the demo to run live. Check the rules of your event, because the time allowed differs.

### What a talk that is too long looks like

With a limit of 60 seconds the same deck fails, and the script says by how much.

{{cmd:09-over}}

{{shot:09-over|Terminal output saying the talk is over a 60 second limit by 22 seconds}}

## Troubleshooting

**`Address already in use` when I serve the deck.** Another program holds the port. Pass a different number to `python -m http.server`.

**`Expecting value: line 1 column 1` from `build_deck.py`.** The model reply had no text. Print `response.stop_reason`. If it is `max_tokens`, raise `MAX_TOKENS`.

**`ANTHROPIC_API_KEY is not set`.** Load your `.env` into the shell before you run the script.

**A slide has a bullet that is not in my README.** The prompt asks for README facts only, but a model can still add words. Read every slide before you present.

## Frequently asked questions

**How many slides do I need for an AI hackathon pitch?**

This tutorial uses five: problem, demo, how it works, what is next and team. The five spoken notes took about 82 seconds at 130 words per minute. Your event may set its own length, so check its rules.

**Do I need a pitch deck for an online AI hackathon?**

This tutorial did not test that, and the answer depends on the event. Read the submission rules. If a deck is allowed, the same five slides work as a short video script.

**What do judges want to see in an AI hackathon pitch?**

This tutorial cannot say what a particular judge wants. It builds the parts most pitches contain: the problem, a working demo, how it works, the plan after the event and the people. A real demo is the part you cannot build from the README alone, which is why Step 2 runs the project.

## What to try next

- Change the Flow line and rebuild to see how the picture changes with five or six boxes.
- Ask the model for a one-line title for each slide and compare it with the headings here.
- Replace the terminal image on slide two with a screenshot of your own app.

## How this tutorial was tested

- Date: 11 November 2026. Python 3.14.6, `anthropic` 2.8.0, macOS. The model is `claude-haiku-5-5`, set in the `MODEL` constant.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of a real API call.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. The model's wording differed between the two runs, as expected.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window. The deck screenshot is a real Chrome screenshot of the page.
- The example project and its team are made up for this tutorial.
- Not run: Windows, Linux, Python versions other than 3.14.6, exporting the deck to PowerPoint or PDF, and any browser other than Chrome.
