---
title: Can you use code written before a hackathon?
summary: Libraries and starter repos are usually fine. A project you built last month is not. Where the line sits and how judges check.
byline: Starfield Labs
cover: pre-written-code-hackathon.png
cover_alt: "Cover card for the article \"Can you use code written before a hackathon?\""
published: 2026-10-20
---

It depends on the event's rules, so read them first. A helpful way to think about it: a hackathon is a chance to show what your team builds during the event. Tools and building blocks made by others are one thing. A project you built last month is another. When in doubt, ask the organizers and keep your work easy to trace.

### How can you think about where the line sits?

The rules for your event are the final word. Until you have read them, a useful question to ask yourself is simple: what will this team build during the event? The table below is a sample way to sort what you might bring. It is a starting point for your own judgment, not a summary of how every event works.

| Lower risk | Declare it or ask first | Higher risk |
| --- | --- | --- |
| Open-source libraries and frameworks | Your own small utility code or helper functions | A project you built before the event |
| Public APIs, SDKs and hosted models | A design system, logo or brand assets made earlier | A starter repo that already contains the core feature |
| Starter templates the organizers provide | Research, sketches, wireframes or a written plan | Code copied from a past hackathon entry, yours or anyone else's |
| Datasets that are public or provided by the event | A model you trained or tuned before | Work presented as new when it is not |

The middle column is where most of the uncertainty sits. One event might welcome planning and design work done ahead of time. Another might want a clean start at kickoff. If the rules do not say, ask.

### Why would a hackathon limit prior work?

The simplest reason is fairness. A hackathon compares what teams can build in the same window of time. A team that arrives with weeks of work has an advantage that has nothing to do with the event. Organizers may also want to see new ideas that grow from the theme, not an existing product in a new wrapper.

That does not mean you have to start from zero. Using good tools and reusable building blocks is part of being a capable builder. In most cases, the concern is the core of the project, not the plumbing.

### How can you make your work easy to verify?

Assume that anyone reviewing your entry may want to see how it came together. You cannot control how they check, but you can make the story clear. Some signals a reviewer might look at:

- Your commit history: when the first commit was made, and how the project grew.
- When your repository was created.
- How well your team can explain a feature or answer follow-up questions.
- Whether a similar project already exists in public.

None of these proves anything on its own. Commit dates, for example, can be changed, so they are a signal at best. The point is not to game any of them. It is to build in a way that leaves an honest, readable trail.

### How do you keep your project clearly within the rules?

A few habits make your entry easy to trust:

- Create a new repository after the event starts.
- Commit early and often, with messages that describe what each change does.
- If you use a starter template, make the first commit the untouched template and say so in your README. That way anyone can see what you added.
- List every external library, API, dataset and model in your README.
- Declare anything you prepared in advance, such as designs or a plan, if the rules allow it.
- Keep your demo focused on what you built during the event.

A short "Built during the event" section in your README makes this explicit. Here is a sample you can adapt:

"Starter: the official template from the organizers (first commit). Everything after that was built during the event. Libraries and APIs used: listed below."

### Can you keep working on an existing idea?

An idea is not code. Arriving with a problem you care about and a rough plan is a sensible way to prepare. What usually matters is where the implementation starts, so check the rules and, if they do not cover it, ask.

Some events may invite you to extend existing work. If an event does, its rules will say so, and you should follow whatever it asks for, such as showing what existed before and what you added. If the rules do not mention it, plan for a fresh start.

### What should you do if you are unsure?

Ask the organizers before kickoff, in writing. Describe what you want to reuse and why, and keep their answer. If the reply is unclear, leave the code out or rebuild it during the event. Rebuilding a small helper costs you an hour. Losing a strong entry over a misunderstanding costs you the weekend.

A short checklist before you start:

- Have you read the event's rules on prior work?
- Have you listed everything you plan to reuse?
- Have you asked about anything in the middle column?
- Is your new repository ready to create at kickoff?

### Where to go next

Ready to build something new from the first commit? Starfield Labs runs hackathons online and in cities. Find an upcoming one at [starfieldlabs.ai/events](https://starfieldlabs.ai/events) and read its rules on prior work before you start. If you want to learn a framework or API before the event, the tutorials at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials) are a good place to start. Learning a tool ahead of time is not the same as building your project ahead of time.
