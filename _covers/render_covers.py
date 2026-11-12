#!/usr/bin/env python3
"""Render dark and light covers for every tutorial in labs-tutorials/README.md.

Per tutorial it writes, into <folder>/images/:
  cover-dark.png, cover-light.png   1280x720
  card-dark.png,  card-light.png     640x360
  og.png                            1200x630, dark
Titles come from each article's H1, the level and one-line summary from
a tutorials.csv file (set TUTORIALS_CSV). Layout values come from the slug, so a rerun gives the same image.
Usage: python3 render_covers.py [--only folder ...]
"""
import csv, json, math, os, re, struct, subprocess, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TUT = ROOT / "tutorials"
CSV = Path(os.environ.get("TUTORIALS_CSV", HERE / "tutorials.csv"))
CHROME = os.environ.get("CHROME_BIN", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SIZES = {"cover": (1280, 720), "card": (640, 360), "og": (1200, 630)}
PILL_OVERRIDE = {"TT-004": "Markdown"}


def seeded(slug):
    h = 2166136261
    for ch in slug:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    def nxt():
        nonlocal h
        h = (h * 1664525 + 1013904223) & 0xFFFFFFFF
        return h / 4294967296
    return nxt


def tech(folder, tid):
    if tid in PILL_OVERRIDE:
        return PILL_OVERRIDE[tid]
    pj = TUT / folder / "package.json"
    if pj.exists():
        return "Next.js" if "next" in pj.read_text() else "JavaScript"
    return "Python"


def jobs(only):
    rows = {r["id"]: r for r in csv.DictReader(open(CSV))}
    out = []
    for m in re.finditer(r"^\| (TT-\d+) [^|]*\| `(?:tutorials/)?([^`]+)/`", (ROOT / "README.md").read_text(), re.M):
        tid, folder = m.groups()
        if only and folder not in only:
            continue
        h1 = re.search(r"^# (.+)$", (TUT / folder / "article.md").read_text(), re.M).group(1)
        r = seeded(folder)
        level = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}[rows[tid]["level"]]
        spec = dict(slug=folder, kind="Tutorial", title=h1, sub=rows[tid]["what_you_build"],
                    pills=[rows[tid]["level"], tech(folder, tid)], level=level,
                    sx=round(900 + r() * 130), sy=round(260 + r() * 180),
                    tilt=round(-22 + r() * 44), ang=round(r() * 2 * math.pi, 2))
        for kind, mode, name in (("cover", "dark", "cover-dark"), ("cover", "light", "cover-light"),
                                 ("card", "dark", "card-dark"), ("card", "light", "card-light"),
                                 ("og", "dark", "og")):
            out.append((folder, name, kind, dict(spec, mode=mode)))
    return out


def render(job):
    folder, name, kind, spec = job
    w, h = SIZES[kind]
    dest = TUT / folder / "images" / f"{name}.png"
    url = (HERE / "cover.html").as_uri() + "#" + urllib.parse.quote(json.dumps(spec))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", "--virtual-time-budget=8000",
                    f"--screenshot={dest}", url], capture_output=True, timeout=120)
    with open(dest, "rb") as fh:
        head = fh.read(24)
    got = struct.unpack(">II", head[16:24])
    ok = got == (w, h) and dest.stat().st_size > 3000
    return folder, name, ok, got


if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else []
    work = jobs(only)
    bad = []
    with ThreadPoolExecutor(4) as ex:
        for folder, name, ok, got in ex.map(render, work):
            if not ok:
                bad.append((folder, name, got))
    print(f"rendered {len(work)} images, {len(bad)} problems")
    for b in bad:
        print("PROBLEM", b)
    sys.exit(1 if bad else 0)
