# Demo script: Ticket Triage Assistant

Slot: 3 minutes. Speak at a steady pace and leave the last 10 seconds free.

## Hook (20s)
Every support team has the same Monday morning: forty new tickets and no idea which one is on fire. We built Ticket Triage Assistant so the urgent ones come to the top in seconds, before anyone has finished their coffee.
> On screen: the empty inbox, then the ticket list loading.

## The problem (30s)
Right now a person reads every ticket, guesses the priority and moves it by hand. A billing error and a question about dark mode look exactly the same in the queue. The slow part is not fixing the issue. It is finding the issue that matters, and while someone searches, the angry customer waits.
> On screen: two tickets side by side, same colour.

## Live demo (80s)
I will load our sample data now. There are twelve tickets, and I will not touch anything else. Watch the priority column fill in. The first ticket is a customer who was charged twice, and it is marked high. The next one is a question about changing a colour theme, and it is marked low. This ticket is written in French, and the assistant still reads it correctly. This one has an empty body, and instead of crashing it asks the customer for more detail. This one is very long, and it still fits on the screen. Now I sort by priority, and the three urgent tickets sit at the top. A support lead can start right there and ignore the noise.
> On screen: load sample data, priority column fills in, sort by priority.

## How it works (25s)
Each ticket goes to a language model with a short instruction and a fixed list of labels. The reply is checked against that list before we show it, so a strange answer never reaches the screen. If the model is slow, the ticket stays in a waiting state and the rest of the list keeps working.
> On screen: the architecture slide with three boxes.

## Result and next step (25s)
On our twelve sample tickets, the urgent ones were found in the first three rows. That is a small test, and we say so. Next we want to connect a real inbox and measure it on a week of tickets. Thank you, and we are happy to take questions.
> On screen: the sorted list and the team name.
