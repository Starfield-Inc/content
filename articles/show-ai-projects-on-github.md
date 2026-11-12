---
title: How to show AI projects on GitHub to employers: a README and demo checklist
summary: Judges and hiring managers skim a project page the same way. A checklist so yours answers their questions fast.
byline: Starfield Labs
cover: show-ai-projects-on-github.png
cover_alt: "Cover card for the article \"How to show AI projects on GitHub to employers: a README and demo checklist\""
published: 2026-11-03
---

To show AI projects on GitHub to employers, make each repository answer four questions in the first screen: what it does, whether it works, how the AI part works and what you did. Those are the same questions you would want answered when presenting a project at a hackathon, so one README can serve both. The checklists below cover the README, the demo and the repository itself.

### What should a reviewer be able to see?

Whoever reads your project page, whether a hackathon judge or a hiring manager, will be reading it with their own questions in mind. A useful exercise is to review your own project against a few broad areas. Here is a sample you can adapt.

| Area to review | What it can show a reader |
| --- | --- |
| Problem and usefulness | You can spot a real need and scope to it |
| Working demo | You ship things that run, not just ideas |
| Technical execution | You understand your stack and its trade-offs |
| Use of AI | You know what the model does well and where it fails |
| Presentation | You can explain technical work clearly |

Assume a reader will skim. Put the answers at the top, so they do not have to look for them.

### What goes in the README?

Use this order. Keep each item short.

1. Project name and one-line description. What it does and for whom, in plain words.
2. Demo link or video, right under the description.
3. Screenshot or GIF of the main flow.
4. The problem, in two or three sentences. Who has it and why it matters.
5. How it works, with a simple diagram or a short list: input, processing steps, model calls, output.
6. Tech stack, listed briefly.
7. How to run it: prerequisites, setup steps, environment variables (names only, never values) and one command to start.
8. Your role. On a team project, say exactly what you built.
9. Limitations and next steps. What does not work yet, and what you would do with more time.
10. Context. If it was built at a hackathon, name the event type and date, and the team.

The "limitations" section is not a weakness. To a technical reader, it shows you tested the project and know where it stops working.

### How do you show the demo?

Assume no one will run your code. Make the demo work without setup.

- Record a short video of the main flow. Two minutes or less is a good target. Show a real input and the real output. Narrate what is happening and why.
- Host a live version if you can, and say if it may be slow or offline. A broken link with no warning is worse than no link.
- Show one hard case. Include an input where the model could fail and show how your app handles it.
- Keep the pitch video separate. If you made a pitch for a hackathon, link it, but lead with the product demo.

Before you share, open the repository in a private browser window, as a stranger would, and follow every link. Then ask someone outside the project to watch the video once and tell you what the app does. If they cannot, shorten the video or improve the narration.

### How do you make the AI parts understandable?

AI projects often hide the most interesting decisions. Bring them to the surface. Add a short "AI approach" section that covers:

- Which kind of model you used and why, for example a hosted model API or a small local model, and the trade-off you accepted.
- How you prompt or configure it. Link the prompt files or show a trimmed example.
- How you check output. Models can produce wrong answers, so describe your validation, test inputs, small evaluation set or manual review.
- How you handle failures: timeouts, errors, off-topic or unsafe responses.
- What data it uses and where it comes from. If you are unsure whether you are allowed to use a dataset, check its terms or ask someone who can advise you.

If you used an AI coding assistant to write parts of the code, it is reasonable to say so briefly and explain how you reviewed the result. If the project came from an event, read that event's rules as well.

### How do you tidy the repository and your profile?

A clean repository signals care. Before you link a project in an application:

- Remove API keys, tokens and personal data. API keys should never be committed. If one ever was, treat it as exposed and replace it.
- Read the event's rules before you add a license or publish code you built with others, and ask your teammates.
- Delete dead code, unused files and test notebooks that do not run.
- Make commit messages readable for the main changes.
- Feature your best few repositories on your profile, with clear names and descriptions.
- Write a short profile introduction that says what you build and links to your top projects.

Quality beats quantity. A few complete, well-explained projects say more than many unfinished ones. When you apply, link the single project closest to the role, and mention it in one sentence in your cover note so the reviewer knows where to start.

### Where to go next

Take your most recent project and work through the README checklist this week. If you need a fresh project to show, a hackathon gives you a deadline, a team project and a reason to write a clear demo. Starfield Labs runs hackathons online and in cities; browse upcoming events at [starfieldlabs.ai/events](https://starfieldlabs.ai/events), and see the tutorials at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials) for builds you can extend.
