---
seo_title: Compare Two Models Side by Side for an AI Hackathon
meta_description: Pick a model for your AI hackathon project with data: build a page that sends one prompt to two models and shows both answers with time and tokens.
---
# Build a hackathon app that compares two models side by side

You build a small web page that sends one prompt to two language models and shows the answers in two columns, with the time each call took, the tokens it used and a cost worked out from the listed prices. The backend is about 50 lines of Python.

**Time:** about two hours. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, a browser, and an Anthropic API key. **Tested:** 10 November 2026 with Python 3.14.6, `anthropic` 2.7.0, `fastapi` 0.162.2 and `uvicorn` 0.54.0 on macOS.

Model answers, timings and token counts differ from run to run. Yours will not match the numbers below.

**One provider only.** This tutorial compares two models from one provider, `claude-haiku-5-5` and `claude-sonnet-5-5`, because the Anthropic key is the one the author of this tutorial has. The pattern does not depend on that. To add a model from another provider, add an entry to `models.py` with its prices, write one `ask` function for that provider's client, and the page shows a third column the same way. I did not run any other provider.

Choosing a model is an early decision in an AI hackathon, and your own prompts say more than a leaderboard. If you are still looking for an event to use this in, see the list of [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A model that reads well in a demo of someone else's prompt may not suit yours. If you send the same prompt to two models and put the answer, the wait and the cost next to each other, you decide from your own data in a few minutes. The cost column matters because the two models in this tutorial have different listed prices, and a demo that gets many requests adds that difference up.

## See it running

This is the finished page, opened with a saved result so that opening it makes no model calls. The prompt, answers, times and token counts are real output of the run in Step 3.

{{shot:07-page|The page with two columns, one for claude-haiku-5-5 and one for claude-sonnet-5-5, each showing an answer about API rate limits, the time, input tokens, output tokens and cost}}

The rest of the tutorial builds it from nothing.

## Step 1: Set up the project and the key

Make a folder, create a virtual environment and activate it. The commands from here on assume it is active.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt`:

{{file:requirements.txt}}

Install it. The output lists the versions used for this tutorial.

{{cmd:02-install}}

{{shot:02-install|Terminal listing the installed versions of anthropic, fastapi and uvicorn}}

Put your key in a file named `.env` in the project folder. Copy the placeholder file and edit it:

{{file:.env.example}}

Never paste a real key into code, a screenshot or a chat. Load the file into your terminal session (macOS and Linux):

```bash
set -a; source .env; set +a
```

## Step 2: List the two models and their prices

Everything that differs between models lives in one file. Each entry has the price per million input tokens, the price per million output tokens, and the setting that stops the model from thinking before it answers. I turned thinking off so that the output tokens you see are the answer and nothing else.

The two models name that setting differently. `claude-haiku-5-5` accepts `{"type": "disabled"}`. When I sent that to `claude-sonnet-5-5`, the API refused it with a message to send `{"type": "between_tools"}` instead. So the setting is stored per model. This is the kind of difference you meet when you add a model from a second provider, and it is a reason to keep it in data and not in `if` statements.

The model IDs came from the installed `anthropic` package. The prices came from Anthropic's public pricing page, read on 10 November 2026: $0.10 per million input tokens and $0.50 per million output tokens for `claude-haiku-5-5`, and $2 and $10 for `claude-sonnet-5-5`. Prices change, so check the page before you rely on them.

{{file:models.py}}

The cost arithmetic is easy to get wrong by a factor of a million, so it has a test with fixed numbers and no API call:

{{file:test_cost.py}}

{{cmd:03-cost-test}}

{{shot:03-cost-test|Terminal output: cost checks passed}}

## Step 3: Send one prompt to both models

`compare.py` has one function, `ask`, that sends the prompt to one model, times the call, reads the token counts from `response.usage` and works out the cost. `compare` calls it for each model, one after the other, so the two calls do not share a connection while they are timed. `max_tokens` is 200 to keep each call short.

The script also runs from the command line. If the key is missing it stops with a message. This is what that looks like:

{{shot:04-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

{{file:compare.py}}

Run it with a prompt. The `--save` option writes the result to a file, which Step 5 uses for the page:

{{cmd:05-compare}}

{{shot:05-compare|Terminal output of compare.py: an answer from each model with seconds, input tokens, output tokens and cost}}

In this run both models were sent the same 30 input tokens. Haiku 5.5 answered in 1.53 seconds with 89 output tokens and a cost of $0.000048. Sonnet 5.5 answered in 1.9 seconds with 84 output tokens and a cost of $0.000900. Both answers were a short explanation of rate limits, and you should read them yourself: the script measures time, tokens and cost, and it does not judge which answer is better. One call each is not a benchmark. Run the same prompt several times before you trust a timing.

## Step 4: Put it behind a web route

`app.py` has two routes. `POST /compare` takes a prompt and returns both results. `GET /` serves the page. Two small choices: the prompt is limited to 1 to 500 characters, so an empty prompt is refused with a 422 error before any model is called, and if a model call fails the browser gets a short fixed message, not the provider's error text.

The `?demo=1` option on `GET /` fills the page from the file that `compare.py --save` wrote. It exists so that a screenshot tool, or you, can open a finished page without paying for two calls each time.

{{file:app.py}}

`test_route.py` checks both behaviours against a running server: the empty prompt, then one real prompt. Start the server in one terminal, with any free port:

```bash
uvicorn app:app --port 8042
```

Run the test in a second terminal:

{{file:test_route.py}}

{{cmd:06-route}}

{{shot:06-route|Terminal output of test_route.py: empty prompt rejected with 422, output tokens for both models, route returned 2 columns}}

The empty prompt was rejected with 422, and the route returned one answer per model. In this run the short prompt got 20 output tokens from Haiku 5.5 and 21 from Sonnet 5.5.

## Step 5: Add the page

`index.html` is plain HTML and JavaScript with no build step. It posts the prompt to `/compare`, then builds one column per result. It uses `textContent`, not `innerHTML`, so a model answer is shown as text and never run as markup. The columns stack on a narrow screen.

{{file:index.html}}

Open `http://127.0.0.1:8042/` for the live page, or `http://127.0.0.1:8042/?demo=1` for the saved result. The screenshot at the top of this article is the second one. I did not type into the page and press the button in a browser for this tutorial. The route behind the button was tested in Step 4.

{{shot:07-page|The page opened with the saved result}}

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set`.** Load the key in the terminal you run the command from, then run it again. The web route reads the key when a request arrives, so start the server from a terminal that has it.
- **A 400 error that mentions `thinking`.** The model wants a different thinking setting. Read the message: it names the value to send. Put that value in the model's entry in `models.py`.
- **The page shows "Something went wrong".** Look at the terminal where `uvicorn` runs. The browser only gets a short message by design.
- **`Address already in use`.** An old server is still running on port 8042. Stop it, or pick another port and change `BASE` in `test_route.py`.
- **The `?demo=1` page is empty.** `demo_result.json` does not exist yet. Run `compare.py` with `--save` to create it.

## What to try next

- Add a third column for a model from another provider, using the same entry in `models.py` and an `ask` function for that provider.
- Send both calls at the same time with threads, and say in the page that the timings were measured that way.
- Run a list of ten prompts through `compare` and save every result to a file, so you can read them side by side later.

## How this tutorial was tested

- Date: 10 November 2026. Python 3.14.6, `anthropic` 2.7.0, `fastapi` 0.162.2, `uvicorn` 0.54.0, macOS. The models are `claude-haiku-5-5` and `claude-sonnet-5-5`.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. Model answers, timings and token counts differed between the two runs, as expected.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window. The page screenshot is a real Chrome screenshot of the running page, opened with `?demo=1`, so it shows a saved result.
- In the terminal output the models are shown as "Haiku 5.5" and "Sonnet 5.5", the names in the `label` field, and the full IDs are in the code.
- Not run: typing into the page and pressing the button in a browser, any provider other than Anthropic, Windows, Linux, and Python versions other than 3.14.6.

## Questions people ask

### Which model should I use for an AI hackathon project?

It depends on your prompts, so test them. This tutorial gives you a page that shows two models answering the same prompt with the time and cost next to each answer. In the run above both models answered in two sentences, and the cost differed: $0.000048 for Haiku 5.5 and $0.000900 for Sonnet 5.5. Read the answers yourself, because the page does not score them.

### How do I compare two models fairly?

Send the same prompt, with the same `max_tokens` and the same thinking setting, and read the same fields from each response. Time the calls one after the other, and repeat the prompt several times, since one call each is not enough to trust a timing. This tutorial does the same prompt, limit and setting for you and leaves the repeats to you.

### Does the cheaper model work for a hackathon demo?

For the one prompt in this run, the cheaper model answered in two sentences like the other one, at a lower cost per call. That is one prompt, not a test of your project. Put your own prompts through the page and read both columns before you choose.
