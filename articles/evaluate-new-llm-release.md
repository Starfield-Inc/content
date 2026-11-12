---
title: How to evaluate a new LLM release in one hour
summary: A one-hour private test your team can run when a new model ships, so you judge it on your own task, not a leaderboard.
byline: Starfield Labs
cover: evaluate-new-llm-release.png
cover_alt: "Cover card for the article \"How to evaluate a new LLM release in one hour\""
published: 2026-11-05
---

When a new model ships, judge it on your own task rather than on its leaderboard scores. Keep a small private test set of real examples, run the new model and your current one side by side, and compare the outputs blind. With some preparation done in advance, a small team can aim to do this in about an hour. The plan below is a sample you can adapt.

### Why not just trust leaderboards?

Public benchmarks can be useful signals, but they answer a different question from yours. They measure performance on fixed, general tasks. Your product has its own inputs, formats, edge cases and costs. A model can rank higher overall and still be worse at the one thing you need.

There are other reasons to be careful. A published score may come from settings you will not use, such as special prompts or several attempts per question, and you cannot always tell how it was produced. A leaderboard also says little about speed, cost, refusals or how well the model follows your output format. Your own test answers those questions directly, on inputs you know.

### What do we need before the release lands?

Most of the effort is work done once, ahead of time. Build a small evaluation kit:

1. **A private test set.** A reasonable starting point is somewhere between 20 and 50 real examples from your task. Include easy cases, hard cases and a few known failures. Keep it out of public repos and out of prompts you post online.
2. **What good looks like.** For each example, either an expected output or a short note on what a good answer contains.
3. **Your real settings.** The exact system prompt, settings and output format you use in production.
4. **A small script.** Something that sends each example to a given model and saves the outputs to a file, with time taken and usage figures if your provider reports them.
5. **A scoring sheet.** A spreadsheet with one row per example and a column for each model.

If you do not have this yet, building it is the best use of your first hour. The next release will then be much quicker to judge.

### How do we run the one-hour test?

Here is a sample timeline for a small team. Adjust it to fit.

| Time | Step | What you do |
| --- | --- | --- |
| 0 to 10 min | Read the release notes | Note anything that affects you: input limits, pricing, new features, known limits and API changes. Skim the model card. |
| 10 to 25 min | Run the set | Run your test set through the new model and your current model with the same prompt and settings. Save everything. |
| 25 to 45 min | Score blind | Shuffle the outputs so reviewers do not know which model wrote which. Score each against your criteria. |
| 45 to 55 min | Check the practical side | Compare speed, cost per task, format errors and refusals. |
| 55 to 60 min | Decide | Agree on one of three calls: switch, test further, or stay. Write down why. |

Two rules keep the test honest. First, change one thing at a time. If you rewrite the prompt for the new model, you are testing the prompt too. Run it once with your current prompt, then try a tuned prompt as a separate step if needed. Second, score blind. Knowing which model wrote an answer makes it hard to judge it fairly, so remove that information before you score.

### What should we score?

Keep the scoring simple enough that two reviewers would mostly agree. For each output, a pass or fail against your criteria is often enough. If you need more detail, use a three-point scale: wrong, acceptable, good.

Look at these dimensions:

1. **Correctness.** Is the answer right for your task?
2. **Format.** Does it follow the structure your code expects, such as valid JSON with the right fields?
3. **Instructions.** Does it respect constraints in the prompt, like length or tone?
4. **Refusals.** Does it refuse things it should answer, or answer things it should refuse?
5. **Speed and cost.** How long does each example take, and what does it cost to run?

Do not collapse everything into one score too early. A model that is slightly better on correctness but often breaks your output format may still be the wrong choice for you.

### How do we read the results?

Look at the failures, not just the totals. Read every example where the two models disagree. Patterns there tell you more than a single number. For example, you might find the new model handles long inputs better but trips on a rare edge case your users hit often.

Treat small differences with care. With a few dozen examples, a gap of one or two cases can be noise. If the result is close, a sensible call is "stay and test further", not "switch".

If you decide to switch, roll out gradually where you can. Run the new model in a staging environment or on a share of traffic first, and keep the old configuration ready to restore.

### How do we keep the test useful over time?

- Add a new example whenever you find a real failure in production.
- Retire examples that every model now passes easily.
- Keep a short log of each release you tested and the decision you made.
- Rerun the set when a model you already use gets updated, and use a fixed model version where your provider offers one.

Over time, the test set becomes a record of what your product needs. That makes each new release a quicker, calmer decision.

### Where to go next

A hackathon is a good place to practice this. Bring a small test set to an event at [starfieldlabs.ai/events](https://starfieldlabs.ai/events) and compare a few models on the problem you are building. For hands-on guides to working with models, see the tutorials at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials).
