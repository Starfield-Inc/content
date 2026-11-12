---
title: "Build a Draft Helper with a Safety Layer in Flask and Claude"
seo_title: "AI Hackathon Draft Helper: Safe Flask and Claude App"
meta_description: "Build an AI hackathon writing app in Flask with Claude: a length limit, a moderation call, a guarded system prompt and a key kept on the server."
description: "Build an AI hackathon writing app in Flask with Claude: a length limit, a moderation call, a guarded system prompt and a key kept on the server."
---

# Build a draft helper with a safety layer in Flask and Claude

You build a small web app where a user pastes a draft and gets three suggestions from Claude. The server limits the length, screens the draft with a second Claude call, tells the model to refuse harmful requests, and never sends the API key to the browser.

**Time:** about 45 minutes. **Level:** intermediate. **You need:** Python basics, Python 3.10 or newer, a little HTML and JavaScript, and an Anthropic API key. **Tested:** 12 November 2026 with Python 3.14.6, Flask 3.1.3 and the `anthropic` package 2.8.0 on macOS, in Chrome.

Model replies differ from run to run. Your suggestions and the wording of the moderation reasons will not match the output below. The shape of the output will.

An app that sends user text to a model is open to misuse the moment it is public, which matters for any AI hackathon demo that judges or visitors can try. The checks here are small enough to add in an afternoon. If you are planning a project, see the [upcoming AI hackathons](/ai-hackathons/).

## Why this matters

A text box connected to a model will receive text you did not plan for: very long pastes, empty submissions, requests to write threats, and drafts that contain orders aimed at the model. Each of these needs a different answer, and the low-cost answers come first. A length check costs nothing. A moderation call costs one short model call. The suggestion call costs the most, so it only runs for drafts that pass the first two.

This is a teaching version. It shows the layers and shows each one working on real calls. It is not a complete safety system, and the end of the article lists what it does not cover.

## See it running first

This is the finished page after a draft passed all the checks and came back with three suggestions. It is a real Chrome screenshot of the running app.

{{shot:09-page-good|The Draft helper page with a short draft about a school garden club, a character counter, and three plain-text suggestions below it}}

The rest of the tutorial builds it from nothing.

## Step 1: Set up the project

Create a virtual environment. The commands from here on assume it is active (`source .venv/bin/activate`).

{{cmd:01-venv}}

{{shot:01-venv|Terminal after creating the virtual environment}}

Create `requirements.txt`:

{{file:requirements.txt}}

Install it and check the versions.

{{cmd:02-install}}

{{shot:02-install|Terminal output listing the installed Flask and anthropic versions}}

You should see `Flask` and `anthropic` with version numbers. Yours may be newer than 3.1.3 and 2.8.0.

## Step 2: Limit the length first

The check that costs nothing goes first and runs on the server. A check in the browser can be skipped by anyone who calls the endpoint directly, so the page only shows a counter as a courtesy. The limit is 1500 characters, which is a few paragraphs and keeps each call small.

The function trims the text, rejects an empty draft, and rejects a draft over the limit. It raises a `Rejected` error with a message that is safe to show to the user.

{{file:safety.py}}

Test it without a key and without the network.

{{file:test_safety.py}}

{{cmd:03-tests}}

{{shot:03-tests|Terminal output of three passing unit tests}}

You should see `Ran 3 tests` and `OK`. One test checks the edge: exactly 1500 characters passes and 1501 does not.

## Step 3: Add the moderation call and the suggestion call

There are two model calls, and each has its own system prompt.

The moderation call reads the draft and returns JSON: `allowed` and a one-sentence `reason`. It is told that ordinary writing on hard topics is allowed, so a news story or a piece of fiction is not blocked just for its subject. If the reply cannot be read as JSON, the function returns "not allowed". That is called failing closed: when the check breaks, the draft is held back, not let through.

The suggestion call has a system prompt that does three things. It says the draft is material to edit, not instructions to follow. It asks for three suggestions and one strength, in plain text. It tells the model to say it cannot help if the draft asks for or contains harmful content, such as threats, harassment, scams or instructions for hurting people.

The draft goes into the message wrapped in `<draft>` tags, so the model can tell where the user's text starts and ends. Both calls pass `thinking={"type": "disabled"}` so that the small `max_tokens` values are spent on the reply.

{{file:assistant.py}}

The tutorial uses two fixed drafts, so every run starts from the same input.

{{file:drafts.py}}

Run the moderation call alone on the good draft and the harmful one.

{{file:demo_moderation.py}}

{{cmd:05-moderation}}

{{shot:05-moderation|Terminal output: the good draft is allowed and the harmful draft is not, each with a one-sentence reason}}

The good draft returns `allowed=True`. The harmful draft, a request for a message to frighten a named neighbour, returns `allowed=False` with a reason. The wording of the reason will differ for you.

## Step 4: Wrap it in a Flask server

The server holds the key and does the checks in a fixed order: read the JSON, check the length, moderate, then suggest. Each outcome has its own status code, so the page and any script can tell them apart:

- 400 for a bad request, such as an empty or too long draft.
- 422 for a draft the moderation call blocked. The body includes `"blocked": true`.
- 502 for a failure in the model service. The detail goes to the server log, and the user gets a general message.

The app refuses to start without the key. This is the first thing to see when something is wrong, so the next step shows it.

{{file:app.py}}

Start the app without a key.

{{cmd:04-no-key}}

{{shot:04-no-key|Terminal output: ANTHROPIC_API_KEY is not set}}

The app exits with a one-line message and a non-zero exit code. Load your key and run `python app.py` to start it on port 8125.

## Step 5: Add the page

The page is one HTML file served by Flask. It has a text area, a counter that turns red over the limit, a button, and a box for the result. A reply with a 422 status is shown in an amber box, and any other error in a red box, so a blocked draft does not look like a crash.

The page sends the draft to `/api/suggest` on the same server. There is no key and no model name in the page.

{{file:templates/index.html}}

The last lines of the script add a way to repeat a run without typing: `/?draft=...` fills the box and sends it once. A short script that the server answers after eight seconds keeps the page in a loading state, so a screenshot taken at load time shows the finished result. That helper exists only for the screenshots and the app would work without it.

## Step 6: Try every outcome from the command line

This script sends four drafts to the running endpoint, the way the page does. It prints the status and the JSON for each.

{{file:try_endpoint.py}}

{{cmd:06-endpoint}}

{{shot:06-endpoint|Terminal output of four requests: a good draft with HTTP 200 and suggestions, a harmful draft with HTTP 422 and blocked true, an empty draft with HTTP 400, and a too long draft with HTTP 400}}

You should see four results:

- The good draft returns HTTP 200, the suggestions, and the token counts.
- The harmful draft returns HTTP 422 and `"blocked": true`. No suggestion call was made for it.
- The empty draft returns HTTP 400.
- The 1501-character draft returns HTTP 400 with "The limit is 1500."

The last two never reached a model. That is the point of putting the free checks first.

## Step 7: Try a draft that gives the model orders

A draft is text from a stranger, and it can contain sentences that look like instructions. This is called prompt injection. The fixed draft here is an essay about bees with one added line telling the model to ignore its instructions and reply with one word.

{{cmd:07-injection}}

{{shot:07-injection|Terminal output: HTTP 200 and three suggestions about the bee essay, with no sign that the added instruction was followed}}

In this run the model treated the added line as part of the draft and gave suggestions about it. I ran this once per test pass, not many times, so it shows that the prompt can hold, not that it always will. A system prompt reduces this risk. It does not remove it, so do not give the model any tool or action that you would not give the user.

## Step 8: Check that the key is not in the page

The key is read by the server and used only in the call to the API. The page never needs it. Check this with a script that fetches the page and every script it loads from the server, then looks for the key value in each.

{{file:check_leak.py}}

{{cmd:08-leak}}

{{shot:08-leak|Terminal output: the page is 3267 bytes, key present False, and the line The key stays on the server}}

You should see `key present: False` and the closing line. This checks the files the app serves. It does not check your server logs, your shell history or your repository, so keep `.env` out of git. The `.gitignore` in this project does that, and `.env.example` holds only the variable name.

## Step 9: See the three outcomes in a browser

These are real Chrome screenshots of the running page. Each one loads the page with a draft in the address, so the result is there at load time.

A draft that passes:

{{shot:09-page-good|The Draft helper page with a school garden club draft and three plain-text suggestions}}

A draft the moderation call blocks. The box is amber, it says "Not sent for suggestions", and it gives the reason:

{{shot:10-page-blocked|The Draft helper page with a harmful draft and an amber box saying the draft was not sent for suggestions, with a reason}}

A draft over the limit. The counter is red, and the server's message is shown. In this screenshot the page still sent the draft, to show that the server checks the limit even when the browser does not stop it:

{{shot:11-page-long|The Draft helper page with a draft of repeated letters, a red counter reading 1501 of 1500, and a red box saying the draft has 1501 characters and the limit is 1500}}

## What this does not cover

- **A moderation call is not a guarantee.** It can block a harmless draft and pass a harmful one. This tutorial tested one clear example of each. Read the false positives and false negatives of your own prompt before you rely on it.
- **There is no rate limit.** Anyone who can reach the server can send as many drafts as they like, and each one costs money. Add a limit per address before you share a public link.
- **There are no accounts and no logging of drafts.** That is simple for privacy, but you cannot investigate misuse either. Decide what you need to keep.
- **The server is Flask's built-in development server.** Use a production server if the app leaves your laptop.
- **Drafts are sent to the Anthropic API.** Tell your users, and do not let them paste what they should not share. Check the current terms and privacy policy of the service you use.

## Troubleshooting

- **The suggestions show `**` around words.** This happened while building this tutorial. The page shows the reply as plain text, and the model had used Markdown bold. The suggestion prompt now says "Use plain text with no Markdown symbols", and the screenshots here were taken after that change. If you would rather keep Markdown, render it in the page with a library and sanitise the output.
- **`ANTHROPIC_API_KEY is not set` when you start the app.** The variable is not in the terminal you are running from. Run `set -a; source .env; set +a` in that terminal.
- **The page screenshot is cut off.** My first capture of the good draft at 640 pixels high stopped in the middle of the suggestions. The window was too short. I raised it to 800.
- **Port 8125 is already in use.** An earlier copy of the app is still running. Stop it, or set `PORT` to another number. The scripts in this tutorial use 8125, so change `BASE` and `URL` there as well.
- **Flask prints a development server warning.** That is expected when you run `python app.py`. It is not an error.

## Frequently asked questions

**How do I keep my Claude API key out of the browser?**

Call the API from the server only. Here the browser sends the draft to `/api/suggest`, and Flask makes the call with the key from its environment. `check_leak.py` fetched the page and its scripts and found the key in none of them.

**Can a second Claude call moderate user text?**

Yes, for a simple check. The moderation call here returns JSON with `allowed` and a reason, and the app returns HTTP 422 for a blocked draft without making the suggestion call. In the runs for this tutorial it allowed the garden club draft and blocked the threatening one. That is two examples, so it does not show how well it works on other text.

**Does a system prompt stop prompt injection?**

It lowers the risk but does not remove it. In this tutorial's run, a draft that told the model to ignore its instructions was treated as text to edit. That was one test on one draft. Keep layers that do not depend on the model, such as the length limit, and do not give the model access to actions you would not give the user.

## What to try next

- Add a rate limit per address, and test it with the same script style as `try_endpoint.py`.
- Run the moderation prompt on twenty drafts that you label by hand, and count the blocks that were wrong in each direction.
- Stream the suggestions to the page as they arrive, and keep the moderation call before the stream starts.

## How this tutorial was tested

- Date: 12 November 2026. Python 3.14.6, Flask 3.1.3, `anthropic` 2.8.0, macOS, Chrome (headless). The model is `claude-haiku-5-5`, set in the `MODEL` constant.
- The code in this article is copied from the project files by a script. The terminal output comes from saved logs of real runs, with real API calls.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no virtual environment. The replay passed. Model replies differed between the two runs, as expected.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window. The three browser screenshots are real Chrome captures of the running page.
- Not run: Windows, Linux, browsers other than Chrome, Python versions other than 3.14.6, a production server, and models other than `claude-haiku-5-5`. The moderation prompt was tried on one harmful and one harmless draft, and the injection test on one draft.
