# Starfield Labs content

Working code, saved output and written pieces from Starfield Labs.

- `tutorials/` holds the tutorials. Each folder is one tutorial: a small project you can run, the article that explains it, and the evidence (real command output and screenshots) from running each step.
- `articles/` holds the articles as Markdown, most with a dark cover (`<name>.png`) and a light cover (`<name>.light.png`). The front matter at the top of each file has the title, summary and publish date.

## What is in a tutorial folder

| Item | Purpose |
| --- | --- |
| `README.md` | Files in the project and the commands to run it |
| `article.md` | The finished tutorial, with `images/` |
| `article.src.md` | The article source, before images and output are inserted |
| `evidence/` | Logs and screenshots saved when each step was run |
| `steps.json` | The steps used to replay the tutorial |
| `.env.example` | The environment variables the project reads |

## Run a tutorial

```bash
cd tutorials/count-tokens-python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Tutorials that call an LLM API also need a key:
cp .env.example .env     # then put your API key in .env
set -a; source .env; set +a
```

Then run the commands listed in that folder's `README.md`. Node.js tutorials (`tutorials/llm-javascript-web-page/`, `tutorials/nextjs-streaming-chat/`) use `npm install` instead. Most demos use a small, cheap model set in `TUTORIAL_MODEL`. Each run is short, but API calls can cost money, so check your provider's prices. Never commit `.env`.

## Tutorials

A few of the tutorials. Each links to its folder.

| Tutorial | Notes |
| --- | --- |
| [TT-012 Count tokens in your text with a tokenizer library](tutorials/count-tokens-python/) | - |
| [TT-001 Set up a hackathon project repo in 30 minutes](tutorials/hackathon-repo-setup/) | Not run: push, other operating systems |
| [TT-002 Build a hackathon demo chatbot with an LLM API in an afternoon](tutorials/hackathon-demo-chatbot/) | Page Send button not driven in a browser |
| [TT-035 Write an evaluation script with 20 test cases for your LLM app](tutorials/eval-llm-app-python/) | One case still fails by design. Replies differ word for word between runs |
| [RB-005 Set up Jupyter in a virtual environment and run a notebook headless](tutorials/jupyter-notebook-setup-python/) | Browser notebook page not driven |
| [RB-017 Build a summariser command-line tool in Python with Claude](tutorials/claude-summarizer-cli-python/) | Tested on two short made-up texts |
| [RB-025 Build a draft helper with a safety layer (Flask and Claude)](tutorials/safe-writing-assistant-app/) | One prompt-injection draft tested |
| [RB-031 Answer questions from your own notes with Chroma and Claude](tutorials/chroma-knowledge-base-chatbot/) | Local embedding model, about 79 MB download |
| [RB-034 Git workflow for a hackathon team](tutorials/git-github-team-workflow/) | Local bare repo stands in for GitHub. Pull requests not run |
| [RB-035 Build a personal assistant with LangChain and Claude in Python](tutorials/langchain-claude-assistant-python/) | In-memory memory only |

**[Read more: all 97 tutorials →](tutorials/README.md)**

The notes list limits of what was tested. Model replies differ between runs, so counts and scores you get will differ from the saved evidence.

## Licences

Code and text in this repository are under the [MIT licence](LICENSE). Tutorials that download or use embedding or other models (for example `embeddings-search-python/`) use those models under their own licences. Check the folder's README and the model's page before you reuse it. Data fetched from third-party sites, such as RSS feeds or the Hugging Face API, stays under those sites' terms.

## Layout

`_covers/` holds the scripts that render cover images. They need Chrome and a `tutorials.csv` file (set `TUTORIALS_CSV`).

## Articles

43 articles are in [`articles/`](articles/). Each is one Markdown file. The first 30 have cover images beside them; the rest do not have covers yet.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
