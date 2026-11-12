"""Render a README to site/index.html so you can see it the way a judge's browser does.

Usage: python render_readme.py path/to/README.md
Local images next to the README are copied into site/.
"""
import shutil
import sys
from pathlib import Path

import markdown

CSS = """body{font:16px/1.55 -apple-system,Helvetica,Arial,sans-serif;max-width:760px;margin:24px auto;padding:0 20px;color:#1f2328}
h1,h2{border-bottom:1px solid #d8dee4;padding-bottom:.3em}pre{background:#f6f8fa;padding:12px;border-radius:6px;overflow:auto}
code{background:#f6f8fa;padding:2px 4px;border-radius:4px}img{max-width:100%;border:1px solid #d8dee4;border-radius:6px}"""


def main():
    src = Path(sys.argv[1])
    out = Path("site")
    out.mkdir(exist_ok=True)
    for f in src.parent.iterdir():
        if f.suffix.lower() in (".png", ".jpg", ".gif"):
            shutil.copy(f, out / f.name)
    body = markdown.markdown(src.read_text(encoding="utf-8"), extensions=["fenced_code"])
    (out / "index.html").write_text(
        f"<!doctype html><meta charset=utf-8><title>README</title><style>{CSS}</style>{body}", encoding="utf-8")
    print(f"Wrote {out / 'index.html'}")


if __name__ == "__main__":
    main()
