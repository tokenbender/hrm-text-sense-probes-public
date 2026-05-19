from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPECIAL_TOKEN_RE = re.compile(r"</s>|<\|[^>]+?\|>")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, help="artifact run directory name under artifacts/")
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def prompt_echo_score(prompt: str, text: str) -> float:
    prompt_norm = " ".join(prompt.lower().split())
    text_norm = " ".join(text.lower().split())
    if not prompt_norm or not text_norm:
        return 0.0
    prefix = text_norm[: min(len(text_norm), len(prompt_norm), 600)]
    return SequenceMatcher(None, prompt_norm[:600], prefix).ratio()


def has_repeated_line(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) >= 12]
    counts = Counter(lines)
    return any(count >= 3 for count in counts.values())


def flags_for_record(record: dict, max_new_tokens: int) -> list[str]:
    text = record.get("generated_text", "").strip()
    flags: list[str] = []
    if not text:
        flags.append("empty")
    if record.get("output_tokens", 0) >= max_new_tokens:
        flags.append("hit_token_cap")
    if SPECIAL_TOKEN_RE.search(text):
        flags.append("special_token_leak")
    if prompt_echo_score(record.get("prompt", ""), text) >= 0.74:
        flags.append("prompt_echo")
    if "<think>" in text and "</think>" not in text:
        flags.append("unfinished_thinking")
    if has_repeated_line(text):
        flags.append("repeated_line")
    if len(text.split()) <= 3 and record.get("output_tokens", 0) <= 8:
        flags.append("too_terse")
    return flags


def main() -> None:
    args = parse_args()
    artifact = ROOT / "artifacts" / args.run
    manifest = json.loads((artifact / "manifest.json").read_text(encoding="utf-8"))
    records = load_jsonl(artifact / "outputs.jsonl")
    errors = load_jsonl(artifact / "errors.jsonl")
    max_new_tokens = int(manifest.get("max_new_tokens") or 256)

    model_flags: dict[str, Counter] = defaultdict(Counter)
    category_flags: dict[str, Counter] = defaultdict(Counter)
    flagged_records: list[dict] = []
    token_stats: dict[str, list[int]] = defaultdict(list)

    for record in records:
        model_key = record["model_key"]
        category = record["category"]
        token_stats[model_key].append(int(record.get("output_tokens", 0)))
        flags = flags_for_record(record, max_new_tokens)
        for flag in flags:
            model_flags[model_key][flag] += 1
            category_flags[category][flag] += 1
        if flags:
            flagged_records.append(
                {
                    "prompt_id": record["prompt_id"],
                    "title": record["title"],
                    "category": category,
                    "model_key": model_key,
                    "flags": flags,
                    "output_tokens": record.get("output_tokens", 0),
                    "excerpt": record.get("generated_text", "").strip()[:320],
                }
            )

    error_counts = Counter(error.get("model_key", "unknown") for error in errors)
    data = {
        "run": args.run,
        "outputs": len(records),
        "errors": len(errors),
        "error_counts": dict(error_counts),
        "model_flags": {key: dict(value) for key, value in sorted(model_flags.items())},
        "category_flags": {key: dict(value) for key, value in sorted(category_flags.items())},
        "flagged_records": flagged_records,
    }
    (artifact / "diagnostics.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = []
    lines.append(f"# Diagnostics: {args.run}")
    lines.append("")
    lines.append(f"- Outputs: `{len(records)}`")
    lines.append(f"- Errors: `{len(errors)}`")
    lines.append("- Scope: mechanical red flags only, not a correctness score.")
    lines.append("")
    lines.append("## Model Red Flags")
    lines.append("")
    lines.append("| Model | Avg tokens | Flags |")
    lines.append("|---|---:|---|")
    for model in manifest.get("models", []):
        key = model["key"]
        tokens = token_stats.get(key, [])
        avg = sum(tokens) / len(tokens) if tokens else 0.0
        flags = model_flags.get(key, Counter())
        flag_text = ", ".join(f"{flag}: {count}" for flag, count in sorted(flags.items())) or "none"
        if error_counts.get(key):
            flag_text = f"errors: {error_counts[key]}" + (f", {flag_text}" if flag_text != "none" else "")
        lines.append(f"| `{key}` | {avg:.1f} | {flag_text} |")
    lines.append("")
    lines.append("## Category Red Flags")
    lines.append("")
    lines.append("| Category | Flags |")
    lines.append("|---|---|")
    for category, flags in sorted(category_flags.items()):
        flag_text = ", ".join(f"{flag}: {count}" for flag, count in sorted(flags.items())) or "none"
        lines.append(f"| `{category}` | {flag_text} |")
    lines.append("")
    lines.append("## Flagged Examples")
    lines.append("")
    for item in flagged_records[:240]:
        lines.append(
            f"### `{item['prompt_id']}` / `{item['model_key']}` / {', '.join(item['flags'])}"
        )
        lines.append("")
        lines.append(f"- Category: `{item['category']}`")
        lines.append(f"- Title: {item['title']}")
        lines.append(f"- Output tokens: `{item['output_tokens']}`")
        lines.append("")
        lines.append("```text")
        lines.append(item["excerpt"])
        lines.append("```")
        lines.append("")
    (artifact / "diagnostics.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(artifact / "diagnostics.md")
    print(artifact / "diagnostics.json")


if __name__ == "__main__":
    main()
