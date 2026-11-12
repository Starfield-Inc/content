# Hackathon demo script and checklist

Small tools to prepare a three-minute hackathon demo: a timed script, seeded test data, a rehearsal comparison and a preflight check. Standard library only.

| File | What it does |
| --- | --- |
| `demo_script.md` | The three-minute story, in beats with time budgets |
| `check_script.py` | Estimates speaking time per beat from the word count |
| `seed_data.py` | Writes the same 12 made-up tickets every time (`--check` verifies them) |
| `rehearse.py` | Compares your stopwatch times with the plan |
| `preflight.py` | Checks data, backup video, port, disk and network |
| `checklist.md` | The manual checklist for demo day |

Run:

```bash
python3 seed_data.py
python3 check_script.py demo_script.md
python3 rehearse.py demo_script.md --times 22,27,64,27,24
python3 preflight.py
```

The rehearsal times above are example numbers, not a measured run. `preflight.py` needs `backup/demo-backup.mp4`. Record your own demo and save it there. `ffmpeg` is optional and only used in the tutorial to make a stand-in file.
