"""List new models from chosen Hugging Face organisations and send a message about them."""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from filters import CHOSEN, in_window
from hfapi import RateLimited, newest_models


def read_orgs(path):
    lines = Path(path).read_text().splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def load_seen(path):
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else {}


def save_seen(path, seen):
    tmp = f"{path}.tmp"
    Path(tmp).write_text(json.dumps(seen, indent=2, sort_keys=True))
    os.replace(tmp, path)


def licence(model):
    return next((t.split(":", 1)[1] for t in model["tags"] if t.startswith("license:")), "none")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orgs", nargs="*", help="organisations; default is orgs.txt")
    ap.add_argument("--days", type=int, default=45)
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--state", default="seen.json")
    ap.add_argument("--message-file", default="alerts.txt")
    ap.add_argument("--keep-copies", action="store_true", help="do not drop models built on another author's model")
    args = ap.parse_args()

    orgs = args.orgs or read_orgs("orgs.txt")
    now = datetime.now(timezone.utc)
    since = (now - timedelta(days=args.days)).date()
    print(f"Checking {len(orgs)} organisations for models created since {since} ({args.days} days)")

    seen, new, left, bad = load_seen(args.state), [], None, []
    try:
        for org in orgs:
            models, left = newest_models(org, args.limit)
            if not models:
                bad.append(org)
                print(f"  {org}: no models found. Check the spelling, names are case sensitive.")
                continue
            recent = [m for m in models if in_window(m, args.days, now)]
            kept = recent if args.keep_copies else [m for m in recent if not CHOSEN(m, org)]
            fresh = [m for m in kept if m["id"] not in seen]
            note = "  (limit reached, raise --limit)" if len(recent) == len(models) else ""
            print(f"  {org}: {len(models)} fetched, {len(recent)} in the date range, "
                  f"{len(recent) - len(kept)} dropped as copies, {len(fresh)} not seen before{note}")
            new += fresh
    except RateLimited as err:
        print(err)
        return 3

    if bad:
        return 2

    new.sort(key=lambda m: m["createdAt"], reverse=True)
    if new:
        lines = [f"[{now:%Y-%m-%d %H:%M} UTC] {len(new)} new model(s) on Hugging Face"]
        for m in new:
            lines.append(f"  {m['createdAt'][:10]}  {m['id']}  licence: {licence(m)}  https://huggingface.co/{m['id']}")
        message = "\n".join(lines)
        with open(args.message_file, "a") as out:
            out.write(message + "\n")
        for m in new:
            seen[m["id"]] = m["createdAt"]
        save_seen(args.state, seen)
        print("\n" + message)
    else:
        print("\nNo new models since the last run.")
    print(f"\nAPI calls left in this window: {left}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
