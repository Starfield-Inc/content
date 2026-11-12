---
title: Can you use AI coding tools in a hackathon?
summary: Allowed, allowed with disclosure, or banned: the three rule patterns for AI coding tools, and how to disclose what you used.
byline: Starfield Labs
cover: ai-coding-tools-hackathon-rules.png
cover_alt: "Cover card for the article \"Can you use AI coding tools in a hackathon?\""
published: 2026-10-19
---

It depends on the event. Each hackathon sets its own rules, and the only answer that counts is the one in the rules for the event you join. Read them before you write a line of code, ask the organizers if anything is unclear, and be open about what you used.

### How can you make sense of an event's rules on AI tools?

When you read a rulebook, it helps to sort what it says into one of three broad shapes. This is a simple way to think about it, not a list of every possibility.

| Rule shape | What it means | What you should do |
| --- | --- | --- |
| Allowed | You can use AI assistants, code completion and chat tools freely. | Use them, but still understand and own every part of your code. |
| Allowed with disclosure | You can use them, but you must say which tools you used and for what. | Keep notes as you build and add a disclosure section to your submission. |
| Restricted | AI-generated code is not allowed, or only for certain tasks. | Turn off completion in your editor and keep your work clearly your own. |

Some rules mix these. For example, an event might allow AI tools for boilerplate and debugging but ask that the core idea and logic come from the team. Another might treat an AI model as part of the product you are building, and have separate rules for AI that writes your code. Read both parts carefully.

### Where do you find the rules for a specific event?

Look in a few places before kickoff:

- The event page and its official rules or terms.
- The judging criteria, if they are published. Words like "originality" can hint at how generated code will be viewed.
- The FAQ or announcements channel, if the event has one.
- The organizers themselves. If the rules are silent or unclear, ask in writing and keep the answer.

If you cannot find anything, do not assume. A short question to the organizers before kickoff is better than a dispute at the end.

### Why might an event restrict AI coding tools?

You may never be told the reason, but a few are easy to imagine. An event might be built to test fundamentals, such as a student contest. It might want to compare teams on an even footing. Or the organizers might worry about code that nobody on the team understands, which is hard to judge and hard to maintain.

An AI-focused event might take the opposite view. If the point is to see what builders can ship with AI tools in a short time, using those tools well is part of the skill on show. Either way, the rules tell you which view applies.

### How do you disclose AI tool use in a submission?

When disclosure is required, or simply welcome, a short and specific note works best. A vague line like "we used AI" tells a reader very little. Add a section to your README or submission form. Here is a sample you can adapt:

**AI tools used**

- Tool type: an AI coding assistant in our editor, and a chat-based model.
- What it helped with: project scaffolding, writing tests, debugging an API error, drafting the README.
- What we wrote ourselves: the core matching logic, the prompt design, the UI layout.
- How we checked it: we reviewed and tested all generated code before merging.

A few habits make this easy:

- Keep a running log during the event. Note the task and the tool each time you lean on AI for something substantial.
- Commit often with clear messages, so your history shows how the project grew.
- If someone asks about AI help during your demo, be direct and specific.

Disclosure is not an admission of weakness. In our view, a team that can say exactly what it built, and how, makes a stronger impression than one that is vague.

### How do you use AI tools well during a hackathon?

Even when AI tools are allowed, it pays to use them with care. A good rule of thumb: let the assistant speed up the work, but keep the decisions with the team.

- Plan first. Write a short spec of what you are building before you prompt anything.
- Generate in small pieces. Ask for one function or component at a time, then read it.
- Test as you go. Run each piece with real inputs before you build on top of it.
- Remember that models can produce wrong answers. Check the output, especially anything that looks confident and detailed.
- Keep secrets out of prompts and code. Do not paste API keys into a chat, and do not commit them to your repository.
- Be cautious with code you cannot account for. If a suggestion looks like it was lifted from another project, rewrite it or leave it out.
- Make sure someone can explain every part. In a demo or Q&A, "the AI wrote that" is a weak answer.

### What if you break a rule by accident?

If you realize mid-event that you used a tool the rules restrict, tell the organizers as soon as you can. Explain what happened and what you changed. An early, honest correction gives them the chance to decide fairly, and it is far easier than explaining later why you stayed quiet.

### Where to go next

The best way to learn how events handle AI tools is to take part. Starfield Labs runs hackathons online and in cities, and builders can bring their own AI agent through its MCP connection. Find an upcoming event at [starfieldlabs.ai/events](https://starfieldlabs.ai/events), read its rules before kickoff, and plan your disclosure from the first hour. If you want to practice building with AI tools first, the guides at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials) are a good place to start.
