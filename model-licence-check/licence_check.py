"""Pull a model's licence field, fetch its licence file, run the checklist and save a short report."""
import argparse
import hashlib
import sys
import textwrap
from pathlib import Path

from checklist import CHECKLIST, run_checklist
from hfapi import NotFound, model_info, raw_file

NOTE = ("This report marks lines of licence text for a person to read. It is not legal advice and it does not say "
        "whether you may use a model. Get a lawyer's view before you rely on a licence.")
SHOW = 2      # lines shown per question
WIDTH = 260   # characters per line


def read_models(path):
    lines = Path(path).read_text().splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def licence_fields(info):
    """The licence tag, plus the name and link the model card may give."""
    tag = next((t.split(":", 1)[1] for t in info.get("tags", []) if t.startswith("license:")), "none")
    card = info.get("cardData") or {}
    files = [s["rfilename"] for s in info.get("siblings", []) if s["rfilename"].upper().startswith(("LICENSE", "LICENCE"))]
    return {"tag": tag, "name": card.get("license_name"), "link": card.get("license_link"), "files": files}


def short(line):
    return line if len(line) <= WIDTH else line[:WIDTH].rsplit(" ", 1)[0] + " ..."


def check_model(model_id):
    info = model_info(model_id)
    fields = licence_fields(info)
    text = raw_file(model_id, fields["files"][0]) if fields["files"] else ""
    return fields, text


def report_section(model_id, fields, text):
    out = [f"## {model_id}", "",
           f"- Licence tag: `{fields['tag']}`",
           f"- Licence name on the card: {fields['name'] or 'not given'}",
           f"- Licence link on the card: {fields['link'] or 'not given'}"]
    if not text:
        out += ["- Licence file: none found in this repository. Read the model card and any link above.", ""]
        return out
    digest = hashlib.sha256(text.encode()).hexdigest()[:12]
    out += [f"- Licence file: `{fields['files'][0]}`, {len(text.splitlines())} lines, {len(text)} characters, sha256 {digest}", ""]
    result = run_checklist(text)
    for key, question, _ in CHECKLIST:
        hits = result[key]
        out.append(f"**{question}**")
        if not hits:
            out.append("- No trigger phrase found. Silence is not permission: a person must decide what it means.")
        for line, phrases in hits[:SHOW]:
            out.append(f"- [{', '.join(phrases)}]")
            out += textwrap.wrap(short(line), 112, initial_indent="  ", subsequent_indent="  ")
        if len(hits) > SHOW:
            out.append(f"- ... {len(hits) - SHOW} more flagged lines in the licence file")
        out.append("")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", help="model ids; default is models.txt")
    ap.add_argument("--tags-only", action="store_true", help="print the licence fields and stop")
    ap.add_argument("--report", default="report.md")
    args = ap.parse_args()

    report = ["# Licence check report", "", NOTE, ""]
    for model_id in args.models or read_models("models.txt"):
        try:
            fields, text = check_model(model_id)
        except NotFound:
            print(f"{model_id}: not found, or not public. Check the spelling (publisher/name).")
            return 2
        if args.tags_only:
            print(f"{model_id}\n  tag: {fields['tag']}\n  name: {fields['name']}\n  link: {fields['link']}\n  files: {fields['files']}")
            continue
        counts = {k: len(v) for k, v in run_checklist(text).items()}
        print(f"{model_id}: tag {fields['tag']}, file {fields['files'][0] if fields['files'] else 'none'}")
        print("  flagged lines: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
        report += report_section(model_id, fields, text)
    if not args.tags_only:
        Path(args.report).write_text("\n".join(report) + "\n")
        print(f"\nSaved {args.report}. It is not legal advice: read the note at the top of the report.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
