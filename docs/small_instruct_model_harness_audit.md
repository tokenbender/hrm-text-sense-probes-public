# Around-1B Instruct Harness Audit

This note records the candidate and harness choices for the around-1B expansion
run. The prompt set stays fixed to `prompts/vibe_2026_nonce.jsonl`; only the
model family and adapter set changes.

## Selected Models

| Model key | Model | Prompt adapter | Sampling source |
| --- | --- | --- | --- |
| `hrm_direct` | `sapientinc/HRM-Text-1B` | HRM PrefixLM direct wrapper | HRM-Text model card and eval config |
| `smollm2_instruct` | `HuggingFaceTB/SmolLM2-1.7B-Instruct` | Checkpoint chat template | SmolLM2 model-card sampling |
| `qwen25_05b_instruct` | `Qwen/Qwen2.5-0.5B-Instruct` | Checkpoint chat template with Qwen system prompt | `generation_config.json` |
| `h2o_danube3_500m_chat` | `h2oai/h2o-danube3-500m-chat` | Checkpoint chat template, user-only | Model-card generate path |
| `falcon3_1b_instruct` | `tiiuae/Falcon3-1B-Instruct` | Checkpoint chat template with Falcon3 model-card system prompt | Model-card generate path plus `generation_config.json` |
| `tinyllama_11b_chat` | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | Checkpoint chat template | Model-card sampling |
| `lfm25_12b_instruct` | `LiquidAI/LFM2.5-1.2B-Instruct` | Repository `chat_template.jinja` | Model-card generation parameters |
| `qwen25_15b_instruct` | `Qwen/Qwen2.5-1.5B-Instruct` | Checkpoint chat template with Qwen system prompt | `generation_config.json` |
| `qwen3_06b_thinking` | `Qwen/Qwen3-0.6B` | Checkpoint chat template with `enable_thinking=true` | Qwen3 model-card default thinking mode plus `generation_config.json` |
| `qwen3_17b_thinking` | `Qwen/Qwen3-1.7B` | Checkpoint chat template with `enable_thinking=true` | Qwen3 model-card default thinking mode plus `generation_config.json` |
| `h2o_danube2_18b_chat` | `h2oai/h2o-danube2-1.8b-chat` | Checkpoint chat template, user-only | Model-card generate path plus `generation_config.json` |

## Exclusions

- `google/gemma-3-1b-it`: official checkpoint is license-gated; tokenizer,
  config, and generation config returned `401` without accepted access.
- `meta-llama/Llama-3.2-1B-Instruct`: official checkpoint is license-gated;
  tokenizer, config, and generation config returned `401` without accepted
  access.
- `ibm-granite/granite-3.3-2b-instruct`: useful as a 2B upper-bound model, but
  this run stays centered on sub-2B/around-1B comparators first.

## Output Budget

The expansion keeps the prior report's `max_new_tokens=256` cap so the rows are
easy to compare against the post-trained fair artifact.
