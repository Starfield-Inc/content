---
title: "Set Up Jupyter in a Virtual Environment and Run a Notebook Headless"
seo_title: "Jupyter Notebook Setup in Python for AI Hackathons"
meta_description: "Set up Jupyter for your AI hackathon: virtual environment, a notebook that calls an LLM and draws a chart, then run it headless with nbconvert."
description: "Set up Jupyter for your AI hackathon: virtual environment, a notebook that calls an LLM and draws a chart, then run it headless with nbconvert."
---

# Set up Jupyter in a virtual environment and run a notebook from the command line

You will install Jupyter in a virtual environment, write a notebook that asks a model to label eight sentences and charts the result, then run the whole notebook without opening a browser. It takes about 30 minutes.

**Level:** Beginner. **You need:** Python 3.10 or newer, a terminal and an Anthropic API key. **Tested:** 12 November 2026 on macOS with Python 3.14.6, `notebook` 7.6.5, `nbconvert` 7.17.2 and `anthropic` 2.8.0. The Windows activation command comes from the Python docs and was not run.

In an AI hackathon you often explore data in a notebook, then need the same steps to run again on a clean machine before a demo. A virtual environment makes the setup repeatable, and a headless run proves the notebook works from top to bottom. When you are ready to use it, see the [upcoming AI hackathons](/ai-hackathons/).

## Why a virtual environment and a headless run

A notebook remembers the order in which you ran its cells, not the order they appear in. A notebook that works on your screen can fail on a fresh run. Running it headless executes every cell from the top, in order, and saves the outputs. If it passes, anyone with the same packages gets the same steps.

## See it running first

By the end one command runs the notebook and writes the chart below. The rest of this tutorial builds it from scratch.

{{shot:08-chart|A bar chart with the counts of questions, statements and requests that the model found in eight sentences}}

## Step 1. Create a virtual environment

A virtual environment keeps this project's packages apart from the rest of your machine. In an empty folder, run:

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Activate it. On macOS and Linux use `source .venv/bin/activate`. On Windows use `.venv\Scripts\activate`. Every command below assumes it is active.

## Step 2. Install the packages

List what the project needs in `requirements.txt`, so anyone can install the same set. `ipykernel` lets Jupyter run your code with this environment's Python.

{{file:requirements.txt}}

{{cmd:02-install}}

{{shot:02-install|Terminal: the last lines of pip install, ending with Successfully installed}}

The install downloads a lot of small packages, so allow a few minutes. Your versions will be newer if you install later. List the versions that were installed:

{{cmd:02b-list}}

{{shot:02b-list|Terminal: pip list showing the installed notebook, nbconvert, ipykernel, anthropic and matplotlib versions}}

## Step 3. Check that Jupyter is installed

{{cmd:03-check}}

{{shot:03-check|Terminal showing the ipykernel, nbconvert and notebook versions}}

To work in the browser, run `jupyter notebook` in this folder. It opens a page where you create a notebook and type the cells below. This tutorial did not drive that browser page. It built the same notebook from files, so every run could be replayed.

## Step 4. Write the notebook cells

The notebook has three code cells. Each is its own file in `cells/`, so you can read it here and paste it into a cell. The first cell loads the libraries and stops with a clear message if the key is missing. Set the key in your terminal before you start Jupyter, for example `export ANTHROPIC_API_KEY=...` on macOS and Linux. Never paste a key into a cell, because a notebook saves everything you type.

{{file:cells/01_setup.py}}

The second cell sends one request to `claude-haiku-5-5`. It asks for one label per line, so the reply is easy to split. Thinking is turned off so the small `max_tokens` limit is spent on the answer.

{{file:cells/02_ask.py}}

The third cell counts the labels and draws a bar chart. It also saves the chart as `chart.png`.

{{file:cells/03_chart.py}}

To get the same notebook file as this tutorial, this script assembles the cells into `first_notebook.ipynb`:

{{file:build_notebook.py}}

{{cmd:04-build}}

{{shot:04-build|Terminal after the notebook file is written, showing 4 cells}}

The 4 cells are the three code cells plus a title cell.

## Step 5. Run the notebook headless

`nbconvert` runs every cell in order and writes a new notebook with the outputs filled in. The original file stays unchanged.

{{cmd:05-run}}

{{shot:05-run|Terminal output of nbconvert running the notebook and writing executed.ipynb}}

The run takes a few seconds. The kernel warning about plain TCP is normal on a local run. Nothing leaves your machine except the one API request.

## Step 6. Read what the run saved

The outputs are stored inside `executed.ipynb`. This small script prints the text outputs of each cell.

{{file:show_outputs.py}}

{{cmd:06-outputs}}

{{shot:06-outputs|The labels the model gave, the token usage and the chart output}}

The model labelled 2 sentences as questions, 3 as statements and 3 as requests. The request used 135 input tokens and 20 output tokens. A model can label differently on another run, so your counts may differ.

## Step 7. Export the result to HTML

An HTML file is easy to share with a teammate who has no Jupyter. It holds the code, the outputs and the chart.

{{cmd:07-html}}

{{shot:07-html|Terminal output of nbconvert writing executed.html}}

The warning about alternative text only means the chart image has no description. The export still works.

## Step 8. Check what a mistake looks like

Run the same notebook in a shell where the key is not set. The first cell stops the run.

{{cmd:09-nokey}}

{{shot:09-nokey|The error message when the key is missing}}

The command ends with exit code 1. A script or a scheduler can use that code to tell that the notebook failed.

## Troubleshooting

- **`jupyter: command not found`.** The virtual environment is not active. Activate it and try again.
- **`No module named 'anthropic'` inside the notebook.** The notebook is using a different Python. Start `jupyter notebook` from the activated environment.
- **The run stops with "Set ANTHROPIC_API_KEY".** The key is not in the environment of the shell that started Jupyter or `nbconvert`. Export it there and run again.
- **The chart does not show in the notebook.** Run the chart cell after the cell that creates `labels`. Cell order matters.

## Frequently asked questions

**How do I set up Jupyter for an AI hackathon project?**

Create a virtual environment, install `notebook`, `ipykernel` and the libraries you need from a `requirements.txt`, then run `jupyter notebook`. In the test the install gave `notebook` 7.6.5 and `ipykernel` 7.4.0.

**How do I run a Jupyter notebook without opening it?**

Use `jupyter nbconvert --to notebook --execute first_notebook.ipynb --output executed.ipynb`. It runs every cell in order and saves the outputs in a new file. Add `--to html` to export a page you can share.

**Why does my notebook fail on a clean run?**

The cells may depend on the order you ran them, or on a package or key that only your session had. A headless run starts from the top with only the environment you give it. In this tutorial it stopped with exit code 1 when the key was missing.

## What to try next

- Change the sentences, or add a fourth label, and run the notebook again.
- Read the sentences from a CSV file instead of a list.
- Run the notebook on a schedule and keep the HTML export.

## How this tutorial was tested

Every command and screenshot above comes from one real run on 12 November 2026. The code in the blocks is copied from the project files, not retyped. The steps were then run again from an empty folder, and all of them passed. The model call used `claude-haiku-5-5`, and the notebook ran against the real API. The terminal screenshots show the saved output of each command in a terminal-style frame. The chart is a real browser screenshot of the saved `chart.png`. Not run: Windows, Linux, and the browser-based Jupyter page opened by `jupyter notebook`.
