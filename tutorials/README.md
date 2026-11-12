# Tutorials

Each folder is one tutorial: the written tutorial (`article.md`), and for the ones we ran, the project code, saved output and screenshots. See the [main README](../README.md) for how to run one.

TT rows were built and run step by step. RB rows are either built and run (notes say what ran) or text-only: those say "Text only, not re-run".

| Tutorial | Notes |
| --- | --- |
| [TT-001 Set up a hackathon project repo in 30 minutes](hackathon-repo-setup/) | Not run: push, other operating systems |
| [TT-002 Build a hackathon demo chatbot with an LLM API in an afternoon](hackathon-demo-chatbot/) | Page Send button not driven in a browser |
| [TT-003 Add streaming so your hackathon demo feels fast](stream-llm-answers/) | Button clicks and live route not in the saved evidence |
| [TT-004 Write a hackathon README that judges will read](hackathon-readme/) | Checklist limits are our own. Rubric example not checked |
| [TT-005 Keep your hackathon demo working when the API rate limit hits](api-rate-limit-fallback/) | A real 429 from the live API was not run |
| [TT-007 Build a hackathon app that compares two models side by side](compare-two-models/) | Two Claude models only |
| [TT-008 Prepare a hackathon demo script and test data so nothing breaks](hackathon-demo-script/) | Rehearsal times and backup video are examples, not real recordings |
| [TT-009 Make a hackathon pitch deck from your repo in five slides](hackathon-pitch-deck/) | PowerPoint and PDF export not run |
| [TT-010 Build a chatbot that remembers the conversation in Python](chatbot-memory-python/) | - |
| [TT-011 Call an LLM from JavaScript and show the answer on a web page](llm-javascript-web-page/) | Keep API keys on a server, not in browser code |
| [TT-012 Count tokens in your text with a tokenizer library](count-tokens-python/) | - |
| [TT-013 Turn text into embeddings and find similar sentences](embeddings-search-python/) | Runs a local model, no key. Check the model licence before reuse |
| [TT-014 Classify customer reviews with an LLM and check it on 50 examples](classify-reviews-llm/) | Labels are our own judgement |
| [TT-017 Write prompts as tests: build a tiny prompt test file](prompt-tests/) | - |
| [TT-018 Compare zero-shot and few-shot prompting](zero-vs-few-shot/) | Scores depend on our own labelling rule |
| [TT-019 Build a personal AI news digest from RSS feeds with an LLM](ai-news-digest/) | Live feed counts change daily. Check each feed's terms of use |
| [TT-020 Get an alert when a new model appears on Hugging Face](hf-new-model-alert/) | Chat webhook and scheduling explained, not run |
| [TT-021 Build a model price table from public price lists](model-price-table/) | Prices change; check the vendor price page before relying on them |
| [TT-022 Test a new model with your own 20 questions](test-new-model-20-questions/) | Prices copied from compare-two-models, not re-checked. One run per model |
| [TT-023 Check a model's licence with a script and a checklist](model-licence-check/) | A checklist, not legal advice |
| [TT-024 Remove duplicate stories from many news feeds](news-dedupe/) | - |
| [TT-025 Summarise a long article with an LLM without losing the numbers](summarize-keep-numbers/) | Kept-number counts varied between runs. Checker misses number words |
| [TT-027 Check an AI summary against its source with a second pass](check-summary-python/) | One false alarm and one miss shown. Results vary, not a catch rate |
| [TT-029 Build a streaming chat page in Next.js](nextjs-streaming-chat/) | Not run: dev server, Try again click, mid-stream failure |
| [TT-030 Build an agent that answers questions about a code repo](repo-qa-agent-python/) | Prompt injection not tested |
| [TT-031 Test an MCP server with a client before you trust it](mcp-server-test/) | Inspector and other transports not run |
| [TT-032 Validate LLM JSON output with a schema in Python](validate-llm-json-python/) | Counts vary between runs |
| [TT-034 Cache LLM answers to cut repeat costs](cache-llm-answers-python/) | Temperature step replayed on its own. Cache file holds prompts in plain text |
| [TT-035 Write an evaluation script with 20 test cases for your LLM app](eval-llm-app-python/) | One case still fails by design. Replies differ word for word between runs |
| [TT-036 Add rate limiting and a spending cap to an LLM endpoint](llm-endpoint-limits-python/) | Example prices are assumptions |
| [RB-001 Gemini CLI vs Claude Code: which tool fits which task](gemini-cli-vs-claude-code/) | Text only, not re-run. Tool paths, flags and model names may be out of date |
| [RB-002 KoboldAI Tutorial: Using Free and Open Source AI Models to Craft Fun and Quirky Stories](koboldai-story-writing-colab/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-003 Building Real-Time Voice Agents for AI Hackathons: Gemini Live API Guide](gemini-live-voice-agent/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-004 ElevenLabs Tutorial: Adding a Witty Narrator into Minecraft via a Simple Mod](minecraft-ai-narrator-mod/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-005 Set up Jupyter in a virtual environment and run a notebook headless](jupyter-notebook-setup-python/) | Browser notebook page not driven |
| [RB-006 OpenClaw AI agent tutorial: autonomous wallets on Base and Solana, part 1](openclaw-agent-wallets-part-one/) | Text only, not re-run. Needs wallets and accounts. Use test funds only |
| [RB-007 OpenClaw and Moltbook: setup and integration](openclaw-moltbook-memory/) | Text only, not re-run |
| [RB-008 Set up the Google Workspace CLI package for AI agents](google-workspace-cli-agent/) | Text only, not re-run. Needs a Google account |
| [RB-009 Getting Started with Arc Testnet: Send USDC with ethers.js for AI Hackathons](arc-usdc-ethersjs/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-010 Set up Python in VS Code and make your first Claude call](python-vscode-first-project/) | Partial. Editor window steps described, not run |
| [RB-011 Google Colab tutorial: How to create your own AI image generator](image-generator-colab/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-012 Mastering Multilingual Translations with LLaMA 3.1](llama31-multilingual-translator/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-014 OpenAI Whisper tutorial: how to create speaker identification app](whisper-speaker-diarization/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-015 Exploring the Power of Google AI Studio: A Comprehensive Guide](google-ai-studio-guide/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-016 Getting Started with xAI's Grok API: Your First AI Integration for AI Hackathons](grok-api-beginner/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-017 Build a summariser command-line tool in Python with Claude](claude-summarizer-cli-python/) | Tested on two short made-up texts |
| [RB-018 Host an LLM on an AMD GPU in the cloud](vllm-amd-cloud-llm-host/) | Text only, not re-run. Needs a cloud GPU. Prices may be out of date |
| [RB-019 Building Efficient AI Models with OpenAI's Model Distillation for AI Hackathons: A Comprehensive Guide](openai-model-distillation-guide/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-020 Audiocraft tutorial: How to create music with Audiocraft](audiocraft-musicgen-streamlit/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-021 Using agent harnesses for AI hackathons with Claude Code](claude-code-agent-harness/) | Text only, not re-run. Cost figures may be out of date |
| [RB-022 Shape-E Tutorial: how to set up and use Shap-E model](shap-e-text-to-3d/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-023 OpenAI Whisper tutorial: Creating OpenAI Whisper API in a Docker Container](whisper-api-docker-flask/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-024 Stable Diffusion tutorial: how to create video with text prompts](deforum-video-from-prompts/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-025 Build a draft helper with a safety layer (Flask and Claude)](safe-writing-assistant-app/) | One prompt-injection draft tested |
| [RB-026 Fine-Tuning TinyLLaMA with Unsloth](tinyllama-finetune-unsloth/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-027 OpenAI's Swarm: A Deep Dive into Multi-Agent Orchestration for Everyone](openai-swarm-multi-agent-guide/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-028 Chirp Tutorial: How to use Google's Chirp speech-to-text AI model on Google Cloud console](chirp-speech-to-text-gcp/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-030 Stable Diffusion tutorial: How to use Lexica, the Stable Diffusion AI art image search engine](lexica-image-search-api/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-031 Answer questions from your own notes with Chroma and Claude](chroma-knowledge-base-chatbot/) | Local embedding model, about 79 MB download |
| [RB-032 Build a three-role agent pipeline with CrewAI](multi-agent-crew-python/) | Python 3.11 used. Python 3.14 is not supported by CrewAI. Large install |
| [RB-033 AutoGPT tutorial: How to set up AutoGPT](autogpt-local-setup/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-034 Git workflow for a hackathon team](git-github-team-workflow/) | Local bare repo stands in for GitHub. Pull requests not run |
| [RB-035 Build a personal assistant with LangChain and Claude in Python](langchain-claude-assistant-python/) | In-memory memory only |
| [RB-036 Unlocking LLaMA 3 with Ollama: A Beginner's Guide](llama3-ollama-python/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-037 Build a rulebook Q&A assistant in Python that cites its sources](legal-qa-assistant-python/) | Invented rulebook. Not legal advice |
| [RB-038 ElevenLabs Tutorial: Building AI-Powered Auto Dubbing Service](elevenlabs-auto-dubbing-streamlit/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-040 Stable Diffusion tutorial: Prompt Inpainting with Stable Diffusion](stable-diffusion-inpainting-python/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-041 ChatGPT tutorial: How to integrate ChatGPT and Whisper API into your project](chat-completions-whisper-api/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-043 OpenAI Codex tutorial: Natural language to SQL query with OpenAI Codex](nl-to-sql-codex/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-044 Pay-per-call LLM API with Circle USDC nano payments](circle-gateway-nanopayments/) | Text only, not re-run. Needs a wallet. Use test funds only |
| [RB-045 Craiyon tutorial: text-to-image generation prompt guide](craiyon-prompt-guide/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-046 Cohere tutorial: How to use Cohere Playground](cohere-playground-basics/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-047 Vectara Hackathon Guide](vectara-rag-quickstart/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-048 AI21 Labs tutorial: How to use the Playground](ai21-playground-guide/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-049 Comprehensive Guide to AI71's API Hub](ai71-falcon-api-guide/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-050 Building an AI-Powered Personal Health Dashboard with Falcon 180B](falcon-health-dashboard-fastapi/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-051 Stable Diffusion tutorial: How to make an AI art with QR code](qr-code-ai-art-diffusion/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-052 Leveraging Composio for Advanced Multi-Agent AI Applications](composio-autogen-agents/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-053 ChatGPT tutorial: How to create a website with ChatGPT](chatgpt-portfolio-website/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-054 Anthropic tutorial: how to create a 100 000 token context AI chatbot](claude-100k-chatbot-python/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-055 OpenAI Whisper tutorial: How to use OpenAI Whisper](whisper-transcription-notebook/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-056 Developing Intelligent Agents with CrewAI](crewai-intelligent-agents/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-057 Stable Diffusion prompt tutorial: Basics of prompt engineering for Stable Diffusion](stable-diffusion-prompt-basics/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-058 ChatGPT Plugin Tutorial: How to build ChatGPT Plugin for image generation using Stable Diffusion](chatgpt-plugin-image-flask/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-061 ElevenLabs Tutorial: How to Build your own Podcast Generation app](podcast-generator-elevenlabs-streamlit/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-063 Mastering AI Agent Management with AgentOps: An In-Depth Guide](agentops-multi-agent-monitoring/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-064 Stable Diffusion Tutorial: How to bring book characters to live with Stable Diffusion](chroma-stable-diffusion-search/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-065 AutoGPT Tutorial: Building an AI Agent-Powered Research Assistant App](autogpt-research-assistant-app/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-066 Building an Intelligent AI Agent for Content Moderation with Structured Output](content-moderation-agent-python/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-067 Best Practices for Deploying AI Agents with the Llama Stack for AI Hackathons](llama-stack-local-agents/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-070 Creating Your Advanced AI Companion for MongoDB Management](mongodb-atlas-llm-agent/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-071 Falcon LLMs: In-depth Tutorial.](falcon-llm-colab-guide/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-072 Getting Started with Aria: A Beginner's Guide to Rhymes AI's Multimodal API for AI Hackathons](aria-multimodal-api/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-073 ElevenLabs Tutorial: Building Simple Word Spelling App](elevenlabs-spelling-app-streamlit/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-074 Stable Diffusion tutorial: Text-guided image-to-image generation with Stable Diffusion](stable-diffusion-img2img-diffusers/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-075 PaLM2 Tutorial: Create your own AI-powered Virtual Assistant](palm2-text-bison-intro/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
| [RB-076 OpenAI Whisper tutorial: How to use Whisper to transcribe a YouTube video](whisper-transcribe-youtube/) | Text only, not re-run. Details such as versions, prices and APIs may be out of date |
