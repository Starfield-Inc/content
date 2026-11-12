---
title: How to evaluate LLM outputs in one hour
summary: Hand-check 20 to 50 outputs, add one code check, and show judges real evidence that your app works.
byline: Starfield Labs
cover: evaluate-llm-outputs.png
cover_alt: "Cover card for the article \"How to evaluate LLM outputs in one hour\""
published: 2026-11-08
---

To evaluate LLM outputs, collect a small set of real inputs, run your app on them, and check each output against a short written rule. For a hackathon team, a few dozen hand-checked examples plus one automated check in code is a good place to start. Budget about an hour for it. What you get back is evidence, which is easy to leave out of a demo.

You do not need a framework, a leaderboard or a large dataset. You need a spreadsheet, a clear idea of what "good" means for your app, and the discipline to look at real outputs.

### Why bother with an eval in a short build?

Models can produce wrong answers, and the same input can give different results on different runs. An app can look fine in three tries and fail on the fourth. A live demo shows one path. An eval shows you how often that path works.

A small eval also helps you while you build:

- You notice failure patterns early, while there is still time to fix the prompt or the data.
- You can tell whether a change made things better or worse, instead of guessing.
- You have a clear answer when someone asks "How do you know it works?"

### What should you test?

Start with the one task your demo depends on. If your app summarizes support tickets, test summaries. If it extracts fields from invoices, test extraction. Do not try to cover every feature.

Then write down what a good output looks like. Keep it to two or three rules a teammate could apply without asking you. Here are sample rules you can adapt:

| Task | Rule for a pass |
| --- | --- |
| Summarize a ticket | Mentions the customer's main problem; no facts that are not in the ticket |
| Extract invoice fields | Total, date and vendor match the source document |
| Answer from docs | Answer is supported by a retrieved passage; says "I don't know" when nothing fits |

If you cannot write the rule, the task is not defined well enough yet. Fix that first.

### How do you build the test set?

A good rule of thumb is 20 to 50 inputs. With too few, one odd case can swing your view. With too many, you will not finish checking by hand in the time you have. Pick a number your team can actually read.

- **Collect real inputs.** Use the dataset you are building on. Pick a spread: easy cases, long ones, messy ones and a few that should be refused or answered with "I don't know".
- **Add a handful of edge cases on purpose.** Empty input, very long input, input in another language, input that tries to change the model's instructions.
- **Put them in a sheet.** One row per input. Columns: input, output, pass or fail, note.
- **Freeze the set.** Do not swap inputs after you see the results. Otherwise the eval quietly turns into a demo.

If you must write some inputs yourself, mark them as synthetic in the sheet so you can say so honestly.

### How do you check outputs by hand?

Run your app on every input and paste the outputs into the sheet. Then read each one against your rules.

- Mark each row pass or fail. A 1 to 10 score is slower, and teammates tend to disagree on it.
- Write a short note on every fail: "made up a date", "ignored second question", "too long".
- If two teammates are free, have each check half, then swap ten rows to see whether you agree. Where you disagree, tighten the rule.
- Group the fail notes. Look for the two or three patterns that explain the most failures. Those are your next fixes.

In our view, this step is where most of the value is. Reading real outputs shows you problems a single number can hide.

### What is the one code check?

Add one automated check that runs on every output. Pick something you can test with plain code, not with another model. Some options to consider:

- **Format:** the output parses as valid JSON with the required fields.
- **Grounding:** every quoted number or name appears in the source text.
- **Length:** the output stays under a limit you set.
- **Refusal:** the app says "I don't know" on inputs marked as unanswerable.

Write it as a short script that reads your sheet or a JSON file and prints a pass rate. Run it after every prompt or model change. It is a cheap way to catch a change that made things worse before you find out on stage.

You can add a second check that uses a model as a grader later. If you do, hand-check a sample of its grades first. A grader is also a model, and it can be wrong too.

### How do you show this to others?

If your event has a presentation or a written submission, keep the eval to one slide or one section of your README:

- What you tested (the task and how many inputs).
- Your rule for a pass, in one line.
- The result. For example, a team might write "41 of 50 passed" next to the code check pass rate.
- The main failure pattern and what you changed because of it.

Show a before and after if you have one. Be honest about what still fails. We think a clear limit, stated plainly, is worth more than a perfect demo with nothing behind it.

### Where to go next

The best way to practice is on a real deadline. Pick a hackathon at [starfieldlabs.ai/events](https://starfieldlabs.ai/events), build one feature, and add a small eval before you record your demo. For hands-on guides to building and testing LLM apps, browse the tutorials at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials).
