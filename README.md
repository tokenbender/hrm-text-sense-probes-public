# HRM-Text English Sense Probes

This repository shares a small, reproducible evaluation harness and the raw
results from an English sense-checking comparison centered on
`sapientinc/HRM-Text-1B`.

The project is not presented as a benchmark leaderboard. It is a qualitative
probe suite for ordinary English tasks that are easy to inspect by hand:
tracking small state changes, handling corrections, respecting instruction
boundaries, avoiding overclaiming, resolving references, and stopping at the
right answer. The main value of the repository is that the prompts, harness
choices, model outputs, and diagnostic notes are all preserved together.

## Main Result

The expanded run contains:

- 120 hand-written nonce prompts.
- 12 task areas, with 10 distinct prompts per area.
- 11 models, all run through the closest recorded official harness or sampling
  path used for that checkpoint.
- 1320 raw generations.
- 0 generation errors in the final expanded run.

The short read is that HRM-Text-1B is fast and sometimes effective on simple
state or stop-condition prompts, but it is not robust as a general English
sense model in this setup. It often answers too tersely, drops required
constraints, or collapses ordinary instruction-following prompts into one-token
answers. The stronger around-1B instruct rows in this run were
SmolLM2-1.7B-Instruct, LFM2.5-1.2B-Instruct, Qwen2.5-1.5B-Instruct, and
Falcon3-1B-Instruct, depending on the area.

Please treat that statement as a qualitative read over this prompt set, not as
a universal model ranking.

## What To Open First

- `docs/index.html` is the static HTML report. It is copied from the final run
  artifact so GitHub Pages can serve it directly.
- `artifacts/vibe-2026-expanded-120-harness-20260519T095252Z/index.html` is the
  same report inside the preserved run directory.
- `artifacts/vibe-2026-expanded-120-harness-20260519T095252Z/raw_prompt_by_prompt.md`
  contains the complete prompt-by-prompt raw output.
- `artifacts/vibe-2026-expanded-120-harness-20260519T095252Z/expanded_vibe_verdict.md`
  gives a concise read of good cases, failure cases, and area-level behavior.
- `docs/small_instruct_model_harness_audit.md` records the around-1B model and
  sampling choices.
- `docs/benchmaxxing_controls.md` explains what was done to reduce ordinary
  benchmark or synthetic-data leakage.

## Models In The Expanded Run

The final public artifact includes these rows:

- `sapientinc/HRM-Text-1B`
- `HuggingFaceTB/SmolLM2-1.7B-Instruct`
- `Qwen/Qwen2.5-0.5B-Instruct`
- `h2oai/h2o-danube3-500m-chat`
- `tiiuae/Falcon3-1B-Instruct`
- `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
- `LiquidAI/LFM2.5-1.2B-Instruct`
- `Qwen/Qwen2.5-1.5B-Instruct`
- `Qwen/Qwen3-0.6B`
- `Qwen/Qwen3-1.7B`
- `h2oai/h2o-danube2-1.8b-chat`

The Qwen3 rows use the default thinking-mode chat harness recorded for those
checkpoints. Under the shared 256-token cap, they often spend the budget in
thinking text and do not always reach a final answer. That behavior is kept in
the artifact because it is useful evidence about this short-answer setup, but
it should be interpreted carefully.

## Prompt Design

The expanded prompt file is `prompts/vibe_2026_nonce_120.jsonl`.

The prompts were written for this run rather than copied from common public
evaluation suites. They use mundane nonce details and avoid multiple-choice,
school-exam, and common synthetic-Q/A framing. The categories are:

- state tracking
- update handling
- instruction boundaries
- causal sense
- ambiguity
- negation
- epistemic restraint
- compression
- contradiction detection
- style control
- reference resolution
- stop conditions

These controls reduce obvious contamination risk, but they do not prove that no
model has seen a similar capability pattern before. The report should be read
as a transparent qualitative probe, not as a contamination-proof benchmark.

## Reproducing The Expanded Run

Install the dependencies in a Python environment with GPU-capable PyTorch
available:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the expanded comparison:

```bash
PYTHONPATH=src python -m hrm_sense_probes.run_probe \
  --prompt-file prompts/vibe_2026_nonce_120.jsonl \
  --model hrm_direct=sapientinc/HRM-Text-1B \
  --model smollm2_instruct=HuggingFaceTB/SmolLM2-1.7B-Instruct \
  --model qwen25_05b_instruct=Qwen/Qwen2.5-0.5B-Instruct \
  --model h2o_danube3_500m_chat=h2oai/h2o-danube3-500m-chat \
  --model falcon3_1b_instruct=tiiuae/Falcon3-1B-Instruct \
  --model tinyllama_11b_chat=TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
  --model lfm25_12b_instruct=LiquidAI/LFM2.5-1.2B-Instruct \
  --model qwen25_15b_instruct=Qwen/Qwen2.5-1.5B-Instruct \
  --model qwen3_06b_thinking=Qwen/Qwen3-0.6B \
  --model qwen3_17b_thinking=Qwen/Qwen3-1.7B \
  --model h2o_danube2_18b_chat=h2oai/h2o-danube2-1.8b-chat \
  --out-dir artifacts/repro-expanded-120 \
  --max-new-tokens 256 \
  --hrm-condition direct \
  --baseline-format raw \
  --harness-mode official \
  --run-label "HRM-Text Expanded 120-Prompt Sense Probe" \
  --comparison-stage "expanded around-1B post-trained/instruct comparators" \
  --seed 20260519
```

Build the companion reports from the artifact directory:

```bash
python tools/build_html_report.py --run repro-expanded-120
python tools/build_raw_prompt_dump.py --run repro-expanded-120
python tools/diagnose_run.py --run repro-expanded-120
```

The Lium scripts are included as one operator convenience path, but they are
not required. The harness itself is the Python module under `src/`.

## Repository Structure

- `src/hrm_sense_probes/run_probe.py` contains the model adapters, prompt
  rendering, official-harness generation settings, and JSONL output writer.
- `prompts/` contains the small and expanded prompt sets.
- `tools/` contains report and diagnostics builders.
- `docs/` contains the public HTML report and audit notes.
- `artifacts/vibe-2026-expanded-120-harness-20260519T095252Z/` contains the
  preserved final run.
- `scripts/` contains the expanded-run Lium helper scripts.

## License And Model Terms

The harness code in this repository is shared under the MIT License. The prompt
files and written notes are shared under CC BY 4.0. The generated model outputs
are included as reproducibility artifacts; please also respect the license and
usage terms of each source model.
