#!/usr/bin/env python3
"""Render covers for the site's seed pieces into a staging folder, one <slug>.png per piece.

Reads the headers of content/seed/{articles,tutorials}/*.md in a starfield-labs checkout (read only)
and writes to _covers/site/{articles,tutorials}/:
  <slug>.png        dark, 1280x720 (what the site's `cover:` header takes)
  <slug>.light.png  light, 1280x720 (kept for a future light-mode cover; the site has no field for it yet)
Usage: python3 render_seed_covers.py <path to a starfield-labs checkout with content/seed>
"""
import difflib, json, math, re, struct, sys, urllib.parse, subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from render_covers import CHROME, ROOT, TUT, HERE, seeded, tech

OUT = HERE / "site"


def header(md):
    head = md.split("---")[1]
    out = {}
    for line in head.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            v = m.group(2).strip()
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            out[m.group(1)] = v
    return out


def short_sub(summary):
    first = re.split(r"(?<=[.!?])\s", summary.strip())[0]
    return first if len(first) <= 95 else ""


def our_folder_tech():
    pairs = []
    for m in re.finditer(r"^\| (TT-\d+) [^|]*\| `(?:tutorials/)?([^`]+)/`", (ROOT / "README.md").read_text(), re.M):
        tid, folder = m.groups()
        h1 = re.search(r"^# (.+)$", (TUT / folder / "article.md").read_text(), re.M).group(1)
        pairs.append((h1.lower(), tech(folder, tid)))
    return pairs


def specs(checkout):
    techs = our_folder_tech()
    items, unmatched = [], []
    for kind in ("articles", "tutorials"):
        for md in sorted((checkout / "content/seed" / kind).glob("*.md")):
            h = header(md.read_text())
            slug = md.stem
            r = seeded(slug)
            spec = dict(slug=slug, title=h["title"], sub=short_sub(h.get("summary", "")),
                        sx=round(900 + r() * 130), sy=round(260 + r() * 180),
                        tilt=round(-22 + r() * 44), ang=round(r() * 2 * math.pi, 2))
            if kind == "tutorials":
                best = max(techs, key=lambda t: difflib.SequenceMatcher(None, t[0], h["title"].lower()).ratio())
                score = difflib.SequenceMatcher(None, best[0], h["title"].lower()).ratio()
                if score < .8:
                    unmatched.append((slug, round(score, 2)))
                level = h["level"].capitalize()
                spec.update(kind="Tutorial", pills=[level, best[1]], level={"Beginner": 1, "Intermediate": 2, "Advanced": 3}[level])
            else:
                spec.update(kind="Article", pills=[], level=1)
            items.append((kind, spec))
    return items, unmatched


def render(job):
    kind, spec, mode, name = job
    dest = OUT / kind / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = (HERE / "cover.html").as_uri() + "#" + urllib.parse.quote(json.dumps(dict(spec, mode=mode)))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1280,720",
                    "--virtual-time-budget=8000", f"--screenshot={dest}", url], capture_output=True, timeout=120)
    w, h = struct.unpack(">II", dest.read_bytes()[16:24])
    return dest, (w, h) == (1280, 720) and dest.stat().st_size > 3000


if __name__ == "__main__":
    items, unmatched = specs(Path(sys.argv[1]))
    jobs = [(k, s, "dark", f"{s['slug']}.png") for k, s in items] + [(k, s, "light", f"{s['slug']}.light.png") for k, s in items]
    with ThreadPoolExecutor(4) as ex:
        bad = [d for d, ok in ex.map(render, jobs) if not ok]
    print(f"{len(items)} pieces, {len(jobs)} images, {len(bad)} problems; tutorials with a weak title match: {unmatched}")
