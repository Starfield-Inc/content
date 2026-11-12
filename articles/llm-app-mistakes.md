---
title: Common mistakes when building LLM apps, and how to fix them
summary: The mistakes that sink short LLM builds, from no eval to an untested demo path, each with a fix and a rough time cost.
byline: Starfield Labs
cover: llm-app-mistakes.png
cover_alt: "Cover card for the article \"Common mistakes when building LLM apps, and how to fix them\""
published: 2026-11-11
---

Four mistakes are worth watching for when you build an LLM app: skipping evaluation, scoping an agent too broadly, leaking API keys, and never testing the exact demo path. Each one is cheap to fix early and expensive to fix late. For most of them, budget somewhere between ten minutes and an hour.

Use this list as a checklist at the start of a short build, such as a hackathon, and again before you submit.

### Which mistakes cost the most?

Here is the short version. The time budgets are suggestions for a small team that already has a working prototype. Adjust them to your project.

| Mistake | Fix | Suggested time budget |
| --- | --- | --- |
| No eval | Hand-check a few dozen outputs, add one code check | About 1 hour |
| Over-scoped agent | Cut to one task and a few tools | 30 to 60 minutes |
| Keys in the repo | Move to environment variables, replace the key | 15 to 30 minutes |
| Untested demo path | One entrypoint script, run it every few hours | 30 minutes, then a few minutes per run |
| Prompt changes without checks | Rerun the eval after each change | A few minutes per change |
| No plan for bad output | Add limits, fallbacks and an "I don't know" path | 30 to 60 minutes |

The sections below explain each one.

### Why is skipping evaluation a mistake?

Models can produce wrong answers, and the same input can give a different output on a different run. An app that worked in three tries can fail on the fourth, and you will not see it unless you look at many outputs.

Fix: Pick the one task your demo depends on. Collect a set of real inputs (20 to 50 is a good rule of thumb), run the app on all of them, and mark each output pass or fail against a short written rule. Add one check in code, such as "output is valid JSON" or "every number appears in the source." Rerun it whenever you change the prompt or model. You will also have a clear answer when someone asks how you know the app works. If time is short, a small set checked carefully beats a large set nobody reads.

### What does an over-scoped agent look like?

For example, a team might plan an agent that plans, browses, writes code, sends email and books meetings. Each extra tool adds new ways to fail, and more choices give the agent more chances to pick the wrong one.

Fix: Write the one task the agent must complete in a single sentence. Give it only the tools that task needs, often two or three. Set a step limit and a time limit so a bad run ends instead of looping. If a step can be plain code instead of a model decision, make it plain code. You can add tools later, once the core task works reliably.

### How do API keys end up in the repo, and what do you do?

It tends to happen in a rush: a key pasted into a config file, a notebook or a test script, then committed. API keys should not be committed. Treat any key that reaches a shared or public repo as exposed, because someone else could use it on your account.

Fix:

- Move every key into environment variables, loaded from a local .env file.
- Add .env to .gitignore before your first commit.
- Commit a .env.example with the variable names and no values.
- If a key was ever committed, revoke it and create a new one. Deleting the file is not enough, because it stays in the git history.

Do this in the first hour. It takes minutes then and much longer after a leak.

### Why test the exact demo path?

It is easy to test parts of the app separately and run the full flow for the first time on stage. That is when a missing setup step, an expired key, a usage limit or a slow network can show up.

Fix: Write a single script that sets up the demo state and runs the full demo task. Run it from the first day and every few hours after. Check real results, such as the file written or the record created, not just the app's success message. Run it on a fresh clone at least once, so you catch files and settings that only exist on one laptop. In the final hours, freeze features. If the event's rules allow it, keep a recording of a good run as a backup.

### What other mistakes are worth catching?

- **Changing prompts without rerunning checks.** A fix for one case can break others. Rerun your eval after every prompt or model change.
- **No plan for bad output.** Decide what the app does when the model is unsure, returns broken output or times out. A clear "I don't know" or a retry is better than a confident wrong answer.
- **Sending personal data without thinking.** Use sample or public data in a short build, and read the rules of your data source and the event. If you are unsure what is allowed, ask before you use it.
- **Building the interface first.** A polished screen with no working core cannot be demoed. Get the rough path working end to end, then add the interface.
- **Relying on one long prompt.** When a single prompt tries to do retrieval, reasoning and formatting at once, failures are hard to trace. Split it into steps you can check one at a time.
- **Leaving the README for last.** People may read it after the demo. Write what the app does, how to run it and what it cannot do yet while you still remember.

### Where to go next

The quickest way to build these habits is to practice them under a real deadline. Find a hackathon at [starfieldlabs.ai/events](https://starfieldlabs.ai/events) and use this list as your start and finish checklist. For step-by-step guides to evals, agents and LLM app setup, see the tutorials at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials).
