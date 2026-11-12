---
title: AI hackathon project ideas you can demo in a weekend
summary: Project ideas sized for 24 and 48 hours, each with the one thing to cut so your demo still works on Sunday.
byline: Starfield Labs
cover: ai-hackathon-project-ideas.png
cover_alt: "Cover card for the article \"AI hackathon project ideas you can demo in a weekend\""
published: 2026-10-13
---

A good AI hackathon project is one small loop you can show working on real input before the deadline. Pick an idea where a model does one clear job, wrap it in the thinnest interface that proves it, and decide on day one what you will drop. The ideas below are examples sorted by how much time they might need, and each comes with a suggested scope cut.

### How do you size an idea for the time you have?

Before you choose, run the idea through three questions:

1. Can you say it in one sentence? "It reads a lease and lists the risky clauses" works. "An AI platform for renters" does not.
2. Can you get real input in the first hour? If you need data you do not have, you may spend the weekend on data instead of the product.
3. Is there one moment in the demo where the model clearly does the work? Build the demo around that moment. Everything else supports it.

A good rule of thumb: for a 24-hour event, plan one input, one model step and one output. For a 48-hour event, allow yourself one extra step, such as a second model call, a tool the model can use, or a simple memory of past results.

### Which ideas fit a 24-hour hackathon?

These examples need one model call or a short chain, and a single screen.

| Idea | What the model does | Scope cut |
| --- | --- | --- |
| Document explainer | Turns a dense document (a lease, a policy, a paper) into plain-language answers to a fixed set of questions | Support one document type only |
| Meeting-notes cleaner | Turns a raw transcript into decisions, owners and dates | Skip live audio; paste or upload text |
| Accessibility checker | Describes an image or screenshot and flags missing alt text or low contrast | One page at a time, no crawling |
| Support reply drafter | Drafts a reply to a customer message using a short help document | No ticketing integration; copy and paste |
| Study-card maker | Turns lecture notes into question-and-answer cards | Text only; skip file parsing |
| Recipe adapter | Rewrites a recipe for a diet, a serving size or what is in the fridge | No nutrition database |

Aim to demo any of these in under two minutes, with a real example you bring with you.

### Which ideas fit a 48-hour hackathon?

With two days, you can try adding a second step: search over your own data, a tool the model calls, or an agent that takes a few actions in sequence.

| Idea | What the model does | Scope cut |
| --- | --- | --- |
| Codebase Q&A helper | Answers questions about one repository by searching its files | One small repo; no live sync |
| Research assistant | Searches a fixed set of sources, then writes a cited summary | Download the sources first; no open web |
| Form-filling agent | Reads a document and fills a structured form, asking the user only when unsure | One form; no account login |
| Expense sorter | Reads receipts from photos and sorts them into categories with totals | Fixed category list; no bank connection |
| Voice journal | Transcribes a short voice note and tags mood and themes over time | Store a week of entries locally |
| Bug triage bot | Reads new issue reports, labels them and suggests a likely owner | Read-only; no posting back to the tracker |

The scope cut is not a weakness. It is what lets you finish. In our view, a narrow tool that works is a better demo than a wide one that breaks on stage.

If you already work with an AI agent, you can bring it along: Starfield Labs has an MCP connection for agents.

### How do you pick between ideas as a team?

Here is a simple scoring method you can adapt. Score each shortlisted idea from one to three on four things, then add the scores:

- Problem: Does someone you can name actually have this problem?
- Demo moment: Is there a clear point where the model visibly does the work?
- Data: Do you already have, or can you quickly make, realistic input?
- Skills: Can the team build the core in the first half of the event?

Take the highest score. If two ideas tie, pick the one with the stronger demo moment. Then write the scope cut on a shared note so nobody quietly adds it back at 2 a.m.

Before you lock in, read the event's theme and rules in full. An idea that ignores the brief is a risky choice, even if it works well.

### What should you cut first when time runs short?

When you fall behind, a sensible order to cut is:

1. Accounts and login. Use a single demo user.
2. Settings and options. Hard-code sensible defaults.
3. Edge cases. Handle the inputs you will show, and say what you would handle next.
4. Visual polish. A clean, plain page is fine.
5. The second feature. Protect the one loop that makes the demo.

Do not cut the real input. Running the model on a real example is the part of the demo that proves the idea, so keep it even if everything around it is plain.

A few more habits help on the day. Keep the best version of your demo working at all times, and only add to it on a separate copy. Save two or three real inputs that you know work well. Write down the one sentence you will use to open the demo, and practise it once before the deadline.

### Where to go next

Pick two ideas from the tables, run them through the scoring step with your team, and write down your scope cut before you write any code. Then find a hackathon, online or in a city near you, at [starfieldlabs.ai/events](https://starfieldlabs.ai/events) and build it. If you want a head start on the technical side, such as calling a model API or adding search over your own data, the guides at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials) walk through the basics.
