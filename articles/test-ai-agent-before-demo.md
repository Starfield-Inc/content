---
title: How to test an AI agent before a demo
summary: Test the demo task from hour one, verify real outputs, and keep one script that runs it all.
byline: Starfield Labs
cover: test-ai-agent-before-demo.png
cover_alt: "Cover card for the article \"How to test an AI agent before a demo\""
published: 2026-11-09
---

To test an AI agent before a demo, run the exact task you plan to show, end to end, from early in the build. Check what the agent actually produced, not what it says it did. And keep one script that starts the whole demo, so the version you test is the version you present.

An agent has more moving parts than a single model call. It can pick the wrong tool, loop, time out, or report success on a step that never happened. The checklist below is a sample you can adapt for a short build with a fixed demo slot.

### Where can an agent demo go wrong?

A useful way to think about it: the risk sits in the gap between what the team tested and what they run live. Watch for these situations:

- The demo task was only tried once, late on the last day.
- The agent's final message said "Done", and nobody checked the file, database or API it was meant to change.
- Setup steps lived in one person's terminal history.
- A rate limit, an expired key or a slow network appeared only under demo conditions.
- A last-minute prompt change fixed one case and broke the main one.

Each item on the checklist below is meant to close one of these gaps.

### Step 1: Write the demo task on day one

Before you write much code, write the demo script in plain words. One user, one goal, a few steps. For example: "A user pastes a meeting transcript. The agent creates three tasks in the tracker and drafts a follow-up email."

Then make that task your first test. Run it end to end, even when most of it is stubbed. Run it again every hour or so. That way you see breakage soon after it happens, not the night before you present.

If the full task is too slow to run that often, keep a short version that touches every tool once, and run the full one a few times a day.

### Step 2: Check outputs, not claims

An agent's summary of its own work is not evidence. It can say a file was saved when the write failed, or say a test passed when it never ran.

For each step in the demo task, decide what you can inspect directly:

| Agent says | Check instead |
| --- | --- |
| "Created three tasks" | Query the tracker and count them |
| "Saved the report" | Open the file and read it |
| "Sent the email" | Look in the sent folder or the service's log |
| "Tests pass" | Run the tests yourself and read the output |

Where you can, turn these into small assertions in code that run after each demo attempt. A short script that prints PASS or FAIL per step is enough.

Keep these checks after the demo works. They are a quick way to see whether a late prompt change broke something.

### Step 3: Keep one entrypoint

The demo should start with one command, such as ./run\_demo.sh or make demo. That script should:

- Load settings and keys from environment variables, not from the code.
- Reset the demo state (clear test data, load known inputs).
- Start any services the agent needs.
- Run the demo task.
- Run the output checks from Step 2 and print the results.

Everyone on the team uses this script, every time. If you change how the demo starts, change the script, not your terminal habits. It also makes it easier for anyone else to run your project later.

### Step 4: Break it on purpose

Once the main path works, try a few things that can happen in real use:

- **Slow or failed tool calls.** Does the agent retry, give up cleanly, or hang?
- **Unclear input.** Does it ask a question or guess?
- **A long input.** Does it run into a size or time limit?
- **Repeated runs.** Run the demo task five times in a row. A model can give different results on different runs, so one success is not a pattern.

Set a step limit and a time limit on the agent loop, so a bad run ends instead of spinning on stage.

Write down what you saw on each failed run. If the same failure shows up twice, fix it or remove that step from the demo. A shorter demo that works every time is better than a longer one that works some of the time.

### Step 5: Prepare for the live slot

In the last few hours, freeze features and protect the demo path. Here is a sample final checklist:

- Demo task passes on several clean runs in a row
- Output checks pass, not just the agent's final message
- One entrypoint script works on a fresh clone
- Keys are in environment variables and not in the repo
- Usage limits and credits checked for the demo window
- Logs visible, so you can explain a failure if one happens
- A recording of a successful run, in case the network fails
- No prompt or model changes after the final test run

Read the event's rules on demo format before you plan around a recording or a live run. If live logs fit the format, consider showing them, or the check output, during the demo. The audience then sees the agent working instead of taking your word for it.

### Where to go next

A good way to get better at this is to ship an agent under a real deadline. Find a hackathon at [starfieldlabs.ai/events](https://starfieldlabs.ai/events). If you already work with an AI agent, you can bring it: Starfield Labs has an MCP connection for agents. For step-by-step agent builds, see the tutorials at [starfieldlabs.ai/tutorials](https://starfieldlabs.ai/tutorials).
