from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, help="artifact run directory name under artifacts/")
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def model_order(manifest: dict) -> list[str]:
    return [model["key"] for model in manifest.get("models", [])]


def generation_config(harness: dict) -> str:
    effective = harness.get("effective_generation_config") or harness.get("sampling_overrides") or {}
    if not effective:
        return "Transformers/model default"
    return ", ".join(f"{key}={value!r}" for key, value in effective.items())


def main() -> None:
    args = parse_args()
    artifact = ROOT / "artifacts" / args.run
    manifest = json.loads((artifact / "manifest.json").read_text(encoding="utf-8"))
    records = load_jsonl(artifact / "outputs.jsonl")
    errors = load_jsonl(artifact / "errors.jsonl")
    out = artifact / "raw_prompt_by_prompt.md"

    by_prompt: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_prompt[record["prompt_id"]].append(record)

    records_by_prompt_model = {
        prompt_id: {record["model_key"]: record for record in prompt_records}
        for prompt_id, prompt_records in by_prompt.items()
    }
    order = model_order(manifest)

    lines: list[str] = []
    lines.append(f"# {manifest.get('run_label', args.run)}")
    lines.append("")
    lines.append(f"- Run: `{args.run}`")
    lines.append(f"- Started: `{manifest.get('started_at', 'not recorded')}`")
    lines.append(f"- Prompt file: `{manifest.get('prompt_file', 'not recorded')}`")
    lines.append(f"- Harness mode: `{manifest.get('harness_mode', 'not recorded')}`")
    lines.append(f"- Comparison stage: `{manifest.get('comparison_stage', 'not recorded')}`")
    lines.append(f"- Max new tokens: `{manifest.get('max_new_tokens', 'not recorded')}`")
    lines.append(f"- Outputs: `{len(records)}`")
    lines.append(f"- Errors: `{len(errors)}`")
    lines.append("")
    lines.append("## Models")
    lines.append("")
    for model in manifest.get("models", []):
        harness = model.get("harness") or {}
        lines.append(
            f"- `{model['key']}`: `{model['model_id']}` revision `{model.get('revision', 'not recorded')}`; "
            f"{harness.get('adapter', 'adapter not recorded')}; {generation_config(harness)}"
        )
    lines.append("")

    if errors:
        lines.append("## Errors")
        lines.append("")
        for error in errors:
            lines.append(
                f"- `{error.get('model_key', 'unknown')}` during `{error.get('stage', 'unknown')}`: "
                f"`{error.get('error_type', 'unknown')}` {error.get('error', '')}"
            )
        lines.append("")

    lines.append("## Prompt By Prompt")
    lines.append("")
    for idx, prompt_id in enumerate(sorted(by_prompt), start=1):
        prompt_records = by_prompt[prompt_id]
        first = prompt_records[0]
        lines.append(f"## {idx:03d}. {first['title']} (`{prompt_id}`)")
        lines.append("")
        lines.append(f"- Category: `{first['category']}`")
        lines.append(f"- Rubric: {first['rubric']}")
        lines.append("")
        lines.append("### Prompt")
        lines.append("")
        lines.append("```text")
        lines.append(first["prompt"])
        lines.append("```")
        lines.append("")

        records_by_model = records_by_prompt_model[prompt_id]
        for model_key in order:
            record = records_by_model.get(model_key)
            if not record:
                continue
            lines.append(f"### {model_key}")
            lines.append("")
            lines.append(
                f"- Model: `{record['model_id']}`; input tokens `{record['input_tokens']}`; "
                f"output tokens `{record['output_tokens']}`; elapsed `{float(record['elapsed_sec']):.2f}s`"
            )
            lines.append("")
            lines.append("```text")
            lines.append(record["generated_text"].strip())
            lines.append("```")
            lines.append("")

    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
