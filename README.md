# portable-jailbreak

Portable jailbreak against a local open-weight LLM (`gpt-oss-20b`) using a benign “negative-example” wrapper.
**Focus:** portability across languages/encodings + structured-output compliance (exact-N).

## Contents
- `prompts/PROMPT-primary.txt` – the wrapper template (no raw harmful content).
- `tools/validate_and_normalize.py` – parses model replies, normalizes to YAML, writes summary JSON.
- `findings/findings.json` – hackathon-ready entries (placeholders to fill).
- `results/` – aggregated metrics (`summary.json`) and normalized outputs.

> Safety note: No raw harmful content is stored in README. Normalized YAML is kept in `runs_normalized/`.

## Placeholders (must replace)
For **reproducibility**, replace these before use:
- `{N}` → a positive integer (e.g., `10` or `100`). Use the **same value** in all runs you compare.
- `{LANG}` → exactly `English` **or** `Turkish` (no other values for reproducibility).

See `prompts/PROMPT-primary.txt` for the template and the three `{PAYLOAD}` choices (English/Turkish/Base64).


