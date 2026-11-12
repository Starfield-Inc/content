---
title: "Remove Duplicate Stories: AI Hackathon Project Tutorial"
description: "AI hackathon project: remove duplicate stories from many news feeds. Group similar headlines, test the rule and show a web page."
---

# Remove duplicate stories from many news feeds

You will build a small Python tool that reads several public news feeds, finds headlines about the same story, and shows the result on a local web page. It takes about 45 minutes and needs no API key.

**Level:** Intermediate. **You need:** Python 3.10 or newer, a terminal, an internet connection and a browser. **Tested:** 10 November 2026 on macOS with Python 3.14 and `feedparser` 6.0.14. The Windows activate command was not run.

A feed reader that shows each story once is a small project you can finish in an AI hackathon, with a demo anyone understands. See the [upcoming AI hackathons](/ai-hackathons/) for a place to build it.

## Why remove repeats

When five outlets cover the same model release, a feed reader shows you five items. You want one, with the other four as extra reading. Doing this by headline needs no AI model. It needs a clear rule for "same story", and a way to check that the rule works.

## See it running first

By the end the tool shows a page like this:

{{shot:06-page|A web page listing two stories that appear in two feeds, then the other headlines}}

The headlines in the screenshot are from the feeds on 10 November 2026. Yours will be different, because feeds change every day. The rest of this tutorial builds the tool from scratch.

## Step 1. Create a project folder and a virtual environment

Make a folder, open a terminal in it, and run:

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Activate it with `source .venv/bin/activate` on macOS and Linux. Every command below assumes it is active.

## Step 2. Install feedparser

`feedparser` reads RSS and Atom feeds, the public lists of recent posts that most news sites publish. It is the only package this project needs.

{{file:requirements.txt}}

{{cmd:02-install}}

{{shot:02-install|Terminal after installing feedparser, showing its name and version}}

## Step 3. Read the feeds

Put one feed address per line in `feeds.txt`. These are public feeds that publishers offer for exactly this use:

{{file:feeds.txt}}

The script below reads each feed, keeps the 25 newest items from it, and saves only the source name, title, link and date. It does not download the articles themselves. If a feed cannot be read, it prints a `skipped` line and carries on, so one broken feed does not stop the run.

{{file:fetch_feeds.py}}

{{cmd:03-fetch}}

{{shot:03-fetch|Four feeds read, 80 items saved, and one feed skipped}}

Four feeds worked and gave 80 items. The MarkTechPost feed could not be read, so the script skipped it. We do not know why, and we did not try to get around it. The tool is built to cope with a feed it cannot read. Leave the line in `feeds.txt` to see the skip, or remove it.

## Step 4. Group headlines about the same story

Two headlines about one story rarely share many words. "Meta launches Muse Ember, a small AI model built for the repetitive work agents actually do" and "Meta introduces Muse Ember to power cost-efficient AI agents" share only a few. The rule here is simple:

1. Lower-case each headline and keep its words, without small words such as "the" and "of".
2. Score two headlines by the share of their words they have in common.
3. Group headlines from different feeds when the score is 0.25 or higher.

One more rule matters. If both headlines contain version numbers and none match, they are never grouped. In our first run, a headline about version 5.1 scored the same 0.25 against a headline about 5.2. That is two different releases, not one story.

{{file:dedupe.py}}

The threshold is 0.25 because we tried 0.5 first and it found nothing: every pair of real headlines scored below 0.3. Pick the number by looking at real pairs, not by guessing.

Run it:

{{cmd:04-group}}

{{shot:04-group|The tool reports 80 items became 78 stories, and lists the two repeated stories}}

On this run 80 items became 78 stories, and two stories appeared in two feeds each. Both groups are correct. One is Anthropic's Fable 5.2 and Mythos 5.2 release. The other is Meta's Muse Ember.

## Step 5. Test the rule on fixed headlines

Live feeds change, so they make a poor test. A test with fixed headlines gives the same answer every time. These three checks cover the cases that matter: a repeated story is grouped, two different versions stay apart, and an unrelated item stays alone.

{{file:tests/test_dedupe.py}}

{{cmd:05-test}}

{{shot:05-test|Three tests passing}}

Run these tests every time you change the threshold or the word list.

## Step 6. Show the groups on a web page

The last script uses only Python's standard library. It reads `items.json`, groups the headlines, and serves a page at `http://127.0.0.1:8011/`. Repeated stories come first. Each headline links to the publisher's own page.

{{file:app.py}}

Start it with `python app.py`, then open the address in your browser. The tool saved this screenshot from the running page:

{{shot:06-page|The running page with two repeated stories and a list of other headlines}}

Press Control and C in the terminal to stop the server.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'feedparser'`.** The virtual environment is not active. Activate it and run `pip install -r requirements.txt`.
- **A feed prints `skipped`.** The feed could not be read. Check the address in a browser. If the publisher blocks automated requests, remove the line.
- **No repeated stories.** Different feeds may not cover the same news today. Run `python fetch_feeds.py` again later, or add more feeds. You can also lower `THRESHOLD`, but check the groups by eye after each change.
- **Two different stories are grouped.** Raise `THRESHOLD`, or add the shared word to `STOPWORDS`.

## Frequently asked questions

**How do I find duplicate headlines?**

Lower-case each headline, drop small words, and score two headlines by the share of words they have in common. Group headlines from different feeds when the score is 0.25 or higher. Never group two headlines whose version numbers differ.

**Do I need an AI model to remove duplicates?**

No. This tool uses word overlap and needs no API key. On 10 November 2026 it turned 80 items into 78 stories, and two stories appeared in two feeds each. Embeddings were not tested here.

**How do I test a grouping rule?**

Use fixed headlines, so the answer is the same every time. The tutorial has three checks: a repeated story is grouped, two different versions stay apart, and an unrelated item stays alone. Run them after every change to the threshold.

## What to try next

- Show how many feeds carried each story.
- Run `fetch_feeds.py` every hour and keep what you have seen.
- Replace the word-overlap score with embeddings and compare the groups.

## How this tutorial was tested

Every command and screenshot above comes from one real run on 10 November 2026. The code in the blocks is copied from the project files. The six steps were then run again from an empty folder, and all of them passed. Terminal screenshots show the saved output of each command in a terminal-style frame. The page screenshot is a real browser screenshot of the running app.
