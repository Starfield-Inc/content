"""Load prices.csv, cost a usage you choose, print a table, flag old rows."""
import argparse
import csv
import sys
from datetime import date
from decimal import Decimal, InvalidOperation

COLUMNS = ["model", "input_per_mtok", "output_per_mtok", "source_url", "checked_on"]


def load_prices(path):
    """Read the CSV into a list of dicts with real numbers and a real date."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path}: missing column(s): {', '.join(missing)}")
        for n, row in enumerate(reader, start=2):  # line 1 is the header
            try:
                rows.append({
                    "model": row["model"].strip(),
                    "input": Decimal(row["input_per_mtok"]),
                    "output": Decimal(row["output_per_mtok"]),
                    "source_url": row["source_url"].strip(),
                    "checked_on": date.fromisoformat(row["checked_on"].strip()),
                })
            except InvalidOperation:
                raise ValueError(f"{path} line {n} ({row['model']}): a price is not a number: "
                                 f"{row['input_per_mtok']!r}, {row['output_per_mtok']!r}") from None
            except ValueError as err:
                raise ValueError(f"{path} line {n} ({row['model']}): {err}") from None
            if not rows[-1]["source_url"].startswith("https://"):
                raise ValueError(f"{path} line {n} ({row['model']}): source_url must start with https://")
    return rows


def cost(row, input_tokens, output_tokens):
    """Dollars for this usage. Prices are per million tokens."""
    million = Decimal(1_000_000)
    return row["input"] * Decimal(input_tokens) / million + row["output"] * Decimal(output_tokens) / million


def age_days(row, today):
    return (today - row["checked_on"]).days


def render(rows, input_tokens, output_tokens, max_age, today):
    lines = [f"Usage: {input_tokens:,} input tokens and {output_tokens:,} output tokens. Today: {today}.",
             f"{'Model':<46}{'In $/M':>8}{'Out $/M':>9}{'Cost $':>10}{'Checked':>12}{'Age':>5}  Flag"]
    for row in sorted(rows, key=lambda r: cost(r, input_tokens, output_tokens)):
        age = age_days(row, today)
        flag = f"OLD (over {max_age} days)" if age > max_age else ""
        lines.append(f"{row['model']:<46}{row['input']:>8.2f}{row['output']:>9.2f}"
                     f"{cost(row, input_tokens, output_tokens):>10.2f}{row['checked_on'].isoformat():>12}{age:>5}  {flag}".rstrip())
    old = sum(1 for r in rows if age_days(r, today) > max_age)
    lines.append(f"{len(rows)} rows, {old} older than {max_age} days.")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--file", default="prices.csv")
    p.add_argument("--input-tokens", type=int, default=3_000_000, help="input tokens you use")
    p.add_argument("--output-tokens", type=int, default=500_000, help="output tokens you use")
    p.add_argument("--max-age", type=int, default=30, help="flag rows checked more than this many days ago")
    p.add_argument("--today", type=date.fromisoformat, default=date.today(), help="pretend today is YYYY-MM-DD")
    a = p.parse_args()
    try:
        rows = load_prices(a.file)
    except (OSError, ValueError) as err:
        print(f"Cannot read prices: {err}", file=sys.stderr)
        sys.exit(1)
    print(render(rows, a.input_tokens, a.output_tokens, a.max_age, a.today))


if __name__ == "__main__":
    main()
