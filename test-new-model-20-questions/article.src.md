---
seo_title: "Test a New Model with Your Own Questions: AI Hackathon Guide"
meta_description: "Test a new model for your AI hackathon project with your own 20 questions. Score two models, record cost and time and write down the result."
---

# Test a new model with your own 20 questions

You build a Python script that asks 20 questions with known answers to two models, scores the replies by a fixed rule, and records the cost and time of each model.

**Time:** about 40 minutes. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, and an Anthropic API key. **Tested:** 11 November 2026 with Python 3.14.6 and the `anthropic` package 2.8.0 on macOS.

Model replies and timings differ from run to run. Your numbers will not match the output below exactly. The shape of the output will.

Sponsors announce new models during an AI hackathon, and your own questions tell you whether a model fits your project. If you are choosing a model for a build, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A vendor chart tells you how a model did on someone else's questions. Your project has its own questions. Twenty questions with answers you can check take under an hour to write, cost a fraction of a cent to run, and give you a number you can repeat. The scoring rule matters as much as the questions, so this tutorial keeps the rule small and shows every line of it.

## See it running first

This is the finished report. Two models answered the same 20 questions. Each row shows the accepted answer and whether each model matched it.

{{shot:06-score|Terminal output of score.py: 20 rows comparing Haiku 5.5 and Sonnet 5.5, with totals of 20 of 20 and 19 of 20 correct and the cost of each}}

The rest of the tutorial builds it from scratch.

## Step 1: Set up the project

Make a folder, create a virtual environment and activate it. The commands from here on assume it is active.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt` with one line:

{{file:requirements.txt}}

Install it. The output below shows the version used for this tutorial.

{{cmd:02-install}}

{{shot:02-install|Terminal showing the anthropic package installed}}

## Step 2: Write 20 questions with checkable answers

Pick questions where a program can decide right or wrong. Here every question has a short answer: a number, a word, or a time. Each entry lists the answers you accept. Some questions allow two forms, such as `3` and `three`.

The questions mix easy facts with a few that need a step of reasoning, such as the bat-and-ball question and the train arrival time. Use your own questions for your own project. These are only examples.

{{file:questions.json}}

## Step 3: Write the scoring rule

The rule is exact match after cleaning. The program lowercases the reply, trims spaces, drops quote marks and one final full stop, and removes thousands commas inside numbers. The reply is correct only if the result equals one of the accepted answers, cleaned the same way. No model judges another model, and no part of a reply is searched for the answer.

This rule is strict on purpose. A reply of `210 minutes` does not match `210`. That keeps the score checkable by anyone, and you will see below that it changes a result. If your project can live with extra words, loosen the rule and write down how.

{{file:score.py}}

The rule is the part of this tutorial most worth checking by hand, so test it on fixed answers before any model is involved. This step makes no API call.

{{cmd:03-test-score}}

{{shot:03-test-score|Terminal output of test_score.py: ten fixed answers, six marked correct and four wrong, ending with all 10 scoring checks passed}}

The four wrong cases show what the rule does not forgive: extra words around the answer, a wrong number, a wrong word and an empty reply.

## Step 4: Describe the two models

The script needs each model's name and its price per million tokens, so it can turn token counts into dollars. Prices change. Copy the real numbers from the provider's price page on the day you run this. The two models are `claude-haiku-5-5` and `claude-sonnet-5-5`.

The `thinking` setting is how each model is told not to think before it answers. The two models name that setting differently, so each carries its own value. The point is to compare short answers fairly.

{{file:models.py}}

## Step 5: Store the key outside the code

Put your key in a file named `.env` in the project folder. Copy the placeholder file and edit it:

{{file:.env.example}}

Then load it into your shell with `set -a; source .env; set +a`. Keep `.env` out of git. The project `.gitignore` already lists it. Never paste a key into a chat or a screenshot.

## Step 6: Run the questions on both models

The script sends each question with one extra line, "Reply with only the final answer. No explanation, no working." It asks one model's 20 questions, then the other's, one call at a time, so the timings do not compete for the same connection. It saves every raw answer, the tokens and the seconds to `results.json`.

{{file:run_eval.py}}

If the key is missing, the script stops with a plain message instead of a long error:

{{cmd:04-no-key}}

{{shot:04-no-key|Terminal output when the key is not set}}

Now run it with the key loaded.

{{cmd:05-run}}

{{shot:05-run|Terminal output of run_eval.py: both models asked 20 questions and results saved}}

The runner does not print the answers. They are in `results.json`, ready for the scorer.

## Step 7: Score and compare

`score.py` reads `results.json` and `questions.json`, applies the rule and prints a table plus one totals line per model.

{{cmd:06-score}}

{{out:06-score}}

What the run showed:

- Haiku 5.5 got 20 of 20. Sonnet 5.5 got 19 of 20.
- The one miss was question 5. Sonnet 5.5 replied `210 minutes`. The number is right, but under the strict rule it is wrong. With a looser rule both models would have scored 20 of 20. This is why the rule must be written down before you read the results.
- Each model sent 889 input tokens. Haiku 5.5 produced 75 output tokens and Sonnet 5.5 produced 79.
- Haiku 5.5 cost $0.000126 and Sonnet 5.5 cost $0.002568, from the prices in `models.py`. Sonnet 5.5 cost about 20 times as much for the 20 questions.
- Time for the 20 calls was 21.9 seconds for Haiku 5.5 and 26.2 seconds for Sonnet 5.5. Timing depends on your network and the load at the time, so repeat it before you rely on it.

Twenty easy questions cannot separate two capable models. Both did well, and the one difference came from formatting, not knowledge. Add harder questions from your own project before you decide.

If you point the scorer at a file that does not exist, it says so:

{{cmd:07-missing}}

{{shot:07-missing|Terminal output when the results file is missing}}

## Step 8: Write down the result

Keep a short note next to the results. Use these lines as a template and fill in your own numbers:

- Date, model names, and the price per million tokens you used.
- The scoring rule, in one sentence, and the date you wrote it.
- Score per model, cost per model, seconds per model.
- Every miss and why it was a miss, so a reader can see if the rule or the model caused it.
- What you did not test.

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set`.** The key is not in your shell. Run `set -a; source .env; set +a` in the same terminal, then run the script again.
- **An authentication error from the API.** The key is wrong or revoked. Create a new one in your Anthropic account and update `.env`.
- **A model's answer is right but marked wrong.** Open `results.json` and compare the raw reply with the accepted answers. Either add the form to `accept` or loosen the rule, and note the change.
- **The model name is not found.** Model names change. Check the current names in the provider's documentation and update `models.py`.
- **A reply is cut off or empty.** The script limits each reply to 200 tokens. Raise `MAX_TOKENS` in `models.py` if your questions need longer answers.

## Frequently asked questions

**How do I know if a new model fits my project?**

Write questions from your own project with answers a program can check, run them on the new model and on the one you use now, and compare the scores, cost and time. In this test one model scored 20 of 20 and the other 19 of 20, and the difference came from a reply with extra words.

**How many test questions do I need?**

This tutorial used 20, which is enough to see the method work and to spot formatting problems. It was not enough to separate two capable models, because both scored almost the same. The test did not find a number to recommend. Add questions until the results stop changing when you add more.

**Can I trust a model leaderboard for my hackathon idea?**

A leaderboard measures someone else's questions. This tutorial did not test any leaderboard. It shows how to measure your own questions, which is the only score that reflects your project.

## What to try next

- Add 10 harder questions from your own project and see whether the two models separate.
- Run the same 20 questions three times and check how much the score and time move.
- Add a second scoring rule that accepts a number inside a longer reply, and compare both scores.

## How this tutorial was tested

- Date: 11 November 2026. Python 3.14.6, `anthropic` 2.8.0, macOS. The models are `claude-haiku-5-5` and `claude-sonnet-5-5`.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. In the replay the totals were again 20 of 20 and 19 of 20, with different timings, as expected.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run: Windows, Linux, Python versions other than 3.14.6, models other than the two named, and more than one run of the 20 questions per pass. The prices in `models.py` were not checked against a live price page on the test date.
