---
title: "Build a Streaming Chat Page in Next.js"
seo_title: "Streaming Chat Page in Next.js: AI Hackathon Tutorial"
meta_description: "Build a streaming chat page in Next.js for your AI hackathon project, with history, a stop button and clear error states."
---

# Build a streaming chat page in Next.js

You build a chat page in Next.js that streams answers from the Anthropic API as they are written, keeps the conversation history, has a Stop button, and shows a clear message when something fails.

**Time:** about 45 minutes. **Level:** intermediate. **You need:** JavaScript and React basics, Node 20.9 or newer, an Anthropic API key, and Google Chrome if you want to run the browser steps. **Tested:** 11 November 2026 with Node 20.20.2, Next.js 16.4.6, React 19.3.1, `@anthropic-ai/sdk` 1.8.0 and Chrome 157 on macOS. Every package version is pinned to an exact version in `package.json`, because versions change fast. Check them again before you copy this into a new project.

A chat page is a common screen to put in front of a room when you demo an AI hackathon project. A Stop button and readable errors take a few extra minutes and stop the demo from freezing in front of a room. If you are looking for a project to build this into, see the [upcoming AI hackathons](/ai-hackathons/).

Model replies differ from run to run. Your words, chunk counts and timings will not match the output below. The shape of the output will.

## Why this matters

A language model writes an answer a few words at a time. If the page waits for the whole answer, the reader stares at nothing. Streaming shows the words as they arrive. In this project the first words reached the test script after about 1.4 seconds, and the whole short answer was done at about 1.7 seconds, so the wait for first text is the part the reader feels.

Streaming also brings problems that a plain request does not have. The user may want to stop. The connection may fail before the first word, or halfway. Most tutorials leave those out. This one builds them in.

## See it running first

This is the finished page in Chrome. It has sent two messages. The second question, "Which of those three...", only makes sense because the page sends the earlier messages with it.

![Chat page in Chrome with two questions and two answers, the second answer refers to the three tips from the first](images/shot-history.png)

The rest of the tutorial builds it from nothing.

## Step 1: Set up the project

Create a folder and put this `package.json` in it. The versions have no `^` or `~`, so everyone who follows the tutorial installs the same code. `puppeteer-core` is only used by the test scripts in later steps.

{{file:package.json}}

Install and build. The `npm ls` lines in the output show what was installed.

{{cmd:01-install}}

{{shot:01-install|Terminal output of npm install and the list of installed versions}}

The page, layout and styles come in Step 3. For the build below, the finished files are already in the folder.

## Step 2: Add a route that streams

The browser must never hold your API key. The route handler runs on the server, reads the key from `process.env`, and passes the browser only the answer text.

Three choices in this file are worth reading before you copy it:

- **Check the body at the edge.** The route accepts 1 to 20 messages, each a `user` or `assistant` message under 2000 characters, starting and ending with a user message. The browser is not trusted, so the route rebuilds each message with only `role` and `content`.
- **Use `messages.create` with `stream: true`.** The call resolves once the API has accepted the request. A bad key fails there, so the route can return a proper error status before any text is streamed. I checked this with a wrong key in Step 7: the route answered with a clear error instead of an empty stream.
- **Close the call to the API when the browser leaves.** `cancel()` runs when the browser drops the connection, which is what Stop does. It aborts the request to the API too, so the model stops working on an answer nobody will read.

`thinking: { type: "disabled" }` is copied from the Python version of this idea in `stream-llm-answers`. I did not test the route without it.

{{file:app/api/chat/route.js}}

The model name and the limits are constants at the top. The model used here is `claude-haiku-5-5`, a small model chosen to keep the runs cheap.

Build the app:

{{cmd:02-build}}

{{shot:02-build|Terminal output of npm run build, ending with the route list that includes /api/chat as dynamic}}

The route list at the bottom shows `/api/chat` as dynamic, meaning it runs on each request. The page itself is static. From here on the steps use the built app (`npm start`) so that the first request is not slowed by compiling. While you edit, `npm run dev` does the same job with reloads. I did not run the dev server for this tutorial.

### Try the route without a page

Before there is a page, call the route from a script. `scripts/call-route.mjs` posts one question and prints when each piece of the answer arrives.

{{file:scripts/call-route.mjs}}

`scripts/with-server.sh` starts the built app on port 8129, runs the command you give it, stops the app, and prints the lines the route wrote to its log.

{{file:scripts/with-server.sh}}

First, see what a missing key looks like. This run has no key in its environment. The script exits with code 1, which is what the step expects.

{{cmd:03-no-key}}

{{shot:03-no-key|Terminal output: status 500 and the error message that the key is not set on the server}}

The route answers with status 500 and a message that names the variable. The page will show this text later, so it says what to fix.

Next, send a body the page would never send, to see the validation. This one starts with an assistant message.

{{cmd:04-bad-input}}

{{shot:04-bad-input|Terminal output: status 400 and a message about the allowed messages}}

Now the real call with a key. Put your key in a `.env` file (copy `.env.example`) and load it into the terminal:

{{file:.env.example}}

```bash
set -a; source .env; set +a
```

Never paste a real key into code, a screenshot or a chat.

{{cmd:05-stream}}

{{shot:05-stream|Terminal output of call-route.mjs: status 200, the first six chunks with arrival times, then the full answer}}

Read the lines that start with `chunk`. The first piece arrived at 1419 ms and was the words "Because a demo is". The next five arrived within 6 ms of each other, and the 18th and last piece arrived at 1738 ms. The answer was not one block. The last line of the server log shows 76 output tokens. The route counts text pieces, not tokens, so the two numbers differ.

## Step 3: Build the chat list

The page is one client component. It keeps the messages in state. Each time a piece arrives, it replaces the last assistant message with the longer text. To send a new question, it sends the whole list again, since the API remembers nothing between calls. That is why the second answer in the first screenshot can refer to "those three".

{{file:app/page.js}}

The styles are plain CSS:

{{file:app/globals.css}}

And the layout:

{{file:app/layout.js}}

Open the built app before any chat. This screenshot is taken by the runner from the running app.

{{cmd:06-page}}

{{shot:06-page|Chrome screenshot of the empty chat page with a text box and a disabled Send button}}

Now drive the page the way a person would. `scripts/drive.mjs` opens the page in Chrome with `puppeteer-core`, types a question, clicks Send, and saves screenshots. It takes the first screenshot while the answer is still arriving.

{{file:scripts/drive.mjs}}

{{cmd:07-chat}}

{{out:07-chat}}

{{shot:07-chat|Terminal output of drive.mjs chat}}

This is the page in the middle of the first answer. The red Stop button replaced Send, and the answer so far is on screen.

![Chat page while the first answer is arriving, the Stop button is shown](images/shot-streaming.png)

The log says the Stop button was visible at 2018 ms with part of the first tip on screen, and the first answer finished with 281 characters. After the second question the page held 4 messages. The server log shows the two calls: 31 chunks and 92 output tokens for the first, 16 chunks and 61 for the second. Your numbers will differ.

## Step 4: Add a stop button

While an answer is streaming, the Send button is replaced by Stop. Stop calls `abort()` on the `AbortController` that was passed to `fetch`. The `fetch` rejects with an `AbortError`, and the page keeps the text that has arrived and marks it `[stopped]`. The text stays in the history, so the next question includes it.

The test asks for a long story, waits until there is some text, and clicks Stop.

{{cmd:08-stop}}

{{shot:08-stop|Terminal output of drive.mjs stop: 91 characters on screen, no more text after 2.5 seconds, and a server log line that the client left}}

There are two proofs here. Two and a half seconds after the click, the page still had 91 characters, so the text really stopped. And the server log says `client left after 14 chunks, upstream request aborted`, so the route noticed and closed its call to the API. Without the `cancel()` handler in the route the page would stop, but the model would keep generating and you would keep paying for it.

![Chat page after Stop: a half-written story with the [stopped] tag and the Send button back](images/shot-stopped.png)

## Step 5: Handle errors

The page shows an error in a red banner with a Try again button, keeps the user's question in the list, and leaves the text box usable. The route returns a short message for each failure, and the page shows that message as it is.

The page has two paths. If nothing has arrived, the empty assistant message is removed and the error is shown. If part of an answer arrived and then the connection failed, the page keeps the part and says the answer was cut off. Try again sends the same history again.

Two failures were run for real. First, a server with no key:

{{cmd:09-error-no-key}}

{{shot:09-error-no-key|Terminal output of drive.mjs error: the error text says the key is not set on the server}}

![Chat page with a red banner saying the key is not set on the server and a Try again button](images/shot-error-no-key.png)

Second, a server with a key the API refuses. The key `not-a-real-key` is a made-up string, so the API answered with status 401:

{{cmd:10-error-bad-key}}

{{shot:10-error-bad-key|Terminal output of drive.mjs error with a wrong key: the page shows that the model call failed with status 401}}

![Chat page with a red banner saying the model call failed with status 401](images/shot-error-bad-key.png)

The route logs the status and shows the browser only "The model call failed (status 401)." The raw API message does not reach the page. For a demo that is the right amount of detail. In your own project you may want to log more on the server.

Not run: clicking Try again, and the "cut off" path, where the connection fails halfway through an answer.

### Check that the key stayed on the server

One last check. This script looks through every file the browser can download from `.next/static` for the key value and for the variable name.

{{cmd:11-no-leak}}

{{shot:11-no-leak|Terminal output of check-leak.mjs: 11 files checked, none contains the key or the variable name}}

None of the 11 files contains either. This is a check of this build, not a security review. Anything you import into a client component ends up in those files, so run the check again after you change the code.

## Troubleshooting

- **`ANTHROPIC_API_KEY is not set on the server.`** The server did not get the variable. Run `set -a; source .env; set +a` in the same terminal you start the server from, or use a `.env.local` file, which Next.js loads itself.
- **`The model call failed (status 401).`** The key is wrong or revoked. Create a new one in your Anthropic account and restart the server. The server reads the variable when it starts.
- **`Send 1 to 20 messages that start and end with a user message.`** The route refused the body. After 20 messages the page will hit this. Trim the oldest messages in the page before you send.
- **Stop works on the page but the server log has no `client left` line.** The route must have the `cancel()` handler. Without it the call to the API runs to the end.
- **A screenshot or test cuts off the bottom of the chat.** The test window was too short for the conversation. `scripts/drive.mjs` sets the window height. Raise it.

## Frequently asked questions

**Is Next.js good for an AI hackathon project?**

It worked for this one. A route handler holds the key and streams the answer, and one page file holds the whole chat. You can build and run it with two commands. The tutorial did not compare it with other frameworks.

**How do I add a stop button to a chat?**

Pass an `AbortController` signal to `fetch`, and call `abort()` when the user clicks Stop. Keep the text that has arrived. In the test, 91 characters stayed on screen and no more arrived. Close the API call on the server too, in the stream's `cancel()` handler.

**How do I show an error in a chat UI?**

Make the route return a short message and a status code for each failure, and show that message in a banner with a way to retry. The tutorial ran two: a missing key and a wrong key. Check for errors before you start streaming, so you can return a real status code.

## What to try next

- Add a Try again test: break the key, send, fix it, click Try again.
- Trim the history in the page after 20 messages, or by token count.
- Show a small "typing" marker while the page waits for the first piece.

## How this tutorial was tested

- Date: 11 November 2026. Node 20.20.2, Next.js 16.4.6, React 19.3.1, `@anthropic-ai/sdk` 1.8.0, `puppeteer-core` 25.17.0, Google Chrome 157, macOS. The model is `claude-haiku-5-5`, set in the `MODEL` constant of the route.
- The code in this article is copied from the project files by a script. The output comes from saved logs of real API calls on a running app.
- Every step was run from a clean state, then replayed from an empty copy of the folder with a fresh `npm install`. Model replies differed between the runs, as expected.
- Screenshots of terminal steps are rendered from the saved output of the run. They are not captures of a terminal window. The images named `shot-*.png` and the empty-page image are real screenshots taken by Chrome from the running page.
- The built app (`npm start`) was used for every step.
- Not run: `npm run dev`, Windows, Linux, browsers other than Chrome, Node versions other than 20.20.2, clicking Try again, a failure halfway through an answer, and a mobile screen size.
