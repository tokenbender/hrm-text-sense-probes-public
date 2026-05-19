# Post-Trained Model Harness Audit

This note records the stage-fair rerun setup. HRM-Text stays on its published
post-trained checkpoint. Every comparator is now a post-trained, instruct, or
thinking checkpoint from the same family/size band used in the earlier strict
report.

The probe-wide cap is `max_new_tokens=256`. That cap is the comparison budget,
not a model-specific official recommendation.

## Harness Decisions

| Model key | Model | Prompt adapter | Sampling source | Sampling settings |
| --- | --- | --- | --- | --- |
| `hrm_direct` | `sapientinc/HRM-Text-1B` | HRM PrefixLM wrapper with `<|im_start|>{condition}{prompt}<|im_end|>` and `token_type_ids` set for the prefix | HRM-Text upstream eval config and model-card example | `do_sample=false`; `condition=direct` |
| `smollm2_instruct` | `HuggingFaceTB/SmolLM2-1.7B-Instruct` | Checkpoint chat template with assistant generation prompt | SmolLM2 Instruct model-card chat example | `do_sample=true`, `temperature=0.2`, `top_p=0.9` |
| `ouro_thinking` | `ByteDance/Ouro-1.4B-Thinking` | Checkpoint chat template with `enable_thinking=true` | Ouro Thinking model-card chat example | `do_sample=true`, `temperature=1.0`, `top_p=0.7` |
| `llama32_instruct` | `unsloth/Llama-3.2-3B-Instruct` | Checkpoint chat template with assistant generation prompt | Revision-pinned `generation_config.json` | `do_sample=true`, `temperature=0.6`, `top_p=0.9` |
| `qwen3_4b_instruct` | `Qwen/Qwen3-4B-Instruct-2507` | Checkpoint chat template with assistant generation prompt | Qwen model-card chat example and revision-pinned `generation_config.json` | `do_sample=true`, `temperature=0.7`, `top_p=0.8`, `top_k=20` |
| `olmo3_7b_instruct` | `allenai/Olmo-3-7B-Instruct` | Model-card `apply_chat_template(..., return_tensors='pt', return_dict=True)` path | OLMo 3 Instruct model-card chat example and revision-pinned `generation_config.json` | `do_sample=true`, `temperature=0.6`, `top_p=0.95`, `top_k=50` |

## Exclusion

`ByteDance/Ouro-1.4B-Thinking` has a post-trained Thinking checkpoint and a
model-card chat harness, so it was included in the manifest. It was excluded
from scoring because the official remote code did not load under
`transformers==5.8.0.dev0`, `transformers==4.57.6`, or
`transformers==4.56.2`.

The load failure is:

```text
NameError: name 'compute_default_rope_parameters' is not defined
```

The remote file defines that function as `OuroRotaryEmbedding.compute_default_rope_parameters`
but calls it as a bare free function in `OuroRotaryEmbedding.__init__`. A local
patch would likely be small, but it would stop being a clean official harness.

## Why This Replaces the Base-Model Comparison

The earlier official-harness artifact fixed sampling mistakes, but it still
compared HRM-Text against base checkpoints for Llama, Qwen, OLMo, and Ouro.
That was not a same-stage comparison. Base checkpoints often lack the chat
formatting and instruction-following behavior their post-trained variants rely
on, so weak outputs can reflect the wrong interface rather than weaker English
reasoning.

This rerun keeps the prompt set unchanged and moves only the comparator
checkpoints and adapters to the proper post-trained surfaces.

## Official Sources

- HRM-Text upstream evaluation config:
  `https://github.com/sapientinc/HRM-Text/blob/main/evaluation/config/hrm_benchmarking.yaml`
- HRM-Text model card:
  `https://huggingface.co/sapientinc/HRM-Text-1B`
- SmolLM2 Instruct model card:
  `https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct`
- Ouro Thinking model card:
  `https://huggingface.co/ByteDance/Ouro-1.4B-Thinking`
- Llama 3.2 3B Instruct generation config:
  `https://huggingface.co/unsloth/Llama-3.2-3B-Instruct/blob/main/generation_config.json`
- Qwen3 4B Instruct model card and generation config:
  `https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507`
- OLMo 3 7B Instruct model card and generation config:
  `https://huggingface.co/allenai/Olmo-3-7B-Instruct`
