"""Score saved answers against the accepted answers in questions.json. No model is involved.

The rule: normalise the reply, then it is correct only if it equals one of the accepted answers.
Normalising means: lower case, trim spaces, drop a final full stop, drop quotes, drop thousands commas."""
import json
import re
import sys


def normalise(text):
    text = text.strip().lower().strip("\"'`")
    text = text.rstrip(".").strip()
    return re.sub(r"(?<=\d),(?=\d{3})", "", text)


def is_correct(answer, accept):
    return normalise(answer) in {normalise(a) for a in accept}


def score(results_by_model, questions):
    """Return {model: {"correct": n, "marks": [bool, ...]}} for answers shaped like results.json."""
    out = {}
    for model, rows in results_by_model.items():
        marks = [is_correct(rows[str(q["id"])]["answer"], q["accept"]) for q in questions]
        out[model] = {"correct": sum(marks), "marks": marks}
    return out


def report(data, questions):
    models = list(data["models"])
    scores = score({m: data["models"][m]["answers"] for m in models}, questions)
    print(f"{'#':>2}  {'expected':<10}" + "".join(f"{data['models'][m]['label']:<28}" for m in models))
    for i, q in enumerate(questions):
        cells = ""
        for m in models:
            row = data["models"][m]["answers"][str(q["id"])]
            mark = "ok  " if scores[m]["marks"][i] else "MISS"
            cells += f"{mark} {row['answer'].strip()[:22]!r:<23}"
        print(f"{q['id']:>2}  {q['accept'][0]:<10}{cells}")
    print()
    for m in models:
        d = data["models"][m]
        print(f"{d['label']}: {scores[m]['correct']}/{len(questions)} correct, "
              f"{d['seconds']:.1f} seconds, {d['input_tokens']} input tokens, "
              f"{d['output_tokens']} output tokens, cost ${d['cost_usd']:.6f}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "results.json"
    try:
        data = json.load(open(path))
    except FileNotFoundError:
        sys.exit(f"Cannot find {path}. Run python run_eval.py first.")
    report(data, json.load(open("questions.json")))
