# Starfield Labs content

Working code, saved output and written pieces from Starfield Labs.

- `tutorials/` holds the tutorials. Each folder is one tutorial: a small project you can run, the article that explains it, and the evidence (real command output and screenshots) from running each step.
- `articles/` holds the articles as Markdown, each with a dark cover (`<name>.png`) and a light cover (`<name>.light.png`). The front matter at the top of each file has the title, summary and publish date.

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

| Tutorial | Folder | Notes |
| --- | --- | --- |
| TT-012 Count tokens in your text with a tokenizer library | `tutorials/count-tokens-python/` | - |
| TT-024 Remove duplicate stories from many news feeds | `tutorials/news-dedupe/` | - |
| TT-001 Set up a hackathon project repo in 30 minutes | `tutorials/hackathon-repo-setup/` | Not run: push, other operating systems |
| TT-021 Build a model price table from public price lists | `tutorials/model-price-table/` | Prices change; check the vendor price page before relying on them |
| TT-020 Get an alert when a new model appears on Hugging Face | `tutorials/hf-new-model-alert/` | Chat webhook and scheduling explained, not run |
| TT-023 Check a model's licence with a script and a checklist | `tutorials/model-licence-check/` | A checklist, not legal advice |
| TT-031 Test an MCP server with a client before you trust it | `tutorials/mcp-server-test/` | Inspector and other transports not run |
| TT-002 Build a hackathon demo chatbot with an LLM API in an afternoon | `tutorials/hackathon-demo-chatbot/` | Page Send button not driven in a browser |
| TT-010 Build a chatbot that remembers the conversation in Python | `tutorials/chatbot-memory-python/` | - |
| TT-014 Classify customer reviews with an LLM and check it on 50 examples | `tutorials/classify-reviews-llm/` | Labels are our own judgement |
| TT-017 Write prompts as tests: build a tiny prompt test file | `tutorials/prompt-tests/` | - |
| TT-007 Build a hackathon app that compares two models side by side | `tutorials/compare-two-models/` | Two Claude models only |
| TT-018 Compare zero-shot and few-shot prompting | `tutorials/zero-vs-few-shot/` | Scores depend on our own labelling rule |
| TT-003 Add streaming so your hackathon demo feels fast | `tutorials/stream-llm-answers/` | Button clicks and live route not in the saved evidence |
| TT-005 Keep your hackathon demo working when the API rate limit hits | `tutorials/api-rate-limit-fallback/` | A real 429 from the live API was not run |
| TT-004 Write a hackathon README that judges will read | `tutorials/hackathon-readme/` | Checklist limits are our own. Rubric example not checked |
| TT-008 Prepare a hackathon demo script and test data so nothing breaks | `tutorials/hackathon-demo-script/` | Rehearsal times and backup video are examples, not real recordings |
| TT-009 Make a hackathon pitch deck from your repo in five slides | `tutorials/hackathon-pitch-deck/` | PowerPoint and PDF export not run |
| TT-011 Call an LLM from JavaScript and show the answer on a web page | `tutorials/llm-javascript-web-page/` | Keep API keys on a server, not in browser code |
| TT-013 Turn text into embeddings and find similar sentences | `tutorials/embeddings-search-python/` | Runs a local model, no key. Check the model licence before reuse |
| TT-019 Build a personal AI news digest from RSS feeds with an LLM | `tutorials/ai-news-digest/` | Live feed counts change daily. Check each feed's terms of use |
| TT-022 Test a new model with your own 20 questions | `tutorials/test-new-model-20-questions/` | Prices copied from compare-two-models, not re-checked. One run per model |
| TT-025 Summarise a long article with an LLM without losing the numbers | `tutorials/summarize-keep-numbers/` | Kept-number counts varied between runs. Checker misses number words |
| TT-027 Check an AI summary against its source with a second pass | `tutorials/check-summary-python/` | One false alarm and one miss shown. Results vary, not a catch rate |
| TT-029 Build a streaming chat page in Next.js | `tutorials/nextjs-streaming-chat/` | Not run: dev server, Try again click, mid-stream failure |
| TT-030 Build an agent that answers questions about a code repo | `tutorials/repo-qa-agent-python/` | Prompt injection not tested |
| TT-032 Validate LLM JSON output with a schema in Python | `tutorials/validate-llm-json-python/` | Counts vary between runs |
| TT-034 Cache LLM answers to cut repeat costs | `tutorials/cache-llm-answers-python/` | Temperature step replayed on its own. Cache file holds prompts in plain text |
| TT-035 Write an evaluation script with 20 test cases for your LLM app | `tutorials/eval-llm-app-python/` | One case still fails by design. Replies differ word for word between runs |
| TT-036 Add rate limiting and a spending cap to an LLM endpoint | `tutorials/llm-endpoint-limits-python/` | Example prices are assumptions |

The notes list limits of what was tested. Model replies differ between runs, so counts and scores you get will differ from the saved evidence.

## Licences

Code and text in this repository are under the [MIT licence](LICENSE). Tutorials that download or use embedding or other models (for example `embeddings-search-python/`) use those models under their own licences. Check the folder's README and the model's page before you reuse it. Data fetched from third-party sites, such as RSS feeds or the Hugging Face API, stays under those sites' terms.

## Covers

`_covers/` holds the scripts that render each tutorial's cover images. See `_covers/render_covers.py`; it needs Chrome and a `tutorials.csv` file (set `TUTORIALS_CSV`).

## Articles

30 articles are in [`articles/`](articles/). Each is one Markdown file with its cover images beside it.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
