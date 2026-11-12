---
title: "Build a Three-Role Agent Pipeline in Python with CrewAI"
seo_title: "Multi-Agent Pipeline in Python With CrewAI"
meta_description: "Build a three-role AI hackathon pipeline in Python with CrewAI and a small Claude model, with capped calls and telemetry turned off."
description: "Build a three-role AI hackathon pipeline in Python with CrewAI and a small Claude model, with capped calls and telemetry turned off."
---

# Build a researcher, writer and reviewer pipeline with CrewAI

You build a Python script in which three agents hand work to each other. A researcher lists facts, a writer turns them into a short note, and a reviewer checks the note against the facts. It uses the CrewAI library and the small `claude-haiku-5-5` model.

**Time:** about 30 minutes, plus a large install. **Level:** intermediate. **You need:** Python 3.10 to 3.13 (CrewAI does not support 3.14 at the time of writing), about 1 GB of free disk space, and an Anthropic API key. **Tested:** 12 November 2026 with Python 3.11.15, `crewai` 1.15.40 and `anthropic` 0.73.0 on macOS.

Model replies differ from run to run. The wording and the token counts you see will not match the output below. The shape of the output will.

A team that splits a task into roles can fit a demo into an AI hackathon weekend, and each role is easy to test on its own. If you are planning a project, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

One long prompt asking a model to research, write and check its own work mixes three jobs. Splitting them gives each step one narrow instruction, and the next step receives the earlier output as input. A reviewer that is a separate step can also say no. A framework such as CrewAI handles the hand-off, but it adds weight. This tutorial measures that weight: the install size, the number of requests and the tokens used.

## See it running first

This is the finished crew on a small topic: keeping an API key out of a public git repository. The three outputs come from three agents, and the last line is CrewAI's own count of requests and tokens.

{{shot:05-run|Terminal output of crew_run.py with researcher, writer and reviewer sections and a line of request and token counts}}

The rest builds it from nothing.

## Step 1: Check the licence, the size and the Python version

Before you install a framework, look at what you are taking on.

- **Licence.** The PyPI page for `crewai` has no licence field. The project's GitHub repository carries an MIT licence file. Read it yourself before you use the library in a product.
- **Python version.** The package declares support for Python 3.10 up to, but not including, 3.14. On Python 3.14, `pip` found no matching version when this tutorial was built. So the tutorial uses Python 3.11.
- **Size.** CrewAI pulls in a vector database client, a PDF reader and a telemetry stack, among others. Step 2 shows the real size.

## Step 2: Set up the project

Create a virtual environment with a supported Python version:

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment with Python 3.11}}

Put the requirement in `requirements.txt`. The `anthropic` extra matters. Without it, CrewAI raised an `ImportError` saying the native Anthropic provider was not available, when this tutorial was built.

{{file:requirements.txt}}

Install it. This takes several minutes:

{{cmd:02-install}}

{{shot:02-install|Terminal output of the install step: crewai 1.15.40, anthropic 0.73.0, 140 packages, a virtual environment of 872M}}

The virtual environment holds 140 packages and takes 872M on disk. That is a lot for three API calls, and it is the main cost of using a framework here. The download size was not measured separately.

Put your key in a file named `.env`, copied from the placeholder file:

{{file:.env.example}}

Never paste a real key into code, a screenshot or a chat. Load it into your terminal on macOS or Linux:

```bash
set -a; source .env; set +a
```

## Step 3: Switch telemetry off

CrewAI can send usage data to its maintainers. This tutorial turns that off before the library is imported. The script sets three environment variables: `CREWAI_DISABLE_TELEMETRY`, `CREWAI_DISABLE_TRACKING` and `OTEL_SDK_DISABLED`. A short script confirms the setting by asking the library itself:

{{file:telemetry_check.py}}

{{cmd:03-telemetry}}

{{shot:03-telemetry|Terminal output showing the three variables set to true and telemetry disabled: True}}

This checks the library's own switch. It does not prove that no network traffic leaves your machine, and this tutorial did not inspect traffic.

## Step 4: Write the crew

Each agent has a role, a goal, a short backstory and the same model. Delegation is off, and `max_iter` is 2, so an agent cannot start a long loop. `max_tokens` is 500 for each model reply. These are the hard caps on cost.

Each task names its agent. `context` passes earlier outputs to a later task: the writer sees the research, and the reviewer sees both the research and the draft. The process is sequential, so the tasks run in the order they are listed.

{{file:crew_run.py}}

The key check sits at the top, before the import of `crewai`. The reason: CrewAI loads a `.env` file when it is imported. When this tutorial first checked the key after the import, the script found a key in a parent folder's `.env` and made 9 real requests in a step that was meant to show a missing key.

First see what a missing key looks like. Run the script in a terminal where the variable is not set:

{{cmd:04-no-key}}

{{shot:04-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

## Step 5: Run it

With the key loaded:

{{cmd:05-run}}

{{out:05-run}}

The researcher produced four points, the writer joined them into one note, and the reviewer replied APPROVE with a reason. The final line reports 9 requests, 2706 input tokens and 1137 output tokens. Those figures come from CrewAI's usage counter.

There are three tasks, and the counter says 9 requests. This tutorial did not find out why. The counter may include more than one request per task, but that was not verified against the API's own logs. Treat the figure as an upper bound on cost and watch it when you change the crew.

The reviewer in this run approved the draft. Nothing here shows that the reviewer would catch a wrong claim, because the draft matched the research. To test that, change a task so the writer is asked to add a fact that is not in the research, then see whether the reviewer replies REVISE.

## Troubleshooting

- **`ImportError: Anthropic native provider not available`.** Install with the extra: `pip install "crewai[anthropic]"`. This happened here with a plain `crewai` install.
- **`pip` finds no matching version of `crewai`.** Check `python --version`. On Python 3.14 the install failed here. Use 3.10 to 3.13.
- **The missing-key check passes even though the key is not exported.** CrewAI reads `.env` files on import, from the current folder and its parents. Check the key before the import, as `crew_run.py` does.
- **The reviewer's reply stops in the middle of a word.** This happened in one run with `max_tokens` at 300. The reply was cut by the limit. Raising it to 500 fixed that in the runs that followed. The cause was not investigated further.
- **The install is slow.** It is 872M. A second install on the same machine may reuse `pip`'s cache.

## Frequently asked questions

**Does CrewAI work with a small Claude model?**

Yes, in this tutorial. With the model name `anthropic/claude-haiku-5-5` and the `anthropic` extra installed, the three-role crew ran and finished with no errors. The one failure seen was a reply cut by a 300-token limit, which a limit of 500 avoided.

**How do I switch CrewAI telemetry off?**

Set `CREWAI_DISABLE_TELEMETRY`, `CREWAI_DISABLE_TRACKING` and `OTEL_SDK_DISABLED` to `true` before you import the library. `telemetry_check.py` shows the library then reports telemetry as disabled. It does not inspect network traffic.

**How many API calls does a three-agent crew make?**

CrewAI reported 9 requests for 3 tasks in this run, 2706 input tokens and 1137 output tokens. The reason for 9 was not checked. Caps in the code (`max_iter`, `max_tokens`, no delegation) bound the cost of each agent.

## What to try next

- Give the writer an instruction to add one fact that is not in the research, and check that the reviewer says REVISE.
- Send a REVISE verdict back to the writer for one more draft, and cap it at one retry.
- Build the same three hand-offs with plain SDK calls and compare the request count and the install size.

## How this tutorial was tested

- Date: 12 November 2026. Python 3.11.15, `crewai` 1.15.40, `anthropic` 0.73.0, macOS. The model is `claude-haiku-5-5`.
- The code in this article is copied from the project files by a script. The output and screenshots come from saved logs of real API calls.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with a new virtual environment. The replay passed. The model's wording differed, and the replay reported 9 requests, 2883 input tokens and 1899 output tokens, where the numbers above come from the saved evidence run.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run: Windows, Linux, Python 3.10, 3.12 and 3.13, other models, a plain-SDK version of the crew (CrewAI worked, so the fallback was not needed), and a check of network traffic with telemetry off.
