---
title: "Write an AI Hackathon README That Judges Read"
seo_title: "Write an AI Hackathon README That Judges Read"
meta_description: "An AI hackathon README template: what judges look for in the opening 30 seconds, from the problem line to a demo link and a three-line run guide."
---

# Write a hackathon README that judges will read

You will write a README for a hackathon project, check it with a small Python script, and see it rendered the way a browser shows it. It takes about 30 minutes, needs no API key, and starts from a template you can copy.

**Level:** Beginner. **You need:** Python 3.10 or newer and a terminal. **Tested:** 11 November 2026 on macOS with Python 3.14 and `Markdown` 3.11.3. Windows commands were not run.

In an AI hackathon, the README is often the page a judge reads before they open your demo. Judges have many projects to go through, so this tutorial treats the opening 30 seconds as the time you have. That figure is our working assumption, not a measured number. If you are still choosing an event, see the [upcoming AI hackathons](/ai-hackathons/).

## Why the README matters

A judge sees the project through the README before they see it run. If the page does not say what the project is, where to try it and how to start it, they have to hunt. This tutorial uses a seven-point checklist we wrote ourselves. It is not any event's official rubric. Check your event's rules and judging criteria, and follow those first.

The seven points:

1. One short sentence at the top that says what the project does and for whom.
2. A demo link near the top.
3. A screenshot.
4. A run guide of three lines or fewer.
5. A list of what it is built with.
6. The team.
7. What you would build next.

## See it running first

This is the finished README for a small example project called Notetrim, rendered as a web page. It passes all seven checks. The rest of this tutorial builds it from scratch.

{{shot:07-page|A rendered README with a one-sentence opening, demo links, a screenshot, a run guide, tech list, team and next steps}}

## Step 1. Create a virtual environment

The checker uses only Python's standard library. The page renderer needs one package, so use a virtual environment to keep it apart from the rest of your machine.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Activate it. On macOS and Linux use `source .venv/bin/activate`. Every command below assumes it is active.

## Step 2. Install the Markdown package

`Markdown` turns a README into a web page, so you can look at it the way a judge's browser does.

{{file:requirements.txt}}

{{cmd:02-install}}

{{shot:02-install|Terminal after installing the Markdown package, showing the name and version}}

## Step 3. See what a weak README looks like

Most weak READMEs share one trait: they talk about the team's effort, not the reader's need. Here is one. It is written as a typical example, not copied from a real project.

{{file:weak/README.md}}

The checker reads a README and tests the seven points.

{{file:check_readme.py}}

Run it on the weak README:

{{cmd:03-weak}}

{{shot:03-weak|The checker failing all seven points for the weak README}}

All seven checks fail. The title line "Hackathon project 2026" is 3 words, so even the opening fails: the checker wants between 6 and 25. The command exits with code 1, so a script can use it as a gate.

## Step 4. Give the project something to show

The example project is a small script that pulls action items out of meeting notes. It uses plain matching rules, with no model and no network, so you can run it anywhere. Save this as `app.py` inside an `example/` folder:

{{file:example/app.py}}

And this as `example/notes.txt`:

{{file:example/notes.txt}}

Run it from inside `example/`:

{{cmd:04-app}}

{{shot:04-app|The example app listing four action items from the notes file}}

The notes file has seven lines and the script found 4 action items. A judge needs to see something like this output in your README, so a screenshot of the project working is worth more than a paragraph about it. The image above was saved as `example/screenshot.png` and is the one the README uses.

## Step 5. Write the README from the template

Start from this template. Each section answers one question a judge has.

{{file:template/README.template.md}}

Here is the filled-in version for Notetrim. The opening sentence names the problem and the result. The demo links sit right under it. The run guide is two lines. The links use `example.com` because this is a made-up project.

{{file:example/README.md}}

Check it:

{{cmd:05-good}}

{{shot:05-good|The checker passing all seven points for the Notetrim README}}

The opening is 20 words and all 7 checks pass. A passing check does not make the README good. It only means the parts a reader looks for are there. Read the text aloud and ask whether a stranger would understand the project.

## Step 6. Look at it the way a browser does

A README that reads well as text can still look cluttered as a page. This script renders it to HTML:

{{file:render_readme.py}}

{{cmd:06-render}}

{{shot:06-render|Terminal after rendering the README to a web page}}

The screenshot at the top of this tutorial shows the result. The sentence, the links and the screenshot all sit above the problem section, so someone who stops reading there has still learned what the project is.

## Step 7. Check what a wrong path looks like

Run the checker on a file that does not exist:

{{cmd:08-missing}}

{{shot:08-missing|The checker reporting that the file cannot be found}}

You get a one-line message and exit code 2, which is different from the code 1 a failed check gives.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'markdown'`.** The virtual environment is not active, or the install did not finish. Activate it and run `pip install -r requirements.txt` again.
- **The checker says "no link with demo in its text".** The demo link must be a full `https://` link whose visible text contains the word "demo", and it must sit in the first 12 lines.
- **The screenshot check fails.** The image path is relative to the README. The file has to exist next to it.
- **The rendered page shows no image.** Run the render command from the project folder, because it copies images from next to the README into `site/`.

## Frequently asked questions

**What should an AI hackathon README include?**

One sentence on what the project does and for whom, a demo link, a screenshot, a run guide of three lines or fewer, what it is built with, the team and what comes next. In the test, the Notetrim README had all seven and passed 7 of 7 checks, while the weak one passed none.

**How long should a hackathon README be?**

Short enough that the key facts sit at the top. The Notetrim README keeps its opening sentence to 20 words and its run guide to 2 lines. Our checklist sets limits of 25 words and 3 lines. These are our own limits, not an event rule.

**Do judges read the code in an AI hackathon?**

It depends on the event, and this tutorial did not test it. Read your event's judging criteria. What you can control is making the README work for a reader who never opens the code.

## What to try next

- Run the checker on your own project's README and fix each failure.
- Add a check of your own, such as a link to a licence file.
- Replace the screenshot with a short demo video link.

## How this tutorial was tested

Every command and screenshot above comes from one real run on 11 November 2026. The code in the blocks is copied from the project files, not retyped. The steps were then run again from an empty folder, and all of them passed. Terminal screenshots are rendered from the saved output of the commands, in a terminal-style frame. They are not captures of a window. The rendered README page is a real Chrome screenshot of the running page. The checklist is our own and was not compared against any event's official rubric. Not run: Windows and Linux, other Python versions, and any real hackathon submission.
