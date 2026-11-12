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
| RB-001 Gemini CLI vs Claude Code: which tool fits which task | `tutorials/gemini-cli-vs-claude-code/` | Text only, not re-run. Tool paths, flags and model names may be out of date |
| RB-005 Set up Jupyter in a virtual environment and run a notebook headless | `tutorials/jupyter-notebook-setup-python/` | Browser notebook page not driven |
| RB-006 OpenClaw AI agent tutorial: autonomous wallets on Base and Solana, part 1 | `tutorials/openclaw-agent-wallets-part-one/` | Text only, not re-run. Needs wallets and accounts. Use test funds only |
| RB-007 OpenClaw and Moltbook: setup and integration | `tutorials/openclaw-moltbook-memory/` | Text only, not re-run |
| RB-008 Set up the Google Workspace CLI package for AI agents | `tutorials/google-workspace-cli-agent/` | Text only, not re-run. Needs a Google account |
| RB-010 Set up Python in VS Code and make your first Claude call | `tutorials/python-vscode-first-project/` | Partial. Editor window steps described, not run |
| RB-017 Build a summariser command-line tool in Python with Claude | `tutorials/claude-summarizer-cli-python/` | Tested on two short made-up texts |
| RB-018 Host an LLM on an AMD GPU in the cloud | `tutorials/vllm-amd-cloud-llm-host/` | Text only, not re-run. Needs a cloud GPU. Prices may be out of date |
| RB-021 Using agent harnesses for AI hackathons with Claude Code | `tutorials/claude-code-agent-harness/` | Text only, not re-run. Cost figures may be out of date |
| RB-025 Build a draft helper with a safety layer (Flask and Claude) | `tutorials/safe-writing-assistant-app/` | One prompt-injection draft tested |
| RB-031 Answer questions from your own notes with Chroma and Claude | `tutorials/chroma-knowledge-base-chatbot/` | Local embedding model, about 79 MB download |
| RB-032 Build a three-role agent pipeline with CrewAI | `tutorials/multi-agent-crew-python/` | Python 3.11 used. Python 3.14 is not supported by CrewAI. Large install |
| RB-034 Git workflow for a hackathon team | `tutorials/git-github-team-workflow/` | Local bare repo stands in for GitHub. Pull requests not run |
| RB-035 Build a personal assistant with LangChain and Claude in Python | `tutorials/langchain-claude-assistant-python/` | In-memory memory only |
| RB-037 Build a rulebook Q&A assistant in Python that cites its sources | `tutorials/legal-qa-assistant-python/` | Invented rulebook. Not legal advice |
| RB-044 Pay-per-call LLM API with Circle USDC nano payments | `tutorials/circle-gateway-nanopayments/` | Text only, not re-run. Needs a wallet. Use test funds only |
| RB-063 Mastering AI Agent Management with AgentOps: An In-Depth Guide | `tutorials/agentops-multi-agent-monitoring/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-048 AI21 Labs tutorial: How to use the Playground | `tutorials/ai21-playground-guide/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-049 Comprehensive Guide to AI71's API Hub | `tutorials/ai71-falcon-api-guide/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-009 Getting Started with Arc Testnet: Send USDC with ethers.js for AI Hackathons | `tutorials/arc-usdc-ethersjs/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-072 Getting Started with Aria: A Beginner's Guide to Rhymes AI's Multimodal API for AI Hackathons | `tutorials/aria-multimodal-api/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-020 Audiocraft tutorial: How to create music with Audiocraft | `tutorials/audiocraft-musicgen-streamlit/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-033 AutoGPT tutorial: How to set up AutoGPT | `tutorials/autogpt-local-setup/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-065 AutoGPT Tutorial: Building an AI Agent-Powered Research Assistant App | `tutorials/autogpt-research-assistant-app/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-041 ChatGPT tutorial: How to integrate ChatGPT and Whisper API into your project | `tutorials/chat-completions-whisper-api/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-058 ChatGPT Plugin Tutorial: How to build ChatGPT Plugin for image generation using Stable Diffusion | `tutorials/chatgpt-plugin-image-flask/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-053 ChatGPT tutorial: How to create a website with ChatGPT | `tutorials/chatgpt-portfolio-website/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-028 Chirp Tutorial: How to use Google's Chirp speech-to-text AI model on Google Cloud console | `tutorials/chirp-speech-to-text-gcp/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-064 Stable Diffusion Tutorial: How to bring book characters to live with Stable Diffusion | `tutorials/chroma-stable-diffusion-search/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-054 Anthropic tutorial: how to create a 100 000 token context AI chatbot | `tutorials/claude-100k-chatbot-python/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-046 Cohere tutorial: How to use Cohere Playground | `tutorials/cohere-playground-basics/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-052 Leveraging Composio for Advanced Multi-Agent AI Applications | `tutorials/composio-autogen-agents/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-066 Building an Intelligent AI Agent for Content Moderation with Structured Output | `tutorials/content-moderation-agent-python/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-045 Craiyon tutorial: text-to-image generation prompt guide | `tutorials/craiyon-prompt-guide/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-056 Developing Intelligent Agents with CrewAI | `tutorials/crewai-intelligent-agents/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-024 Stable Diffusion tutorial: how to create video with text prompts | `tutorials/deforum-video-from-prompts/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-038 ElevenLabs Tutorial: Building AI-Powered Auto Dubbing Service | `tutorials/elevenlabs-auto-dubbing-streamlit/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-073 ElevenLabs Tutorial: Building Simple Word Spelling App | `tutorials/elevenlabs-spelling-app-streamlit/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-050 Building an AI-Powered Personal Health Dashboard with Falcon 180B | `tutorials/falcon-health-dashboard-fastapi/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-071 Falcon LLMs: In-depth Tutorial. | `tutorials/falcon-llm-colab-guide/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-003 Building Real-Time Voice Agents for AI Hackathons: Gemini Live API Guide | `tutorials/gemini-live-voice-agent/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-015 Exploring the Power of Google AI Studio: A Comprehensive Guide | `tutorials/google-ai-studio-guide/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-016 Getting Started with xAI's Grok API: Your First AI Integration for AI Hackathons | `tutorials/grok-api-beginner/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-011 Google Colab tutorial: How to create your own AI image generator | `tutorials/image-generator-colab/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-002 KoboldAI Tutorial: Using Free and Open Source AI Models to Craft Fun and Quirky Stories | `tutorials/koboldai-story-writing-colab/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-030 Stable Diffusion tutorial: How to use Lexica, the Stable Diffusion AI art image search engine | `tutorials/lexica-image-search-api/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-067 Best Practices for Deploying AI Agents with the Llama Stack for AI Hackathons | `tutorials/llama-stack-local-agents/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-036 Unlocking LLaMA 3 with Ollama: A Beginner's Guide | `tutorials/llama3-ollama-python/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-012 Mastering Multilingual Translations with LLaMA 3.1 | `tutorials/llama31-multilingual-translator/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-004 ElevenLabs Tutorial: Adding a Witty Narrator into Minecraft via a Simple Mod | `tutorials/minecraft-ai-narrator-mod/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-070 Creating Your Advanced AI Companion for MongoDB Management | `tutorials/mongodb-atlas-llm-agent/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-043 OpenAI Codex tutorial: Natural language to SQL query with OpenAI Codex | `tutorials/nl-to-sql-codex/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-019 Building Efficient AI Models with OpenAI's Model Distillation for AI Hackathons: A Comprehensive Guide | `tutorials/openai-model-distillation-guide/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-027 OpenAI's Swarm: A Deep Dive into Multi-Agent Orchestration for Everyone | `tutorials/openai-swarm-multi-agent-guide/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-075 PaLM2 Tutorial: Create your own AI-powered Virtual Assistant | `tutorials/palm2-text-bison-intro/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-061 ElevenLabs Tutorial: How to Build your own Podcast Generation app | `tutorials/podcast-generator-elevenlabs-streamlit/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-051 Stable Diffusion tutorial: How to make an AI art with QR code | `tutorials/qr-code-ai-art-diffusion/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-022 Shape-E Tutorial: how to set up and use Shap-E model | `tutorials/shap-e-text-to-3d/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-074 Stable Diffusion tutorial: Text-guided image-to-image generation with Stable Diffusion | `tutorials/stable-diffusion-img2img-diffusers/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-040 Stable Diffusion tutorial: Prompt Inpainting with Stable Diffusion | `tutorials/stable-diffusion-inpainting-python/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-057 Stable Diffusion prompt tutorial: Basics of prompt engineering for Stable Diffusion | `tutorials/stable-diffusion-prompt-basics/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-026 Fine-Tuning TinyLLaMA with Unsloth | `tutorials/tinyllama-finetune-unsloth/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-047 Vectara Hackathon Guide | `tutorials/vectara-rag-quickstart/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-023 OpenAI Whisper tutorial: Creating OpenAI Whisper API in a Docker Container | `tutorials/whisper-api-docker-flask/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-014 OpenAI Whisper tutorial: how to create speaker identification app | `tutorials/whisper-speaker-diarization/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-076 OpenAI Whisper tutorial: How to use Whisper to transcribe a YouTube video | `tutorials/whisper-transcribe-youtube/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| RB-055 OpenAI Whisper tutorial: How to use OpenAI Whisper | `tutorials/whisper-transcription-notebook/` | Text only, not re-run. Details such as versions, prices and APIs may be out of date |

`_covers/` holds the scripts that render each tutorial's cover images. See `_covers/render_covers.py`; it needs Chrome and a `tutorials.csv` file (set `TUTORIALS_CSV`).

## Articles

43 articles are in [`articles/`](articles/). Each is one Markdown file. The first 30 have cover images beside them; the rest do not have covers yet.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
