---
title: What to do when an AI model is deprecated: keep your hackathon demo working
summary: A checklist to keep your hackathon demo working after the model it calls is retired.
byline: Starfield Labs
cover: ai-model-deprecated.png
cover_alt: "Cover card for the article \"What to do when an AI model is deprecated: keep your hackathon demo working\""
published: 2026-11-06
---

When a model your project calls is deprecated, act before the date it stops working. Find every place the model is used, pick a replacement, test your demo against it, and update both the code and your project notes. If you cannot migrate, replace the live demo with a recording so people can still see your work.

### What does deprecation mean for my project?

A deprecation notice tells you that a model is scheduled to stop being available. Until then, it may keep working as before. After that, calls to it may fail. Read your provider's notice to see the dates and what they suggest you move to.

Also check how you name the model in your code. If you call it through a general alias rather than a fixed version, find out whether that alias could start pointing to a different model. If it can, your demo could change behavior without any error at all.

For a hackathon project, the risk is quiet. The event ends, you move on, and months later your demo link shows an error page. Anyone who finds your project later sees something broken. A little upkeep prevents that.

### How do I find out in time?

You will not hear about it if you are not listening. Do these once, ideally right after you submit:

- Note the exact model identifiers your project uses, including any version suffixes.
- Subscribe to the provider's deprecation notices, changelog or email updates.
- Make sure the account email is one you still read.
- Add a calendar reminder to open your demo every month or two.
- If your host offers an uptime check, turn it on.

### What is the migration checklist?

When you get a notice, work through these steps in order.

1. **Read the notice.** Find the retirement date, the suggested replacement and any notes on behavior changes.
2. **Find every use.** Search your code and config for the model name. Check environment variables, deployment settings, notebooks and any no-code tools in the pipeline. Also check secondary uses, like an embedding model or a moderation step.
3. **Pick a replacement.** Start with the replacement your provider suggests, if there is one. If your project uses embeddings and you change the embedding model, plan to re-embed your stored data with the new model rather than mixing old and new.
4. **Pin a version.** Use a specific version identifier where your provider offers one, so behavior does not change again without notice.
5. **Test the real flow.** Run the exact path a visitor would follow. Check output format, length, speed and refusals, not just whether it returns something.
6. **Adjust prompts.** A new model may respond differently to the same prompt. Make the smallest changes that get the demo back to its original behavior.
7. **Check the live link.** Open it in a private window and run through it again.
8. **Record the change.** Note the change and the date in your README.

### What if I cannot migrate?

Sometimes there is no good replacement, the credits you used have run out, or you simply do not have time. You can still keep the project understandable.

| Option | When it fits | What to do |
| --- | --- | --- |
| Recorded demo | The app cannot run live any more | Record a short walkthrough while it still works, or build one from screenshots. Link it at the top of the README. |
| Cached responses | The demo uses fixed example inputs | Save real outputs and serve them in a clearly labeled demo mode. |
| Bring your own key | Others may want to run it | Document how to plug in a different provider or model, with a config example. |
| Archive notice | The project is finished | Add a clear note that the live demo is retired, with the date and a link to the recording. |

Be honest in the labeling. If the demo shows cached outputs, say so. People looking at your work should know what they are seeing.

### How do I make the next deprecation easier?

A few choices at build time save effort later. They are worth doing even in a weekend project:

- Keep the model name in one config value or environment variable, not scattered through the code.
- Wrap model calls in one small function or module, so switching provider touches one file.
- Keep a handful of test inputs and expected outputs in the repo, so you can check a new model quickly.
- Record a demo video at submission time, while everything works.
- Write down in the README which model and version you used, and when.
- Never commit API keys to the repo. Keep them in environment variables or your host's secret settings, so a key change does not mean a code change.

For example, a team that keeps its model name in one environment variable might switch models by changing a single setting, then rerun its saved test inputs to confirm the demo still behaves.

### Should I change my submission after the event?

Read the rules for the event you entered before editing anything. If you are not sure what you are allowed to change, ask the organisers. If you cannot change the official entry, put the update in your repository and on your own project page instead, and keep the original submission as a record of what you built at the time.

Whatever you change, keep a short history. A line such as "switched model on this date because the original was retired" helps anyone reading your project understand why it looks different from the original demo.

### Where to go next

If your project is worth keeping alive, it may be worth building on. Join another event at [starfieldlabs.ai/events](https://starfieldlabs.ai/events) to take it further with a newer model, and look through the tutorials at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials) for guides to current models and tools.
