# Model Harness Audit

This note records the inference harness decision for each model in the strict
vibe probe report. The goal is not to give every model a chat wrapper. The goal
is to use the closest official completion surface for that specific checkpoint,
then record the exact adapter and generation settings in the run manifest.

The probe still caps output at `max_new_tokens=140`. That cap is a probe
constraint, not a model-specific sampling recommendation.

## Harness Decisions

| Model key | Model | Prompt adapter | Sampling source | Sampling settings |
| --- | --- | --- | --- | --- |
| `hrm_direct` | `sapientinc/HRM-Text-1B` | HRM PrefixLM wrapper with `<|im_start|>{condition}{prompt}<|im_end|>` and `token_type_ids` set for the prefix | HRM-Text upstream eval config and model-card example | `do_sample=false`; `condition=direct` for these short direct-answer probes |
| `ouro` | `ByteDance/Ouro-1.4B` | Raw completion | Model-card example | No explicit sampling override; uses Transformers/model defaults plus the probe token cap |
| `llama32` | `unsloth/Llama-3.2-3B` | Raw completion | Revision-pinned `generation_config.json` | `do_sample=true`, `temperature=0.6`, `top_p=0.9` |
| `qwen3_4b` | `Qwen/Qwen3-4B-Base` | Raw completion | Revision-pinned `generation_config.json` | `do_sample=false` |
| `olmo3_7b` | `allenai/Olmo-3-1025-7B` | Raw completion | Model-card example because the revision-pinned `generation_config.json` is empty | `do_sample=true`, `top_k=0`, `temperature=1.0`, `top_p=0.7` |

## Why the Previous HTML Needed a Rerun

The original strict run used a uniform greedy generation path:

```text
model.generate(..., do_sample=False, max_new_tokens=140)
```

That was appropriate for HRM-Text direct mode and Qwen3 Base, but not for the
Llama and OLMo rows. Llama's official generation config samples with
`temperature=0.6` and `top_p=0.9`. OLMo3's model-card example samples with
`temperature=1.0`, `top_p=0.7`, and `top_k=0`.

The official-harness rerun therefore treats the old HTML as a legacy artifact
and generates a new report with `harness_mode=official` recorded in
`manifest.json`.

## Official Sources

- HRM-Text upstream evaluation config:
  `https://github.com/sapientinc/HRM-Text/blob/main/evaluation/config/hrm_benchmarking.yaml`
- HRM-Text model card:
  `https://huggingface.co/sapientinc/HRM-Text-1B`
- Ouro model card:
  `https://huggingface.co/ByteDance/Ouro-1.4B`
- Llama 3.2 3B generation config:
  `https://huggingface.co/unsloth/Llama-3.2-3B/blob/main/generation_config.json`
- Qwen3 4B Base generation config:
  `https://huggingface.co/Qwen/Qwen3-4B-Base/blob/main/generation_config.json`
- OLMo3 7B model card:
  `https://huggingface.co/allenai/Olmo-3-1025-7B`
