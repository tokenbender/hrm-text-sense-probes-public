from __future__ import annotations

import argparse
import html
import json
from collections import Counter, defaultdict
from pathlib import Path


RUN = "vibe-2026-20260519T005316Z"
ROOT = Path(__file__).resolve().parents[1]

MODEL_LABELS = {
    "hrm_direct": "HRM-Text-1B direct",
    "ouro": "Ouro 1.4B",
    "smollm2_instruct": "SmolLM2 1.7B Instruct",
    "qwen25_05b_instruct": "Qwen2.5 0.5B Instruct",
    "h2o_danube3_500m_chat": "H2O Danube3 500M Chat",
    "falcon3_1b_instruct": "Falcon3 1B Instruct",
    "tinyllama_11b_chat": "TinyLlama 1.1B Chat",
    "lfm25_12b_instruct": "LFM2.5 1.2B Instruct",
    "qwen25_15b_instruct": "Qwen2.5 1.5B Instruct",
    "qwen3_06b_thinking": "Qwen3 0.6B Thinking",
    "qwen3_17b_thinking": "Qwen3 1.7B Thinking",
    "h2o_danube2_18b_chat": "H2O Danube2 1.8B Chat",
    "ouro_thinking": "Ouro 1.4B Thinking",
    "llama32_instruct": "Llama 3.2 3B Instruct",
    "qwen3_4b_instruct": "Qwen3 4B Instruct 2507",
    "olmo3_7b_instruct": "OLMo 3 7B Instruct",
    "llama32": "Llama 3.2 3B base",
    "qwen3_4b": "Qwen3 4B base",
    "olmo3_7b": "OLMo3 7B base",
}

MODEL_ORDER = [
    "hrm_direct",
    "smollm2_instruct",
    "qwen25_05b_instruct",
    "h2o_danube3_500m_chat",
    "falcon3_1b_instruct",
    "tinyllama_11b_chat",
    "lfm25_12b_instruct",
    "qwen25_15b_instruct",
    "qwen3_06b_thinking",
    "qwen3_17b_thinking",
    "h2o_danube2_18b_chat",
    "ouro_thinking",
    "llama32_instruct",
    "qwen3_4b_instruct",
    "olmo3_7b_instruct",
    "qwen3_4b",
    "olmo3_7b",
    "llama32",
    "ouro",
]

VERDICTS = {
    "nonce_state_01": {
        "winner": "HRM and Qwen",
        "note": "Simple object-state tracking. HRM and Qwen preserve the thermos location; OLMo invents extra instructions and moves it.",
        "models": {
            "hrm_direct": ("pass", "Correct and concise."),
            "qwen3_4b": ("pass", "Correct and slightly clearer."),
            "olmo3_7b": ("fail", "Invents constraints and changes the thermos location."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_revision_02": {
        "winner": "HRM and Qwen",
        "note": "Later correction should override the earlier status line.",
        "models": {
            "hrm_direct": ("pass", "Correctly separates banner from checkout copy."),
            "qwen3_4b": ("pass", "Correct and readable."),
            "olmo3_7b": ("partial", "Reasons about the situation but drifts before a clean answer."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_instruction_03": {
        "winner": "None",
        "note": "Quoted-instruction boundary. Every successful-load model fails in a different way.",
        "models": {
            "hrm_direct": ("fail", "Collapses to a single letter."),
            "qwen3_4b": ("fail", "Repeats meta-instruction text instead of answering."),
            "olmo3_7b": ("fail", "Repeats the boundary instruction."),
            "llama32": ("fail", "Partly follows or repeats the bad quoted instruction."),
        },
    },
    "nonce_cause_04": {
        "winner": "HRM, weak pass",
        "note": "Printer recurrence after replacing the roll should weaken the label-roll explanation.",
        "models": {
            "hrm_direct": ("partial", "Rejects the label-roll explanation but names print head rather than warmup/calibration."),
            "qwen3_4b": ("partial", "Eventually rejects the roll explanation but starts with a weak power-mode story."),
            "olmo3_7b": ("fail", "Calls it a paper jam and drifts into an unrelated physics problem."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_ambiguity_05": {
        "winner": "Qwen, partial",
        "note": "Warehouse 'seal' should stay ambiguous until clarified.",
        "models": {
            "hrm_direct": ("partial", "Keeps two possibilities but both are narrow and does not ask a clarifying question."),
            "qwen3_4b": ("partial", "Gets closer to the intended physical/security-seal ambiguity but adds unrequested work."),
            "olmo3_7b": ("fail", "Echoes prompt-like text instead of resolving the task."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_negation_06": {
        "winner": "HRM",
        "note": "Room D remains unavailable because Kira did not cancel; Room C is the fallback.",
        "models": {
            "hrm_direct": ("pass", "Correct answer, very terse."),
            "qwen3_4b": ("fail", "Drifts into logic terminology."),
            "olmo3_7b": ("fail", "Contradicts itself, saying Room D then Room C."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_epistemic_07": {
        "winner": "HRM, partial",
        "note": "A subject line saying receipt arrived is not proof of payment.",
        "models": {
            "hrm_direct": ("partial", "Preserves payment uncertainty but overstates what is known about invoice receipt."),
            "qwen3_4b": ("fail", "Repeats 'No legal language'."),
            "olmo3_7b": ("fail", "Generic repeated advice, no actual answer."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_compression_08": {
        "winner": "Qwen",
        "note": "Exception-heavy compression. Guests are never allowed after 7 p.m.",
        "models": {
            "hrm_direct": ("fail", "Incorrectly allows guests later for alarms."),
            "qwen3_4b": ("pass", "Preserves closure, badge exception, guest ban, and logging code."),
            "olmo3_7b": ("fail", "Degenerates into repeated numbering."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_contradiction_09": {
        "winner": "HRM and Qwen",
        "note": "Conflicting clinic notes require a safe operational assumption.",
        "models": {
            "hrm_direct": ("pass", "Captures the conflict and safe fridge assumption."),
            "qwen3_4b": ("pass", "Correct and clear."),
            "olmo3_7b": ("partial", "Captures some conflict language but repeats the format."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_style_10": {
        "winner": "Qwen, partial",
        "note": "Three mundane reasons, no hype words. This exposes style and constraint-following drift.",
        "models": {
            "hrm_direct": ("partial", "Gives three reasons and avoids banned hype, but the reasons are weak."),
            "qwen3_4b": ("partial", "Better reasons, but adds an unrequested instruction and truncates before exactly three."),
            "olmo3_7b": ("fail", "Invents constraints and ignores the requested shape."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_ref_11": {
        "winner": "Qwen, partial",
        "note": "Reference resolution needs both badges, not just 'Mara's'.",
        "models": {
            "hrm_direct": ("fail", "Too underspecified; does not answer both parts."),
            "qwen3_4b": ("partial", "Gets Theo carrying Mara's badge but misses visitor vs old badge distinction."),
            "olmo3_7b": ("partial", "First sentence is correct, then drifts into unrelated math."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
    "nonce_stop_12": {
        "winner": "HRM and Qwen",
        "note": "Minimal inventory check with a stop-condition instruction.",
        "models": {
            "hrm_direct": ("pass", "Correct and minimal."),
            "qwen3_4b": ("pass", "Correct with one short reason."),
            "olmo3_7b": ("fail", "Misreads tray one and answers incorrectly."),
            "llama32": ("no output", "Stops immediately."),
        },
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", default=RUN, help="artifact run directory name under artifacts/")
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def slug(value: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in value.lower()).strip("-")


def verdict_class(verdict: str) -> str:
    return verdict.lower().replace(" ", "-")


def model_order_from_manifest(manifest: dict) -> list[str]:
    manifest_keys = [model["key"] for model in manifest.get("models", [])]
    ordered = [key for key in MODEL_ORDER if key in manifest_keys]
    ordered.extend(key for key in manifest_keys if key not in ordered)
    return ordered


def load_judgments(artifact: Path) -> dict:
    path = artifact / "judgments.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return VERDICTS


def judgment_for_prompt(prompt_id: str, prompt_record: dict, judgments: dict) -> dict:
    if prompt_id in judgments:
        return judgments[prompt_id]
    return {
        "winner": "Not manually judged",
        "note": prompt_record.get("rubric") or "Raw expanded-suite output; no manual judgment recorded.",
        "models": {},
    }


def format_generation_config(harness: dict | None) -> str:
    if not harness:
        return "not recorded"
    effective = harness.get("effective_generation_config") or harness.get("sampling_overrides") or {}
    if not effective:
        return "Transformers/model default"
    return ", ".join(f"{key}={value!r}" for key, value in effective.items())


def source_links(harness: dict | None) -> str:
    urls = (harness or {}).get("source_urls") or []
    if not urls:
        return ""
    return "<br>".join(f'<a href="{esc(url)}">{esc(url)}</a>' for url in urls)


def model_card(record: dict, verdict: str, note: str) -> str:
    text = esc(record["generated_text"].strip())
    harness = record.get("harness") or {}
    return f"""
      <article class="model-card {verdict_class(verdict)}">
        <header>
          <h4>{esc(MODEL_LABELS.get(record["model_key"], record["model_key"]))}</h4>
          <span class="chip {verdict_class(verdict)}">{esc(verdict)}</span>
        </header>
        <p class="model-note">{esc(note)}</p>
        <dl class="metrics">
          <div><dt>Tokens</dt><dd>{esc(record["output_tokens"])}</dd></div>
          <div><dt>Elapsed</dt><dd>{float(record["elapsed_sec"]):.2f}s</dd></div>
        </dl>
        <p class="harness-line">{esc(harness.get("adapter", "unrecorded"))}: {esc(format_generation_config(harness))}</p>
        <pre>{text}</pre>
      </article>
    """


def main() -> None:
    args = parse_args()
    artifact = ROOT / "artifacts" / args.run
    out = artifact / "index.html"
    judgments = load_judgments(artifact)
    manifest = json.loads((artifact / "manifest.json").read_text(encoding="utf-8"))
    records = load_jsonl(artifact / "outputs.jsonl")
    errors = load_jsonl(artifact / "errors.jsonl")
    controls = (ROOT / "docs" / "benchmaxxing_controls.md").read_text(encoding="utf-8")
    model_order = model_order_from_manifest(manifest)

    by_prompt: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_prompt[record["prompt_id"]].append(record)

    verdict_counts = Counter()
    model_counts = defaultdict(Counter)
    for prompt_id, prompt_records in by_prompt.items():
        model_verdicts = judgment_for_prompt(prompt_id, prompt_records[0], judgments)["models"]
        for record in prompt_records:
            verdict = model_verdicts.get(record["model_key"], ("unjudged", ""))[0]
            verdict_counts[verdict] += 1
            model_counts[record["model_key"]][verdict] += 1

    prompt_sections = []
    for idx, prompt_id in enumerate(sorted(by_prompt), start=1):
        prompt_records = by_prompt[prompt_id]
        first = prompt_records[0]
        meta = judgment_for_prompt(prompt_id, first, judgments)
        records_by_model = {record["model_key"]: record for record in prompt_records}
        cards = []
        for model_key in model_order:
            record = records_by_model.get(model_key)
            if not record:
                continue
            verdict, note = meta["models"].get(model_key, ("unjudged", "No manual judgment recorded."))
            cards.append(model_card(record, verdict, note))

        prompt_sections.append(f"""
          <section class="test-card" id="{esc(prompt_id)}">
            <div class="test-head">
              <div>
                <p class="eyebrow">Test {idx:02d} / {esc(first["category"])}</p>
                <h3>{esc(first["title"])}</h3>
              </div>
              <a class="anchor" href="#{esc(prompt_id)}">#{esc(prompt_id)}</a>
            </div>
            <div class="prompt-box">
              <strong>Prompt</strong>
              <p>{esc(first["prompt"])}</p>
            </div>
            <div class="rubric-grid">
              <div><span>Rubric</span><p>{esc(first["rubric"])}</p></div>
              <div><span>Read</span><p>{esc(meta["note"])}</p></div>
              <div><span>Winner</span><p>{esc(meta["winner"])}</p></div>
            </div>
            <div class="model-grid">
              {"".join(cards)}
            </div>
          </section>
        """)

    model_rows = []
    errors_by_model = defaultdict(list)
    for error in errors:
        errors_by_model[error["model_key"]].append(error)
    for model in manifest["models"]:
        key = model["key"]
        harness = model.get("harness") or {}
        counts = model_counts.get(key, Counter())
        if errors_by_model.get(key) and not counts:
            status = "load/generation error"
        else:
            status = ", ".join(f"{name}: {counts.get(name, 0)}" for name in ["pass", "partial", "fail", "no output", "unjudged"])
        model_rows.append(f"""
          <tr>
            <td>{esc(MODEL_LABELS.get(key, key))}</td>
            <td><code>{esc(model["model_id"])}</code></td>
            <td><code>{esc(model["revision"])}</code></td>
            <td>{esc(harness.get("adapter", "unrecorded"))}</td>
            <td>{esc(format_generation_config(harness))}</td>
            <td>{esc(status)}</td>
          </tr>
        """)

    error_items = "".join(
        f"""
        <li>
          <strong>{esc(error["model_key"])}</strong> failed during <code>{esc(error["stage"])}</code>:
          <code>{esc(error["error_type"])}</code> {esc(error["error"])}
        </li>
        """
        for error in errors
    )
    if error_items:
        error_notice = f"""
      <div class="notice">
        <strong>Load/generation notes.</strong>
        <ul>{error_items}</ul>
      </div>
        """
    else:
        error_notice = ""
    legacy_notice = ""
    if manifest.get("harness_mode", "legacy") != "official":
        legacy_notice = """
      <div class="notice">
        <strong>Legacy harness.</strong>
        This artifact predates the official per-model harness audit. Treat its
        sampling table as an audit trail, not as the final sampling-correct
        comparison.
      </div>
        """
    stage_notice = ""
    if "post" in str(manifest.get("comparison_stage", "")).lower():
        stage_notice = """
      <div class="notice">
        <strong>Stage-fair comparison.</strong>
        Comparator rows use post-trained or instruct checkpoints with their own
        chat-template adapters and generation settings recorded below. The prior
        base-model comparison is retained only as a historical artifact.
      </div>
        """

    harness_rows = []
    for model in manifest["models"]:
        harness = model.get("harness") or {}
        harness_rows.append(f"""
          <tr>
            <td>{esc(MODEL_LABELS.get(model["key"], model["key"]))}</td>
            <td>{esc(harness.get("sampling_source", "not recorded"))}</td>
            <td>{esc(harness.get("prompt_format", "not recorded"))}</td>
            <td>{esc(format_generation_config(harness))}</td>
            <td>{source_links(harness)}</td>
          </tr>
        """)

    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(manifest.get("run_label", "HRM-Text Strict Vibe Probe Report"))}</title>
  <style>
    :root {{
      --bg: #f6f4ef;
      --panel: #fffdf8;
      --ink: #1d1b16;
      --muted: #666153;
      --line: #d9d2c3;
      --pass: #187449;
      --partial: #9a6500;
      --fail: #b42d2a;
      --none: #60646c;
      --accent: #255f85;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
      color: var(--ink);
      background: var(--bg);
    }}
    header.hero {{
      padding: 40px 32px 28px;
      border-bottom: 1px solid var(--line);
      background: #ebe6da;
    }}
    main {{ max-width: 1440px; margin: 0 auto; padding: 28px 28px 56px; }}
    h1 {{ margin: 0 0 10px; font-size: 34px; line-height: 1.08; letter-spacing: 0; }}
    h2 {{ margin: 34px 0 14px; font-size: 22px; }}
    h3 {{ margin: 0; font-size: 20px; }}
    h4 {{ margin: 0; font-size: 15px; }}
    p {{ margin: 0; }}
    code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.92em; }}
    .subhead {{ max-width: 920px; color: var(--muted); font-size: 16px; }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}
    .summary-tile {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}
    .summary-tile span {{ display: block; color: var(--muted); font-size: 12px; text-transform: uppercase; }}
    .summary-tile strong {{ display: block; margin-top: 4px; font-size: 20px; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }}
    th, td {{ padding: 11px 12px; border-bottom: 1px solid var(--line); vertical-align: top; text-align: left; }}
    th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; background: #f1ede3; }}
    tr:last-child td {{ border-bottom: 0; }}
    .notice {{
      background: #fff7df;
      border: 1px solid #e5c56a;
      border-radius: 8px;
      padding: 14px 16px;
      margin: 18px 0;
    }}
    .controls {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      color: var(--muted);
      white-space: pre-wrap;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12px;
      max-height: 260px;
      overflow: auto;
    }}
    .toc {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 8px;
      margin: 12px 0 24px;
    }}
    .toc a {{
      display: block;
      color: var(--accent);
      text-decoration: none;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px 12px;
    }}
    .test-card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      margin: 18px 0;
    }}
    .test-head {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      align-items: start;
      border-bottom: 1px solid var(--line);
      padding-bottom: 12px;
    }}
    .eyebrow {{ color: var(--muted); font-size: 12px; text-transform: uppercase; margin-bottom: 4px; }}
    .anchor {{ color: var(--accent); text-decoration: none; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .prompt-box {{
      margin: 14px 0;
      padding: 14px;
      background: #f8f5ed;
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .prompt-box strong {{ display: block; margin-bottom: 8px; }}
    .rubric-grid {{
      display: grid;
      grid-template-columns: 1.4fr 1.4fr 0.8fr;
      gap: 10px;
      margin-bottom: 14px;
    }}
    .rubric-grid div {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px 12px;
      background: #fbf9f4;
    }}
    .rubric-grid span {{ display: block; color: var(--muted); font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }}
    .model-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .model-card {{
      border: 1px solid var(--line);
      border-left-width: 5px;
      border-radius: 8px;
      padding: 12px;
      background: #fffefb;
      min-width: 0;
    }}
    .model-card.pass {{ border-left-color: var(--pass); }}
    .model-card.partial {{ border-left-color: var(--partial); }}
    .model-card.fail {{ border-left-color: var(--fail); }}
    .model-card.no-output {{ border-left-color: var(--none); }}
    .model-card.unjudged {{ border-left-color: var(--none); }}
    .model-card header {{ display: flex; justify-content: space-between; gap: 12px; align-items: center; }}
    .chip {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      border-radius: 999px;
      padding: 3px 9px;
      font-size: 12px;
      font-weight: 700;
      color: white;
      text-transform: uppercase;
      white-space: nowrap;
    }}
    .chip.pass {{ background: var(--pass); }}
    .chip.partial {{ background: var(--partial); }}
    .chip.fail {{ background: var(--fail); }}
    .chip.no-output {{ background: var(--none); }}
    .chip.unjudged {{ background: var(--none); }}
    .model-note {{ color: var(--muted); font-size: 13px; margin: 8px 0 10px; }}
    .harness-line {{
      color: var(--muted);
      font-size: 12px;
      margin: -2px 0 10px;
      overflow-wrap: anywhere;
    }}
    .metrics {{ display: flex; gap: 14px; margin: 0 0 10px; color: var(--muted); font-size: 12px; }}
    .metrics div {{ display: flex; gap: 5px; }}
    .metrics dt {{ font-weight: 700; }}
    .metrics dd {{ margin: 0; }}
    pre {{
      margin: 0;
      padding: 12px;
      background: #1f2428;
      color: #f2f4f5;
      border-radius: 6px;
      overflow: auto;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      font-size: 12px;
      max-height: 320px;
    }}
    @media (max-width: 900px) {{
      .summary-grid, .rubric-grid, .model-grid {{ grid-template-columns: 1fr; }}
      header.hero {{ padding: 28px 20px; }}
      main {{ padding: 18px; }}
    }}
  </style>
</head>
<body>
  <header class="hero">
    <h1>{esc(manifest.get("run_label", "HRM-Text Strict Vibe Probe Report"))}</h1>
    <p class="subhead">
      Fresh nonce-heavy English probes with per-model harness metadata recorded in the manifest.
      HRM used <code>direct</code>, not <code>synth,cot</code>. Comparator prompts used the registered adapter for each checkpoint.
      Comparison stage: <code>{esc(manifest.get("comparison_stage", "unspecified"))}</code>.
    </p>
    <div class="summary-grid">
      <div class="summary-tile"><span>Prompts</span><strong>{len(by_prompt)}</strong></div>
      <div class="summary-tile"><span>Outputs</span><strong>{len(records)}</strong></div>
      <div class="summary-tile"><span>Successful Models</span><strong>{len(model_counts)}</strong></div>
      <div class="summary-tile"><span>Model Errors</span><strong>{len(errors)}</strong></div>
    </div>
  </header>
  <main>
    <section>
      <h2>Run Metadata</h2>
      {legacy_notice}
      {stage_notice}
      <table>
        <tbody>
          <tr><th>Started</th><td><code>{esc(manifest["started_at"])}</code></td></tr>
          <tr><th>Device</th><td>{esc(manifest["cuda_device"])} / {esc(manifest["dtype"])}</td></tr>
          <tr><th>Runtime</th><td>torch <code>{esc(manifest.get("torch", "not recorded"))}</code>, transformers <code>{esc(manifest.get("transformers", "not recorded"))}</code></td></tr>
          <tr><th>Prompt file</th><td><code>{esc(manifest["prompt_file"])}</code></td></tr>
          <tr><th>HRM condition</th><td><code>{esc(manifest["hrm_condition"])}</code></td></tr>
          <tr><th>Baseline format</th><td><code>{esc(manifest["baseline_format"])}</code></td></tr>
          <tr><th>Harness mode</th><td><code>{esc(manifest.get("harness_mode", "legacy"))}</code></td></tr>
          <tr><th>Seed</th><td><code>{esc(manifest.get("seed", "not recorded"))}</code></td></tr>
          <tr><th>Max new tokens</th><td>{esc(manifest["max_new_tokens"])}</td></tr>
        </tbody>
      </table>
    </section>

    <section>
      <h2>Model Summary</h2>
      <table>
        <thead><tr><th>Model</th><th>ID</th><th>Revision</th><th>Adapter</th><th>Effective generation config</th><th>Judgment counts</th></tr></thead>
        <tbody>{"".join(model_rows)}</tbody>
      </table>
      {error_notice}
    </section>

    <section>
      <h2>Harness Audit</h2>
      <table>
        <thead><tr><th>Model</th><th>Sampling source</th><th>Prompt format</th><th>Effective generation config</th><th>Official source</th></tr></thead>
        <tbody>{"".join(harness_rows)}</tbody>
      </table>
    </section>

    <section>
      <h2>Benchmaxxing Controls</h2>
      <div class="controls">{esc(controls)}</div>
    </section>

    <section>
      <h2>Test Index</h2>
      <nav class="toc">
        {"".join(f'<a href="#{esc(pid)}">{idx:02d}. {esc(by_prompt[pid][0]["title"])}</a>' for idx, pid in enumerate(sorted(by_prompt), start=1))}
      </nav>
    </section>

    <section>
      <h2>All Tests</h2>
      {"".join(prompt_sections)}
    </section>
  </main>
</body>
</html>
"""
    html_text = "\n".join(line.rstrip() for line in html_text.splitlines()) + "\n"
    out.write_text(html_text, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
