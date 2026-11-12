import json
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from dedupe import group

PORT = 8011
STYLE = """
body{font:16px/1.5 system-ui,sans-serif;margin:0;background:#f4f6f9;color:#1c2430}
main{max-width:860px;margin:0 auto;padding:28px 20px}
h1{font-size:1.6rem;margin:0 0 4px} .sub{color:#566275;margin:0 0 22px}
.story{background:#fff;border:1px solid #d8dee7;border-radius:8px;padding:14px 16px;margin:0 0 12px}
.story h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:#1f5fbf;margin:0 0 8px}
.story a{display:block;color:#1c2430;text-decoration:none;margin:4px 0}
.story a span{display:inline-block;min-width:9em;color:#566275;font-size:.85rem}
.single a{margin:2px 0;font-size:.92rem}
"""


def page() -> str:
    items = json.loads(Path("items.json").read_text())
    groups = group(items)
    repeated = [g for g in groups if len(g) > 1]
    singles = [g[0] for g in groups if len(g) == 1]
    out = [f"<style>{STYLE}</style><main><h1>News without the repeats</h1>",
           f"<p class='sub'>{len(items)} items from {len({i['source'] for i in items})} feeds became {len(groups)} stories. "
           f"{len(repeated)} appear in more than one feed.</p>"]
    for g in repeated:
        links = "".join(f"<a href='{escape(i['link'])}'><span>{escape(i['source'])}</span>{escape(i['title'])}</a>" for i in g)
        out.append(f"<div class='story'><h2>Same story in {len(g)} feeds</h2>{links}</div>")
    out.append("<div class='story single'><h2>Everything else</h2>")
    out += [f"<a href='{escape(i['link'])}'><span>{escape(i['source'])}</span>{escape(i['title'])}</a>" for i in singles[:12]]
    out.append("</div></main>")
    return "".join(out)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = page().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"Open http://127.0.0.1:{PORT}/")
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
