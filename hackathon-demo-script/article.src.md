---
title: "Hackathon Demo Script and Test Data Checklist"
seo_title: "AI Hackathon Demo Script and Test Data Checklist"
meta_description: "An AI hackathon demo script and checklist: a three-minute story, seeded test data and a backup recording, so nothing breaks while judges watch."
description: "An AI hackathon demo script and checklist: a three-minute story, seeded test data and a backup recording, so nothing breaks while judges watch."
---

# Prepare a hackathon demo script and test data so nothing breaks

You build a timed three-minute demo script, a set of seeded test data, a rehearsal check and a preflight script that catches the failures that most often stop a demo.

**Time:** about 40 minutes. **Level:** beginner. **You need:** Python 3.10 or newer and a terminal. No packages and no API key. **Tested:** 11 November 2026 on macOS with Python 3.14.6. `ffmpeg` 8 or later is optional, for Step 6 only.

Most AI hackathon demos fail for small reasons, such as a missing file or a slow network, and a script and a checklist catch them. A demo is short, you cannot restart it, and the judges only see what happens in those minutes. Browse the [upcoming AI hackathons](/ai-hackathons/) to find your next slot, then use this to prepare for it.

The example project is a made-up app called Ticket Triage Assistant. Swap in your own story. The tools do not care what the app does.

## See it running first

This is the preflight check you will have at the end. It checks the test data, the backup video, the port, the disk and the network in one command.

{{shot:08-preflight-pass|Preflight output with five checks passed and none failed}}

The rest builds it from scratch.

## Step 1. Write the three-minute story

A story with five beats is easy to rehearse and easy to cut. Each beat has a time budget in its heading. Lines that start with `>` are notes about what is on screen and are not spoken. Write your own words and keep sentences short enough to say in one breath.

{{file:demo_script.md}}

## Step 2. Seed the test data

Live data changes, and a demo cannot depend on it. This script writes 12 made-up tickets and uses a fixed random seed, so you get the same bytes every time. Four of the tickets are planned edge cases: an empty body, a non-English ticket, an emoji and a very long text. A fifth is a duplicate. These are the inputs that tend to break a first version, so they should be in your sample data on purpose.

{{file:seed_data.py}}

Run it:

{{cmd:01-seed}}

{{shot:01-seed|The seed script writing 12 tickets with a hash and one empty body}}

It wrote 12 tickets. The hash `c5217e68bfc2` identifies this exact file, and one ticket has an empty body.

Now check that a second build matches the file on disk:

{{cmd:02-seed-check}}

{{shot:02-seed-check|The check confirming the data matches the seed}}

If someone edits `demo_data.json` by hand before the demo, this check says no. That is the point.

## Step 3. Time the script before you rehearse

Counting words is a fast way to find a script that is too long. This tool counts the spoken words in each beat and converts them to seconds. The rate of 130 words a minute is an assumption, not a measured value. Time yourself reading one beat aloud and pass your own rate with `--wpm`.

{{file:check_script.py}}

Run it:

{{cmd:03-script-time}}

{{shot:03-script-time|Per-beat word counts and estimated seconds for the demo script}}

The script is 148 seconds at 130 words a minute, which leaves 32 seconds in a 180-second slot. One beat, "How it works", is 25.8 seconds against a 25-second budget. The tool flags it. You can cut a sentence or move a few seconds from the live demo beat, which has room.

## Step 4. See what a short slot looks like

Many events give less than three minutes. Check the same script against a 120-second slot:

{{cmd:04-script-short-slot}}

{{shot:04-script-short-slot|The tool reporting the script is 28 seconds too long for a 120 second slot}}

The tool exits with code 1 and says the script is 28 seconds too long. Cut words now, not on stage. Read the rules for your own event to find the real slot length.

## Step 5. Rehearse with a stopwatch

Estimates are only a start. Say the script aloud, time each beat on a phone and type the seconds into this tool.

{{file:rehearse.py}}

The times below are example numbers we typed in to show the output. They are not a measured rehearsal. Use your own.

{{cmd:05-rehearse}}

{{shot:05-rehearse|Example rehearsal times compared with the budget for each beat}}

The example total is 164 seconds, which leaves 16 seconds. The tool asks for at least 10 seconds spare, because a demo that runs to the last second has no room for one slow page load.

## Step 6. Check everything with a preflight script

A checklist you read is easy to skip. This script checks the things that can be checked: the test data, the backup video, whether the port is free, free disk space and whether the network is reachable. A failed network is a warning, because some demos are meant to run offline.

{{file:preflight.py}}

First run it with no backup video:

{{cmd:06-preflight-fail}}

{{shot:06-preflight-fail|Preflight failing because the backup video is missing}}

Four checks pass and one fails: `backup/demo-backup.mp4` is missing. The script exits with code 1. This is the mistake the checklist exists to catch. The disk figure and the network line come from this computer and will differ on yours.

Record a backup video of your demo working and save it as `backup/demo-backup.mp4`. A screen recorder on your laptop works. This tutorial's tooling could not capture a desktop window, so it makes a three-second test pattern with `ffmpeg` instead. That file is a stand-in to prove the check works, not a real recording.

{{cmd:07-stand-in-video}}

{{shot:07-stand-in-video|Terminal after creating the stand-in video file, showing its size}}

Run the preflight again:

{{cmd:08-preflight-pass}}

All five checks pass. The backup video line shows a length because `ffprobe`, which comes with `ffmpeg`, read the file. Without `ffprobe` the script prints a warning and checks only the file size.

## Step 7. Pack the checklist

Some things cannot be scripted, such as the charger and the screen sleep setting. Keep them in one short file and tick them in the room.

{{file:checklist.md}}

## Troubleshooting

- **"Cannot find demo_script.md".** Run the commands from the project folder, or pass the full path.
- **"No beats found".** The heading must look like `## Hook (20s)`, with the seconds in brackets.
- **The preflight says the port is busy.** An old copy of your app is still running. Stop it, or change `PORT` in `preflight.py` to the port your demo uses.
- **The preflight warns that `ffprobe` is missing.** Install `ffmpeg`, or check the video length by playing it.
- **The seed check says NO.** The file was edited, or `seed_data.py` changed. Run `python3 seed_data.py` again.

## Frequently asked questions

**How long should an AI hackathon demo be?**

Use the length your event gives you. Many events publish a slot, so read the rules. In this test the script took 148 seconds at an assumed 130 words a minute and fit a 180-second slot, but it failed a 120-second slot by 28 seconds.

**Should I record a backup video for an AI hackathon?**

Yes. The preflight check failed when the backup video was missing, so the check treats it as a required item. The video is what you play if the network or the app fails. Record it before demo day and check that it plays to the end.

**What test data should I use in a hackathon demo?**

Fixed, made-up data that you generate with a seed, so it is the same every time. Include edge cases on purpose. Here that was an empty body, a French ticket, an emoji and a very long text. Do not use real customer data.

## What to try next

- Add a check to `preflight.py` for the API key your demo needs, without printing it.
- Time yourself reading each beat and pass your real rate with `--wpm`.
- Rehearse in front of one other person and write down the first question they ask.

## How this tutorial was tested

- Date: 11 November 2026. Python 3.14.6 on macOS. `ffmpeg` was used for the stand-in video only.
- The code in this article is copied from the project files by a script. The command output comes from saved logs of real runs.
- Every step was run from a clean folder, then replayed from an empty copy of the folder with no generated data. The replay passed.
- The rehearsal times in Step 5 are example numbers typed in by us, not a measured rehearsal. The 130 words a minute rate is an assumption.
- The backup video is a three-second test pattern, not a recording of a demo. No screen recording was made.
- Terminal screenshots are rendered from the saved output of the run. They are not captures of a terminal window.
- Not run: Windows, Linux, other Python versions, and the Ticket Triage Assistant app itself, which is only the example story. No event's own rules were checked.
