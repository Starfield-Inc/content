import argparse
import html
import json
from datetime import date
from pathlib import Path

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>My AI news digest</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 42rem; margin: 2rem auto; padding: 0 1rem; color: #1b1f24; line-height: 1.5; }}
h1 {{ font-size: 1.6rem; margin-bottom: 0.2rem; }}
.meta {{ color: #5a6370; margin-top: 0; }}
article {{ border-top: 1px solid #d8dde3; padding: 0.9rem 0; }}
article h2 {{ font-size: 1.05rem; margin: 0 0 0.3rem; }}
article p {{ margin: 0 0 0.4rem; }}
.src {{ font-size: 0.9rem; color: #5a6370; }}
a {{ color: #0b57d0; }}
</style></head><body>
<h1>My AI news digest</h1>
<p class="meta">{when} - {count} items, summaries written by {model}</p>
{items}
</body></html>
"""


def render_html(items: list[dict], when: str, model: str) -> str:
    cards = "\n".join(
        f'<article><h2>{html.escape(i["title"])}</h2><p>{html.escape(i["summary"])}</p>'
        f'<p class="src">Source: {html.escape(i["source"])} - '
        f'<a href="{html.escape(i["link"], quote=True)}">read the original</a></p></article>'
        for i in items
    )
    return PAGE.format(when=when, count=len(items), model=html.escape(model), items=cards)


def render_markdown(items: list[dict], when: str) -> str:
    lines = [f"# My AI news digest - {when}", ""]
    for i in items:
        lines += [f"## {i['title']}", i["summary"], f"Source: {i['source']} - {i['link']}", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("--html", default="digest.html")
    parser.add_argument("--md", default="digest.md")
    parser.add_argument("--when", default=date.today().isoformat())
    parser.add_argument("--model", default="claude-haiku-5-5")
    args = parser.parse_args()

    items = json.loads(Path(args.infile).read_text())
    Path(args.html).write_text(render_html(items, args.when, args.model), encoding="utf-8")
    Path(args.md).write_text(render_markdown(items, args.when), encoding="utf-8")
    print(f"Wrote {args.html} and {args.md} with {len(items)} items")


if __name__ == "__main__":
    main()
