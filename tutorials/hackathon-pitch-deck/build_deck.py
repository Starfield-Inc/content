import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

from anthropic import Anthropic

from readme_parts import WANTED, flow_of, split_sections, title_of

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 4000

PROMPT = """You turn a project README into text for a five-slide hackathon pitch.
Return only a JSON object, no other text, with these keys:
  "problem": one sentence of at most 20 words that states the problem
  "demo_caption": one sentence of at most 12 words about what the demo shows
  "how": a list of exactly 3 bullets, at most 8 words each
  "next": a list of exactly 3 bullets, at most 8 words each
  "team": a list with one string per person, in the form "Name - role"
  "notes": an object with keys problem, demo, how, next, team. Each value is
           what the speaker says on that slide, 25 to 40 words, first person plural.
Use only facts that are in the README. Do not add numbers or claims.

README sections:
"""


def ask_model(sections):
    client = Anthropic()
    body = "\n\n".join(f"## {name}\n{sections[name]}" for name in WANTED)
    response = client.messages.create(
        model=MODEL, max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": PROMPT + body}],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    return json.loads(text), response.usage


def slides_from(project, data, flow):
    return [
        {"id": "problem", "title": "The problem", "text": [data["problem"]], "notes": data["notes"]["problem"]},
        {"id": "demo", "title": "Demo", "text": [data["demo_caption"]], "image": "demo.png", "notes": data["notes"]["demo"]},
        {"id": "how", "title": "How it works", "text": data["how"], "flow": flow, "notes": data["notes"]["how"]},
        {"id": "next", "title": "What is next", "text": data["next"], "notes": data["notes"]["next"]},
        {"id": "team", "title": "Team", "text": data["team"], "notes": data["notes"]["team"]},
    ]


def flow_svg(flow):
    box_w, gap, h = 150, 34, 56
    width = len(flow) * box_w + (len(flow) - 1) * gap
    parts = [f'<svg viewBox="0 0 {width} {h}" class="flow" role="img" aria-label="{html.escape(" to ".join(flow))}">']
    for i, name in enumerate(flow):
        x = i * (box_w + gap)
        parts.append(f'<rect x="{x}" y="0" width="{box_w}" height="{h}" rx="8"/>')
        parts.append(f'<text x="{x + box_w / 2}" y="{h / 2 + 5}" text-anchor="middle">{html.escape(name)}</text>')
        if i < len(flow) - 1:
            ax = x + box_w + 4
            parts.append(f'<path d="M{ax} {h / 2} H{ax + gap - 12}" class="arrow"/>')
            parts.append(f'<path d="M{ax + gap - 16} {h / 2 - 6} L{ax + gap - 6} {h / 2} L{ax + gap - 16} {h / 2 + 6}" class="arrow"/>')
    parts.append("</svg>")
    return "".join(parts)


def slide_html(n, slide):
    items = "".join(f"<li>{html.escape(t)}</li>" for t in slide["text"])
    lead = f"<p class='lead'>{html.escape(slide['text'][0])}</p>" if len(slide["text"]) == 1 else f"<ul>{items}</ul>"
    extra = ""
    if "image" in slide:
        extra = f"<img src='{slide['image']}' alt='Terminal output of the demo run'>"
    if "flow" in slide:
        extra = flow_svg(slide["flow"])
    return (f"<section class='slide' id='slide-{n}'><span class='num'>{n} / 5</span>"
            f"<h2>{html.escape(slide['title'])}</h2>{lead}{extra}</section>")


CSS = """
:root{--bg:#10131a;--card:#1b2030;--ink:#f2f4f8;--muted:#a9b2c7;--accent:#7aa2ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.4 system-ui,sans-serif;padding:24px}
h1{font-size:22px;margin:0 0 16px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.slide{position:relative;aspect-ratio:16/9;background:var(--card);border-radius:12px;padding:28px 32px;overflow:hidden;display:flex;flex-direction:column}
.slide h2{margin:0 0 12px;font-size:26px;color:var(--accent)}
.num{position:absolute;right:20px;top:16px;color:var(--muted);font-size:13px}
.lead{font-size:22px;margin:0}
ul{margin:0;padding-left:22px;font-size:20px}li{margin:4px 0}
img{margin-top:12px;min-height:0;flex:1;object-fit:contain;object-position:left top;border-radius:8px}
.flow{margin-top:18px;width:100%}.flow rect{fill:none;stroke:var(--accent);stroke-width:2}
.flow text{fill:var(--ink);font-size:13px}.flow .arrow{stroke:var(--muted);stroke-width:2;fill:none}
"""


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        sys.exit("usage: python build_deck.py <repo folder> <demo image> [out folder]")
    project, demo = Path(sys.argv[1]), Path(sys.argv[2])
    out = Path(sys.argv[3] if len(sys.argv) == 4 else "deck")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")
    if not demo.is_file():
        sys.exit(f"Cannot find the demo image {demo}")

    readme = (project / "README.md").read_text()
    sections = split_sections(readme)
    data, usage = ask_model(sections)
    slides = slides_from(project, data, flow_of(sections["How it works"]))

    out.mkdir(exist_ok=True)
    shutil.copy(demo, out / "demo.png")
    (out / "deck.json").write_text(json.dumps({"title": title_of(readme), "slides": slides}, indent=2))
    page = "".join(slide_html(i, s) for i, s in enumerate(slides, 1))
    (out / "index.html").write_text(
        f"<!doctype html><meta charset='utf-8'><title>{html.escape(title_of(readme))} pitch</title>"
        f"<style>{CSS}</style><h1>{html.escape(title_of(readme))}: five-slide pitch</h1><div class='grid'>{page}</div>")
    print(f"Wrote {out}/index.html and {out}/deck.json with {len(slides)} slides")
    for i, s in enumerate(slides, 1):
        print(f"  {i}. {s['title']}: {s['text'][0]}")
    print(f"[model call: input tokens {usage.input_tokens}, output tokens {usage.output_tokens}]")


if __name__ == "__main__":
    main()
