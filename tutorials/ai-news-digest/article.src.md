---
title: "Build an AI News Digest: AI Hackathon Project Idea"
seo_title: "Build an AI News Digest: AI Hackathon Project Idea"
meta_description: "AI hackathon project idea: build a news digest from RSS feeds with an LLM, with the source link beside every summary."
---

# Build a personal AI news digest from RSS feeds with an LLM

You build a Python script that reads five public RSS feeds, removes duplicate items, asks a language model for a one-sentence summary of each item, and writes a page with the source link beside every summary.

**Time:** about 30 minutes. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, a terminal and an Anthropic API key. **Tested:** 11 November 2026 on macOS with Python 3.14.6, `feedparser` 6.0.14 and `anthropic` 2.8.0.

A news digest is a good AI hackathon project idea: the data is small, the result is clear and anyone can follow a demo. If you are looking for a project, see the [upcoming AI hackathons](/ai-hackathons/) and pick one that fits. Everything below also works outside an event.

Live feeds change every day, and model replies differ from run to run. Your items and wording will not match the output below. The shape of the output will.

## Why this matters

A summary is only useful if you can check it. A model can leave out a detail or add one that is not in the text. So this digest keeps the link from the feed next to each summary, and the code, not the model, supplies that link. If a summary looks wrong, one click takes you to the original.

## See it running first

This is the finished page. The items here are invented example items from `sample_items.json`, not real headlines. The summaries on it are real model output. The rest of the tutorial builds it from scratch.

{{shot:08-view|A web page titled My AI news digest with five items, each with a short summary and a Source line with a read the original link}}

## Step 1: Set up the project

Make a folder and create a virtual environment. Activate it. The commands from here on assume it is active.

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt`:

{{file:requirements.txt}}

Install it. The output shows the versions used for this tutorial.

{{cmd:02-install}}

{{shot:02-install|Terminal showing feedparser 6.0.14 and anthropic 2.8.0 installed}}

Put your key in a file named `.env`. Copy the placeholder file and edit it:

{{file:.env.example}}

Never paste a real key into code or a screenshot. Add `.env` to `.gitignore`. Load it into your terminal session (macOS and Linux):

```bash
set -a; source .env; set +a
```

## Step 2: Pick five feeds and read them

Put one feed address per line in `feeds.txt`. These are the five used here. Use any public feeds you like, and check each site's terms for personal or other use before you rely on a feed.

{{file:feeds.txt}}

`fetch_feeds.py` reads each feed with feedparser. It keeps the title, link, date and a short plain-text excerpt of each item, and only the three newest items per feed so that the run stays small. If a feed cannot be read, the script prints a "skipped" line and moves on. It does not try another way in.

{{file:fetch_feeds.py}}

{{cmd:03-fetch}}

{{shot:03-fetch|Terminal showing three items read from each of five feeds and 15 items saved}}

Five feeds with three items each gave 15 items. The screenshot shows counts only, because the items are other people's headlines and this tutorial does not republish them.

## Step 3: Remove duplicates

Two feeds often cover one story, and one feed may list the same page twice with a different tracking tail on the address. `dedupe.py` treats two items as the same when the link matches after the query part and the trailing slash are removed, or when the title matches after lowercasing and removing punctuation. It keeps the first one it sees.

This is a plain rule on purpose. It does not catch two different headlines about one story. Matching on meaning is a bigger job, so it is left out.

{{file:dedupe.py}}

To see the rule work on data that never changes, run it on `sample_items.json`. It holds six invented items. Two of them are the same story under different links.

{{file:sample_items.json}}

{{cmd:04-dedupe}}

{{shot:04-dedupe|Terminal showing six items in, five kept and one duplicate removed}}

The first and second items have different links (`example.com` and `www.example.org`) but the same title, so the second one is removed. On the live feeds the same script printed `15 items in, 14 kept, 1 duplicates removed` in the last step of this tutorial. Your count will differ.

## Step 4: Summarise each item

`summarise.py` sends one request per item. The instructions tell the model to use only the title and text it is given, to add nothing, and to reply with a fixed sentence when the text is too thin. Without that last instruction a model tends to fill the gap with a guess. The model name comes from `TUTORIAL_MODEL` when it is set, and otherwise it is `claude-haiku-5-5`.

The link is copied from the feed item into the result. It is never part of the request, so the model cannot change it or invent one.

{{file:summarise.py}}

`spend_log.py` is a budget helper. It adds one line per call to `spend.log` and is not part of the lesson.

{{file:spend_log.py}}

First see what a missing key looks like. Run the script in a terminal where the variable is not set:

{{cmd:05-no-key}}

{{shot:05-no-key|Terminal showing the message that ANTHROPIC_API_KEY is not set}}

Now run it with the key loaded:

{{cmd:06-summarise}}

{{shot:06-summarise|Terminal showing five numbered items with a one-sentence summary and a link under each}}

Read the summaries against the example items. The 12 languages and the 4,000 photos come from the text that was given. The "Weekly roundup" item had an empty text field, so the script returned the fixed sentence, "Not enough text to summarise.", instead of a guess. That is the behaviour you want, and it is the one thing to check first if you change the instructions.

## Step 5: Write the page

`build_page.py` turns the summaries into `digest.html` and `digest.md`. It escapes the text before it goes into the page, and each item gets a "read the original" link.

{{file:build_page.py}}

{{cmd:07-page}}

{{shot:07-page|Terminal showing the digest written with five items and the first lines of digest.md}}

Serve the folder and open the page in a browser:

```bash
python -m http.server 8019 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8019/digest.html`. It looks like the screenshot at the top.

## Step 6: Run the whole chain on live feeds

The same three scripts work on the feeds you fetched in Step 2. This run reads only the first three items to keep the cost small, and it prints counts, not headlines.

{{cmd:09-live}}

{{shot:09-live|Terminal showing duplicates removed, three items summarised and a digest written}}

Open `live/digest.html` to see your own digest. It contains other sites' headlines and short model summaries. Keep it for yourself, or check the terms of each feed before you share it.

## Troubleshooting

**"ANTHROPIC_API_KEY is not set."** The variable is not in this terminal. Run the `set -a; source .env; set +a` line again in the same window.

**A line starting "skipped" when you fetch.** The feed could not be read. It may be down, moved, or it may refuse automated requests. Remove it from `feeds.txt` or replace it. Do not look for a way around a refusal.

**"Not enough text to summarise."** The feed gave a title and little else. Some feeds send only the headline. Either accept it, or fetch the full article page where its terms allow that, which this tutorial does not cover.

**The same story shows twice.** Two different headlines about one story are not caught by the link and title rule. See the ideas below.

## What to try next

- Send the digest as a message to yourself instead of writing a page.
- Add a rule for stories that appear in more than one feed, such as comparing the words in two titles.
- Read the summaries in a second pass and ask a model to flag any sentence that is not backed by the item text.

## Frequently asked questions

### Is a news digest a good AI hackathon idea?

It fits a short event. This one uses five feeds, five short scripts and one page, and you can show a working result in a few minutes. The check against the source link also gives you something to say about accuracy.

### Can I use RSS feeds in a hackathon project?

Public feeds are made to be read by programs, and this project reads them with a normal feed library. Each site sets its own terms, so check them, keep the source link beside every summary and avoid republishing full articles. If a feed refuses a request, skip it.

### How do I keep AI summaries accurate?

Give the model only the item's own text, tell it to add nothing, and give it a fixed reply for when the text is thin. Keep the link next to every summary, supplied by your code. In this run the item with no text got the fixed reply, and the other four summaries matched the text they were given.

## How this tutorial was tested

Tested on 11 November 2026 on macOS with Python 3.14.6. The code in this article is copied from the project files, and the command output is the saved output of the run. The steps ran from a clean state, and then again from a copy of the project in an empty folder. All steps passed both times.

The terminal images are rendered from the saved output of the real run. They are not captures of a terminal window. The page image is a real Chrome screenshot of the page served by the project. It shows invented example items, not real headlines.

Not run: Windows and Linux, Python versions other than 3.14, and any feed other than the five in `feeds.txt`. The model calls used `claude-haiku-5-5` with small inputs. The live step's counts and summaries change every day.
