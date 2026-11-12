---
title: Prompt engineering for beginners: improve one prompt, step by step
summary: Skip the list of tips. Take one real project prompt, improve it in five small steps and see how the output changes.
byline: Starfield Labs
cover: prompt-engineering-for-beginners.png
cover_alt: "Cover card for the article \"Prompt engineering for beginners: improve one prompt, step by step\""
published: 2026-10-30
---

Prompt engineering is writing instructions that get a language model to produce useful, consistent output. A practical way to learn it is to skip the long lists of tips. Take one prompt from a project and improve it one change at a time, while you watch how the output changes.

### What prompt are we improving?

Here is a hypothetical example. A weekend hackathon team is building a small tool for a support team. The tool reads an incoming customer support ticket and writes a short summary that a human agent can act on. The team calls a hosted model API from their backend and shows the result in a simple dashboard.

Their first prompt looks like this:

> Summarize this support ticket: {ticket\_text}

It returns text, so in one sense it works. But in this example the output varies. Some summaries are one line, others are three paragraphs. Some copy the customer's tone, some invent a solution. The dashboard layout breaks whenever the length changes. A short, vague prompt like this is a normal place to start, which makes it a good one to learn from.

### Step 1: Say who the output is for and why

The model does not know that a busy agent will read this in a queue. Tell it.

> You are helping a customer support agent triage tickets. The agent reads many tickets an hour and needs to understand each one in a few seconds. Summarize the ticket below for that agent.
>
> Ticket: {ticket\_text}

What to look for: shorter, more neutral summaries that focus on the problem rather than pleasantries. If the length is still inconsistent, that is expected at this stage. The next step deals with it.

### Step 2: Define the output format exactly

Your code needs a predictable shape. Ask for one.

> Return the summary in this exact format:
>
> Issue: one sentence describing the problem Product area: billing, account, shipping or other Urgency: low, medium or high Next step: one sentence on what the agent should check first

What to look for: responses with the same four lines, so the dashboard can display them. Watch for an extra sentence before the format, or a product area that is not on the list. Models can still return something unexpected, so if your app parses the response, consider asking for JSON and validating it in code before you display it.

### Step 3: Show one good example

Describing a format is a start. Showing one is worth trying next. Add a short example ticket and the summary you want for it.

> Example ticket: "I was charged twice for my subscription this month and I need one charge refunded before my card limit is hit."
>
> Example summary: Issue: Customer was charged twice for one subscription period. Product area: billing Urgency: high Next step: Check the payment history for a duplicate charge this month.

What to look for: "Next step" lines that read as concrete actions, not generic advice like "help the customer." Keep examples short and realistic. If every example is about billing, check whether the summaries start leaning toward billing, and vary your examples as you add more.

### Step 4: Add rules for the hard cases

Run the prompt on ten or twenty realistic tickets. Note where it goes wrong, then write a rule for each failure. Rules like these are a sensible starting point for this example:

- If the ticket does not say what the problem is, write "Issue: unclear" and set Next step to "Ask the customer for details."
- Do not promise refunds, fixes or timelines.
- Use only information in the ticket. Do not guess order numbers or account details.
- If a ticket covers more than one problem, summarize the most urgent one and note that there are others.

What to look for: vague or angry tickets that no longer produce confident, invented summaries. Assume that anyone trying your demo will go straight for the odd cases, so test them before they do.

### Step 5: Test, compare and keep a log

A prompt change can fix one case and break another. Keep a small test set of the same tickets and run it after every change. A simple table is enough. Here is a sample log for this example that you can adapt:

| Version | What changed | What got better | What got worse |
| --- | --- | --- | --- |
| v1 | Plain request | Returns text | Length and content vary |
| v2 | Added audience | Shorter, more focused | Length still unpredictable |
| v3 | Fixed format | Mostly parseable | Occasional off-list categories |
| v4 | One example | Concrete next steps | Slight lean toward the example's topic |
| v5 | Edge-case rules | Fewer invented details | "Unclear" used a bit too often |

Read the outputs yourself. Do not judge a prompt by one good response.

### The final prompt

Put together, the prompt has five parts: audience and purpose, the input, the output format, an example and the rules. That structure is a useful template for many project prompts, whether you are summarizing, classifying, extracting data or drafting text.

A few habits help beyond this example:

- Change one thing at a time, so you know what caused the difference.
- Write instructions as plain, direct sentences.
- Keep the variable input clearly separated, for example in a labeled section.
- Validate the output in code when your app depends on its shape.
- Save each version of the prompt alongside your project code.

### Where to go next

Good practice comes from a project with a real deadline and real people trying it, because they will find the cases your prompt misses. Pick an upcoming hackathon at [starfieldlabs.ai/events](https://starfieldlabs.ai/events) and use this five-step method on your team's main prompt. For hands-on learning material, browse the tutorials at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials).
