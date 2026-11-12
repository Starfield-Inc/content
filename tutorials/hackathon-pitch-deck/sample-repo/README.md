# Action Catcher

Action Catcher reads the notes from a meeting and lists who agreed to do what.

## Problem

After a meeting, the notes hold the decisions, but the tasks are buried in the middle of sentences. People leave unsure who owns what, and the same meeting gets held again a week later. Action Catcher finds the lines where someone commits to a task and puts them in one short list.

## Demo

Run `python demo.py notes.txt` and it prints one line per task with the owner.

## How it works

Flow: Notes file -> Line splitter -> Commitment finder -> Owner list

The splitter cuts the notes into lines. The finder looks for a name followed by "will" or "to do". The list groups tasks by owner.

## What is next

- Read notes straight from a shared document
- Catch due dates such as "by Friday"
- Send each owner a reminder message

## Team

- Maya Ortiz - builds the finder
- Tomas Weber - writes the demo and the tests
- Priya Nair - designs the output and presents
