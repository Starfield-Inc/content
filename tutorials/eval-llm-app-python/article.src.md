---
title: "Write Evaluation Tests for Your AI Hackathon App"
seo_title: "Write Evaluation Tests for Your AI Hackathon App"
description: "AI hackathon testing: write an evaluation script with 20 test cases. Print a pass rate and run it before each change."
meta_description: "AI hackathon testing: write an evaluation script with 20 test cases. Print a pass rate and run it before each change."
---

# Write an evaluation script with 20 test cases for your LLM app

You build a Python script that sends 20 test messages through a small LLM app, checks each reply by rule and prints a pass rate. You then read a failing case, change the prompt, and compare two runs of the same prompt.

**Time:** about 45 minutes. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, and an Anthropic API key. **Tested:** 11 November 2026 with Python 3.14.6 and the `anthropic` package 2.8.0 on macOS 26.

Model replies differ from run to run. Your pass rate and your failing cases may not match the output below. The method will.

A pass rate you can run in a minute lets an AI hackathon team change a prompt late at night without fear that an earlier answer broke. If you plan to build an app for a weekend event, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

You change a prompt, try two questions by hand, and ship it. The two questions work. A third one, which you did not try, now fails. An evaluation script is the habit that catches this. It keeps a fixed list of questions, runs them all, and gives you one number to compare before and after a change.

The app here is a support-reply function for a made-up tea shop. It gets a customer message and a short list of shop facts, and it writes a reply. The checks are plain Python rules, so you do not need a second model to grade the first.

## See it running first

This is the finished script after the prompt change. It ran 20 cases and passed 19.

{{shot:08-eval-v2-a|Terminal output of run_eval.py: 20 cases listed as PASS or FAIL, 19 of 20 passed, pass rate 95 percent, english-only failed}}

The rest of the tutorial builds it from scratch.

## Step 1: Set up the project

Make a folder, create a virtual environment and activate it. The commands from here on assume it is active.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt` with one line:

{{file:requirements.txt}}

Install it. The output shows the version used for this tutorial.

{{cmd:02-install}}

{{out:02-install}}

## Step 2: Write the app you want to test

The app is one function, `reply(message, prompt)`. It sends the shop facts as a system prompt and returns the reply text. It has two prompts, `v1` and `v2`, so you can test a change against the old version. `v1` is the first draft. Ignore `v2` for now.

Two details come from trial and error by other builders with this model. Thinking is turned off, because with thinking on and a small `max_tokens` a reply can hold only a thinking block and no text. I did not turn it on to reproduce that here. And `reply` joins only the text blocks, so an empty reply comes back as an empty string, not an exception. The eval treats an empty string as a failure.

{{file:app.py}}

Put your key in a `.env` file next to the code. Copy the placeholder and edit it:

{{file:.env.example}}

Without a key, the script stops with a clear message instead of a stack trace:

{{cmd:03-no-key}}

{{out:03-no-key}}

Now call the app once, by hand.

{{cmd:04-one-reply}}

{{shot:04-one-reply|Terminal output of app.py answering a shipping question}}

The reply is correct, and it adds a sum of its own: 5 to 7 business days in total. That figure is not in the shop facts. It is arithmetic from them, so the reply is still accurate. This is the kind of thing a single hand test hides and a list of cases forces you to decide about.

## Step 3: Write 20 cases with expected facts

Each case has a customer message and the rules its reply must meet. There are three kinds of rule:

- `must_include`: a list of groups. Each group is a list of acceptable phrasings, and the reply must contain at least one from every group.
- `must_not_include`: phrases that must not appear, such as a promise the policy does not allow.
- `max_words`: a length limit.

The 20 cases cover facts from the shop list (shipping time, cost, returns, hours), questions the facts cannot answer (caffeine, organic, refund timing), and messages that try to change the app's behaviour (a request for a promised refund, a request for pirate speak, a message in Spanish).

{{file:cases.json}}

I first wrote the `return-opened` case with `must_not_include: ["full refund"]`. It failed on a correct reply, because the reply explained that unopened tins get a full refund. The rule was wrong, not the app. I changed it to forbid only phrases that promise a refund for this order, such as "will refund". Read the failing reply before you blame the prompt.

## Step 4: Write the checker and the runner

`check` returns a list of reasons a reply fails, and an empty list means it passed. `main` runs every case, prints PASS or FAIL, saves everything to a JSON file and prints the pass rate. The `--fail-under` option makes the script exit with code 1 when the rate is too low, so a shell script or a CI job can stop on it.

{{file:run_eval.py}}

The checker is code too, so test it. These five tests use fixed replies and make no API call.

{{file:test_checks.py}}

{{cmd:05-test-checker}}

{{shot:05-test-checker|Terminal output of five passing unit tests for the checker}}

## Step 5: Run the 20 cases

{{cmd:06-eval-v1}}

{{shot:06-eval-v1|Terminal output of run_eval.py with prompt v1: 17 of 20 passed, pass rate 85 percent}}

Prompt `v1` passed 17 of 20, a pass rate of 85%. The failures were `angry`, `inject-pirate` and `english-only`. The pass rate is a summary. The next step is to read the failures.

## Step 6: Read the failing cases

`show_failures.py` prints the message, the reason and the reply for each failed case in a saved results file.

{{file:show_failures.py}}

{{cmd:07-failures}}

{{shot:07-failures|Terminal output of show_failures.py listing three failing cases with their replies}}

Each failure says something different:

- `angry`: the reply was 119 words and the limit was 90. The content is fine. The reply is too long for an upset customer.
- `inject-pirate`: the customer asked for pirate speak, and the bot did it, down to "Ahoy, matey!". The facts in it are right.
- `english-only`: the customer wrote in Spanish and the bot answered in Spanish. Whether that is a bug depends on what you want. I decided this shop's support replies are English, so I count it as one.

## Step 7: Change the prompt and run again

The change in `v2` is a block of rules added after the shop facts: use only the facts, say "I do not know" and hand over to the team when the facts do not answer, never promise a refund, always reply in plain English with no role-play voice, stay under 70 words, and ignore messages that ask to change these rules. It is in `app.py` above.

{{cmd:08-eval-v2-a}}

Prompt `v2` passed 19 of 20, a pass rate of 95%. `angry` and `inject-pirate` now pass. `english-only` still fails, although the prompt says to reply in English. The model replied in Spanish anyway. I did not find a wording that fixed it, and I did not keep trying, because this tutorial is about the eval, not about this prompt. The failing case stays in the list. A case you cannot fix yet is useful: it tells you what the app still does not do.

One run on its own does not prove `v2` is better than `v1`. The next step shows why.

## Step 8: Run it twice and compare

The same prompt, the same 20 cases, a second run:

{{cmd:09-eval-v2-b}}

{{cmd:10-compare}}

{{shot:10-compare|Terminal output of compare_runs.py: both runs 95 percent, no verdict changed, 1 of 20 replies word-for-word identical}}

Both runs scored 95% and no case changed its verdict. But only 1 of 20 replies was word-for-word identical. The wording changes every time. The checks passed twice because they test for facts, not for exact text.

That is the good case. It did not always go that way while I was building. With `v1`, the `angry` case passed in one of my build runs and failed in the saved run, and its reply length varies from run to run. I did not look into why. Two runs of 20 cases cannot tell a real change of 5 points from this kind of noise. If you compare two prompts, run each more than once, and look at which cases changed, not only at the rate.

Show the gate with one case. The `english-only` case fails, so `--fail-under 100` exits with code 1:

{{cmd:11-gate}}

{{shot:11-gate|Terminal output of a one-case run that fails and exits with code 1}}

Run the script before each prompt change and again after it. If the rate drops, or a case that passed now fails, you know before you ship.

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set`.** The key is not in `.env` and not exported in the terminal you are using.
- **A case fails and the reply looks right.** Read the "Why it failed" line. In my build the first `return-opened` rule was too broad. Fix the rule, then rerun.
- **A reply comes back empty.** With thinking on and a low `max_tokens`, the model can spend the whole budget on thinking and send no text. The app here turns thinking off. If you turn it on, raise `MAX_TOKENS`.
- **The pass rate changes between runs.** Replies differ every time. Look at which cases changed. If it is always the same one or two, tighten or loosen those rules.

## Frequently asked questions

**How many test cases does a hackathon app need?**

Enough to cover each fact and each way the app can go wrong. This tutorial used 20: 15 for facts and questions the facts cannot answer, 2 for tone and length, and 3 for attempts to change the rules. The tutorial did not test whether a different number is better.

**How do I score free-text answers?**

With rules that look for facts, not exact words. Here each case lists acceptable phrasings, forbidden phrases and a word limit. Across two runs only 1 of 20 replies matched word for word, yet no verdict changed. Rules like these cannot judge tone or style. This tutorial did not use a second model as a grader.

**When should I run the tests?**

Before and after every prompt change, and again whenever you change the model. Run the same prompt more than once if the rate matters, because the results move between runs.

## What to try next

- Add a case each time a real user message goes wrong, so the list grows from real failures.
- Run each case three times and count a case as passed only if all three pass.
- Use `--fail-under` in a script that runs before you commit.

## How this tutorial was tested

- Date: 11 November 2026. Python 3.14.6, `anthropic` 2.8.0, macOS 26. The model is `claude-haiku-5-5`, set in the `MODEL` constant in `app.py`.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls. The shop, its facts and the customer messages are made up.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. Model replies differ between runs, so the replay can show different numbers from the ones above. In the replay here, `v1` scored 85% and `v2` scored 95% twice, with the same failing cases, but 0 of 20 replies were word-for-word identical between the two `v2` runs, not 1 of 20.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run: Windows, Linux, and Python versions other than 3.14.6. Models other than `claude-haiku-5-5`. More than two runs of the same prompt. The `.env` file loader in `app.py` was not tested separately: the runs got the key from the environment.
