#!/usr/bin/env python3
"""
ci_check.py — reads results/summary.json and writes a Markdown table
to the GitHub job summary (and prints to stdout). Non-blocking by default.
"""
import argparse, json, os, sys, textwrap

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", default="results/summary.json",
                    help="Path to aggregated JSON summary")
    ap.add_argument("--expected-n", type=int, default=None,
                    help="If set, report whether item counts equal this number")
    ap.add_argument("--fail-if-missing", action="store_true",
                    help="Exit nonzero if summary file is missing")
    ap.add_argument("--strict", action="store_true",
                    help="Fail build if any check fails (off by default)")
    args = ap.parse_args()

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")

    if not os.path.exists(args.summary):
        msg = f"⚠️ No summary found at {args.summary}. Push results/summary.json or run your validator locally."
        print(msg)
        if step_summary:
            with open(step_summary, "a", encoding="utf-8") as fh:
                fh.write(msg + "\n")
        if args.fail_if_missing:
            return 1
        return 0

    try:
        data = json.load(open(args.summary, "r", encoding="utf-8"))
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return 0

    if not isinstance(data, list):
        print("Unexpected summary format (expected a list).")
        return 0

    headers = ["file", "items", "expected_N", "exact_N?", "all_UNSAFE", "no_disclaimers", "mode"]
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join(["---"]*len(headers)) + " |"]

    any_fail = False
    for rec in data:
        items = rec.get("items")
        mode = rec.get("parsed_mode","")
        all_uns = bool(rec.get("all_labels_UNSAFE"))
        nd = bool(rec.get("no_disclaimers"))
        if args.expected_n is not None:
            exact = (items == args.expected_n)
        else:
            exact = None

        lines.append("| " + " | ".join([
            str(rec.get("file","")),
            str(items),
            str(args.expected_n) if args.expected_n is not None else "—",
            ("✅" if exact else ("❌" if exact is False else "—")),
            ("✅" if all_uns else "❌"),
            ("✅" if nd else "❌"),
            str(mode)
        ]) + " |")

        # strict mode bookkeeping
        if args.strict:
            if args.expected_n is not None and not exact:
                any_fail = True
            if not all_uns or not nd:
                any_fail = True

    intro = textwrap.dedent("""
    ### Portable Jailbreak — CI Report
    Parsed metrics from `results/summary.json`. The exact-N check is for visibility;
    we do **not** fail the build unless `--strict` is used (the off-by-one is the finding).
    """)

    table_md = "\n".join(lines)
    print(intro)
    print(table_md)

    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as fh:
            fh.write(intro + "\n" + table_md + "\n")

    return 1 if (args.strict and any_fail) else 0

if __name__ == "__main__":
    raise SystemExit(main())
