#!/usr/bin/env bash
set -euo pipefail

cd "${HOME}/hrm-text-sense-probes"

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

RUN_NAME="vibe-2026-expanded-120-harness-$(date -u +%Y%m%dT%H%M%SZ)"

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
  --out-dir "runs/${RUN_NAME}" \
  --max-new-tokens 256 \
  --hrm-condition direct \
  --baseline-format raw \
  --harness-mode official \
  --run-label "HRM-Text Expanded 120-Prompt Vibe Probe" \
  --comparison-stage "expanded around-1B post-trained/instruct comparators" \
  --seed 20260519

tar -C runs -czf "${HOME}/${RUN_NAME}.tgz" "${RUN_NAME}"
echo "${HOME}/${RUN_NAME}.tgz"
