# Git workflow for a hackathon team

A local sandbox where two teammates, Alice and Bob, share a project through a bare repository that stands in for GitHub. It runs real `git` and needs no account and no network. You create a conflict on purpose and resolve it.

| File | What it does |
| --- | --- |
| `template/app.py` | The tiny starter program the team shares |
| `template/.gitignore` | Keeps keys and local files out of git |
| `template/PULL_REQUEST_TEMPLATE.md` | The PR description template |
| `pr_body.sh` | Fills the template's change list from your commits |
| `steps.json` | Every command in the tutorial, in order |

Run all steps (from the Starfield Labs tutorial repo, which has the runner):

```bash
python3 .claude/skills/tutorial-build/scripts/run_steps.py labs-tutorials/git-github-team-workflow
```

Or follow `article.md` by hand. The sandbox is created in `sandbox/` and deleted by step 2 when you run it again.

Pull requests need a GitHub account and are explained in the article only. They were not run.
