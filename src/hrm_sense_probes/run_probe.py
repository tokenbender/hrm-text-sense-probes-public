from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import time
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
import transformers
from huggingface_hub import model_info
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, GenerationConfig


HRM_CONDITIONS = {
    "direct": "<|object_ref_start|>",
    "cot": "<|object_ref_end|>",
    "noisy": "<|quad_start|>",
    "synth": "<|quad_end|>",
}


@dataclass(frozen=True)
class ModelSpec:
    key: str
    model_id: str
    kind: str


MODEL_HARNESSES: dict[str, dict[str, Any]] = {
    "hrm_direct": {
        "adapter": "hrm_prefixlm_direct",
        "prompt_format": "<|im_start|>{condition_tokens}{prompt}<|im_end|>",
        "sampling_source": "HRM-Text upstream eval direct config and model-card inference example",
        "sampling_overrides": {"do_sample": False},
        "source_urls": [
            "https://github.com/sapientinc/HRM-Text/blob/main/evaluation/config/hrm_benchmarking.yaml",
            "https://huggingface.co/sapientinc/HRM-Text-1B",
        ],
        "notes": [
            "Uses PrefixLM token_type_ids with prompt positions marked as prefix.",
            "Uses the direct condition token because these are short English instruction probes, not chain-of-thought benchmarks.",
        ],
    },
    "ouro": {
        "adapter": "raw_completion_default_generate",
        "prompt_format": "{prompt}",
        "sampling_source": "Ouro model-card raw completion example; no generation_config.json at the run revision",
        "sampling_overrides": {},
        "source_urls": ["https://huggingface.co/ByteDance/Ouro-1.4B"],
        "notes": [
            "Tokenizer has a chat template, but the official model-card generation example uses raw completion.",
            "No output is expected unless the model loads successfully under the installed Transformers stack.",
        ],
    },
    "smollm2_instruct": {
        "adapter": "chat_template_model_card_sampling",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
        "sampling_source": "SmolLM2 Instruct model-card chat example",
        "sampling_overrides": {"do_sample": True, "temperature": 0.2, "top_p": 0.9},
        "source_urls": ["https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct"],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "notes": [
            "Uses the checkpoint chat template, including the tokenizer's default SmolLM system message.",
            "Uses model-card sampling values and the probe-wide output cap.",
        ],
    },
    "qwen25_05b_instruct": {
        "adapter": "chat_template_generation_config",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
        "sampling_source": "Qwen2.5 Instruct model-card chat example plus generation_config.json",
        "sampling_overrides": {},
        "source_urls": [
            "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct",
            "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/main/generation_config.json",
        ],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant.",
        "notes": [
            "Uses the official Qwen2.5 chat template and revision-pinned sampling config.",
        ],
    },
    "h2o_danube3_500m_chat": {
        "adapter": "chat_template_model_card_default_generate",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
        "sampling_source": "H2O Danube3 500M Chat model-card chat example",
        "sampling_overrides": {},
        "source_urls": ["https://huggingface.co/h2oai/h2o-danube3-500m-chat"],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "notes": [
            "The tokenizer chat template rejects system messages, so prompts are user-only as shown in the model card.",
        ],
    },
    "falcon3_1b_instruct": {
        "adapter": "chat_template_model_card_default_generate",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
        "sampling_source": "Falcon3 Instruct model-card chat example plus generation_config.json",
        "sampling_overrides": {},
        "source_urls": [
            "https://huggingface.co/tiiuae/Falcon3-1B-Instruct",
            "https://huggingface.co/tiiuae/Falcon3-1B-Instruct/blob/main/generation_config.json",
        ],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "system_prompt": "You are a helpful friendly assistant Falcon3 from TII, try to follow instructions as much as possible.",
        "notes": [
            "Uses the system message from the official model-card example.",
        ],
    },
    "tinyllama_11b_chat": {
        "adapter": "chat_template_model_card_sampling",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
        "sampling_source": "TinyLlama Chat model-card generation example",
        "sampling_overrides": {"do_sample": True, "temperature": 0.7, "top_k": 50, "top_p": 0.95},
        "source_urls": ["https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0"],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "notes": [
            "Uses the checkpoint chat template and model-card sampling values.",
        ],
    },
    "lfm25_12b_instruct": {
        "adapter": "chat_template_model_card_sampling",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)",
        "sampling_source": "Liquid AI LFM2.5 Instruct model-card generation parameters",
        "sampling_overrides": {
            "do_sample": True,
            "temperature": 0.1,
            "top_k": 50,
            "repetition_penalty": 1.05,
        },
        "source_urls": ["https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct"],
        "add_generation_prompt": True,
        "template_encode_mode": "tokens",
        "notes": [
            "Uses the repository chat_template.jinja and model-card generation parameters.",
        ],
    },
    "qwen25_15b_instruct": {
        "adapter": "chat_template_generation_config",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
        "sampling_source": "Qwen2.5 Instruct model-card chat example plus generation_config.json",
        "sampling_overrides": {},
        "source_urls": [
            "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct",
            "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/main/generation_config.json",
        ],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant.",
        "notes": [
            "Uses the official Qwen2.5 chat template and revision-pinned sampling config.",
        ],
    },
    "qwen3_06b_thinking": {
        "adapter": "chat_template_thinking_generation_config",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)",
        "sampling_source": "Qwen3 model-card thinking-mode chat example plus generation_config.json",
        "sampling_overrides": {},
        "source_urls": [
            "https://huggingface.co/Qwen/Qwen3-0.6B",
            "https://huggingface.co/Qwen/Qwen3-0.6B/blob/main/generation_config.json",
        ],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "template_kwargs": {"enable_thinking": True},
        "notes": [
            "Uses Qwen3 thinking mode because the model card states it is the default mode.",
        ],
    },
    "qwen3_17b_thinking": {
        "adapter": "chat_template_thinking_generation_config",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)",
        "sampling_source": "Qwen3 model-card thinking-mode chat example plus generation_config.json",
        "sampling_overrides": {},
        "source_urls": [
            "https://huggingface.co/Qwen/Qwen3-1.7B",
            "https://huggingface.co/Qwen/Qwen3-1.7B/blob/main/generation_config.json",
        ],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "template_kwargs": {"enable_thinking": True},
        "notes": [
            "Uses Qwen3 thinking mode because the model card states it is the default mode.",
        ],
    },
    "h2o_danube2_18b_chat": {
        "adapter": "chat_template_generation_config",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
        "sampling_source": "H2O Danube2 1.8B Chat model-card chat example plus generation_config.json",
        "sampling_overrides": {},
        "source_urls": [
            "https://huggingface.co/h2oai/h2o-danube2-1.8b-chat",
            "https://huggingface.co/h2oai/h2o-danube2-1.8b-chat/blob/main/generation_config.json",
        ],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "notes": [
            "The tokenizer chat template rejects system messages, so prompts are user-only as shown in the model card.",
        ],
    },
    "ouro_thinking": {
        "adapter": "chat_template_thinking_model_card_sampling",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, enable_thinking=True)",
        "sampling_source": "Ouro Thinking model-card chat example",
        "sampling_overrides": {"do_sample": True, "temperature": 1.0, "top_p": 0.7},
        "source_urls": ["https://huggingface.co/ByteDance/Ouro-1.4B-Thinking"],
        "add_generation_prompt": True,
        "template_encode_mode": "tokens",
        "template_kwargs": {"enable_thinking": True},
        "notes": [
            "Uses the post-trained Thinking checkpoint rather than the base Ouro checkpoint.",
            "Keeps the model's official thinking tag in the rendered prompt.",
        ],
    },
    "llama32_instruct": {
        "adapter": "chat_template_generation_config",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
        "sampling_source": "revision-pinned Hugging Face generation_config.json",
        "sampling_overrides": {},
        "source_urls": ["https://huggingface.co/unsloth/Llama-3.2-3B-Instruct/blob/main/generation_config.json"],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "notes": [
            "Uses the Llama instruct chat template and the checkpoint generation config.",
        ],
    },
    "qwen3_4b_instruct": {
        "adapter": "chat_template_generation_config",
        "prompt_format": "tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)",
        "sampling_source": "Qwen3 Instruct model-card chat example plus generation_config.json",
        "sampling_overrides": {},
        "source_urls": [
            "https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507",
            "https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507/blob/main/generation_config.json",
        ],
        "add_generation_prompt": True,
        "template_encode_mode": "string",
        "notes": [
            "Uses the post-trained Qwen3 instruct checkpoint, not Qwen3-4B-Base.",
            "The 2507 Instruct model card uses chat-template formatting with an assistant generation prompt.",
        ],
    },
    "olmo3_7b_instruct": {
        "adapter": "chat_template_return_dict_model_card_sampling",
        "prompt_format": "tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors='pt', return_dict=True)",
        "sampling_source": "OLMo 3 Instruct model-card chat example plus generation_config.json",
        "sampling_overrides": {"top_k": 50},
        "source_urls": [
            "https://huggingface.co/allenai/Olmo-3-7B-Instruct",
            "https://huggingface.co/allenai/Olmo-3-7B-Instruct/blob/main/generation_config.json",
        ],
        "add_generation_prompt": True,
        "template_encode_mode": "return_dict",
        "notes": [
            "Uses the OLMo 3 Instruct chat-template API shown in the model card.",
            "Adds the model-card top_k=50 value on top of the revision-pinned generation config.",
        ],
    },
    "llama32": {
        "adapter": "raw_completion_generation_config",
        "prompt_format": "{prompt}",
        "sampling_source": "revision-pinned Hugging Face generation_config.json",
        "sampling_overrides": {"do_sample": True, "temperature": 0.6, "top_p": 0.9},
        "source_urls": ["https://huggingface.co/unsloth/Llama-3.2-3B/blob/main/generation_config.json"],
        "notes": ["Base model, no chat template in tokenizer_config.json."],
    },
    "qwen3_4b": {
        "adapter": "raw_completion_generation_config",
        "prompt_format": "{prompt}",
        "sampling_source": "revision-pinned Hugging Face generation_config.json",
        "sampling_overrides": {"do_sample": False},
        "source_urls": ["https://huggingface.co/Qwen/Qwen3-4B-Base/blob/main/generation_config.json"],
        "notes": [
            "Base model row uses raw completion rather than chat formatting.",
            "The probe keeps its own output-token cap for comparability.",
        ],
    },
    "olmo3_7b": {
        "adapter": "raw_completion_model_card_sampling",
        "prompt_format": "{prompt}",
        "sampling_source": "OLMo3 model-card generation example",
        "sampling_overrides": {"do_sample": True, "top_k": 0, "temperature": 1.0, "top_p": 0.7},
        "source_urls": ["https://huggingface.co/allenai/Olmo-3-1025-7B"],
        "notes": [
            "The revision-pinned generation_config.json is empty, so the model-card example is the official sampling source.",
        ],
    },
}

SAMPLING_KEYS = (
    "do_sample",
    "temperature",
    "top_p",
    "top_k",
    "min_p",
    "typical_p",
    "repetition_penalty",
    "max_new_tokens",
    "bos_token_id",
    "eos_token_id",
    "pad_token_id",
)


def parse_model_spec(value: str) -> ModelSpec:
    if "=" not in value:
        raise argparse.ArgumentTypeError("model must be KEY=MODEL_ID")
    key, model_id = value.split("=", 1)
    key = key.strip()
    model_id = model_id.strip()
    if not key or not model_id:
        raise argparse.ArgumentTypeError("model key and id must be non-empty")
    kind = "hrm" if "HRM-Text" in model_id or key.lower() == "hrm" else "causal"
    return ModelSpec(key=key, model_id=model_id, kind=kind)


def static_harness(spec: ModelSpec, mode: str) -> dict[str, Any]:
    if mode == "legacy":
        return {
            "adapter": "legacy_uniform_greedy",
            "prompt_format": "<hrm-special-or-raw-prompt>",
            "sampling_source": "legacy repo default",
            "sampling_overrides": {"do_sample": False},
            "source_urls": [],
            "notes": ["Uniform greedy decoding was used before the official-harness audit."],
        }
    return MODEL_HARNESSES.get(
        spec.key,
        {
            "adapter": "raw_completion_generation_config",
            "prompt_format": "{prompt}",
            "sampling_source": "Hugging Face generation_config.json or Transformers defaults",
            "sampling_overrides": {},
            "source_urls": [f"https://huggingface.co/{spec.model_id}"],
            "notes": ["No repo-local adapter was registered for this model key."],
        },
    )


def load_prompts(path: Path, limit: int | None) -> list[dict[str, Any]]:
    prompts: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            for field in ("id", "category", "title", "prompt", "rubric"):
                if field not in obj:
                    raise ValueError(f"{path}:{line_no} missing {field}")
            prompts.append(obj)
            if limit is not None and len(prompts) >= limit:
                break
    return prompts


def choose_device(requested: str) -> str:
    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def choose_dtype(device: str, requested: str) -> torch.dtype | None:
    if requested == "auto":
        if device == "cuda":
            return torch.bfloat16
        if device == "mps":
            return torch.float16
        return None
    return getattr(torch, requested)


def hrm_condition_tokens(condition: str) -> str:
    tags = [part.strip() for part in condition.split(",") if part.strip()]
    if not tags:
        raise ValueError("HRM condition cannot be empty")
    unknown = [tag for tag in tags if tag not in HRM_CONDITIONS]
    if unknown:
        raise ValueError(f"Unknown HRM condition tag(s): {unknown}")
    return "".join(HRM_CONDITIONS[tag] for tag in tags)


def format_prompt(prompt: str, spec: ModelSpec, hrm_condition: str, baseline_format: str) -> str:
    text = prompt.strip()
    if spec.kind == "hrm":
        condition = hrm_condition_tokens(hrm_condition)
        return f"<|im_start|>{condition}{text}<|im_end|>"
    if baseline_format == "answer_suffix":
        return f"{text}\n\nAnswer:"
    if baseline_format == "raw":
        return text
    raise ValueError(f"unknown baseline format: {baseline_format}")


def chat_messages(prompt: str, harness: dict[str, Any]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    system_prompt = harness.get("system_prompt")
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt.strip()})
    return messages


def encode_prompt(
    tokenizer,
    prompt: str,
    spec: ModelSpec,
    hrm_condition: str,
    baseline_format: str,
    harness: dict[str, Any],
    max_context: int,
) -> tuple[str, dict[str, torch.Tensor]]:
    adapter = harness.get("adapter", "")
    if adapter.startswith("chat_template"):
        messages = chat_messages(prompt, harness)
        template_kwargs = dict(harness.get("template_kwargs") or {})
        template_kwargs["add_generation_prompt"] = harness.get("add_generation_prompt", True)
        encode_mode = harness.get("template_encode_mode", "string")

        if encode_mode == "return_dict":
            encoded = tokenizer.apply_chat_template(
                messages,
                tokenize=True,
                return_tensors="pt",
                return_dict=True,
                truncation=True,
                max_length=max_context,
                **template_kwargs,
            )
            encoded = dict(encoded)
            rendered = tokenizer.decode(encoded["input_ids"][0], skip_special_tokens=False)
            return rendered, encoded

        if encode_mode == "tokens":
            tokenized = tokenizer.apply_chat_template(
                messages,
                tokenize=True,
                return_tensors="pt",
                truncation=True,
                max_length=max_context,
                **template_kwargs,
            )
            if hasattr(tokenized, "items") and "input_ids" in tokenized:
                encoded = dict(tokenized)
            else:
                encoded = {
                    "input_ids": tokenized,
                    "attention_mask": torch.ones_like(tokenized),
                }
            if "attention_mask" not in encoded:
                encoded["attention_mask"] = torch.ones_like(encoded["input_ids"])
            rendered = tokenizer.decode(encoded["input_ids"][0], skip_special_tokens=False)
            return rendered, encoded

        rendered = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            **template_kwargs,
        )
        encoded = tokenizer(
            rendered,
            return_tensors="pt",
            truncation=True,
            max_length=max_context,
        )
        return rendered, encoded

    rendered = format_prompt(prompt, spec, hrm_condition, baseline_format)
    encoded = tokenizer(
        rendered,
        return_tensors="pt",
        truncation=True,
        max_length=max_context,
    )
    return rendered, encoded


def hf_revision(model_id: str) -> str | None:
    try:
        return model_info(model_id).sha
    except Exception:
        return None


def load_model(model_id: str, dtype: torch.dtype | None, device: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    config = AutoConfig.from_pretrained(model_id, trust_remote_code=True)
    if getattr(config, "pad_token_id", None) is None:
        fallback_pad = tokenizer.pad_token_id or tokenizer.eos_token_id or tokenizer.bos_token_id
        if fallback_pad is not None:
            config.pad_token_id = fallback_pad

    kwargs: dict[str, Any] = {
        "trust_remote_code": True,
        "low_cpu_mem_usage": True,
        "config": config,
    }
    if dtype is not None:
        kwargs["dtype"] = dtype
    try:
        model = AutoModelForCausalLM.from_pretrained(model_id, **kwargs)
    except TypeError:
        if "dtype" in kwargs:
            kwargs["torch_dtype"] = kwargs.pop("dtype")
        model = AutoModelForCausalLM.from_pretrained(model_id, **kwargs)

    model.to(device)
    model.eval()
    return tokenizer, model


def compact_generation_config(config: GenerationConfig) -> dict[str, Any]:
    data = config.to_dict()
    return {key: data.get(key) for key in SAMPLING_KEYS if data.get(key) is not None}


def build_generation_config(
    tokenizer,
    model,
    spec: ModelSpec,
    max_new_tokens: int,
    harness_mode: str,
) -> tuple[GenerationConfig, dict[str, Any]]:
    if harness_mode == "official":
        try:
            generation_config = GenerationConfig.from_pretrained(spec.model_id, trust_remote_code=True)
            config_source = "generation_config.json"
        except Exception:
            generation_config = GenerationConfig.from_model_config(model.config)
            config_source = "model_config_or_transformers_default"
    else:
        generation_config = GenerationConfig.from_model_config(model.config)
        config_source = "legacy_uniform_greedy"

    harness = static_harness(spec, harness_mode)
    for key, value in harness["sampling_overrides"].items():
        setattr(generation_config, key, value)

    generation_config.max_new_tokens = max_new_tokens
    if generation_config.pad_token_id is None:
        generation_config.pad_token_id = tokenizer.pad_token_id
    if generation_config.eos_token_id is None:
        generation_config.eos_token_id = tokenizer.eos_token_id
    if generation_config.bos_token_id is None:
        generation_config.bos_token_id = tokenizer.bos_token_id

    metadata = {
        **harness,
        "mode": harness_mode,
        "config_source": config_source,
        "effective_generation_config": compact_generation_config(generation_config),
    }
    return generation_config, metadata


def generate_one(
    tokenizer,
    model,
    spec: ModelSpec,
    encoded: dict[str, torch.Tensor],
    device: str,
    generation_config: GenerationConfig,
) -> dict[str, Any]:
    encoded = {k: v.to(device) for k, v in encoded.items()}
    if spec.kind == "hrm":
        encoded["token_type_ids"] = torch.ones_like(encoded["input_ids"], device=device)

    start = time.time()
    with torch.inference_mode():
        output_ids = model.generate(
            **encoded,
            generation_config=generation_config,
        )
    elapsed = time.time() - start

    prompt_tokens = encoded["input_ids"].shape[1]
    continuation_ids = output_ids[0, prompt_tokens:]
    return {
        "elapsed_sec": elapsed,
        "input_tokens": prompt_tokens,
        "output_tokens": int(continuation_ids.numel()),
        "generated_text": tokenizer.decode(continuation_ids, skip_special_tokens=False),
        "full_text": tokenizer.decode(output_ids[0], skip_special_tokens=False),
    }


def write_report(path: Path, manifest: dict[str, Any], records: list[dict[str, Any]]) -> None:
    by_prompt: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        prompt_id = record.get("prompt_id", record["id"])
        by_prompt.setdefault(prompt_id, []).append(record)

    lines = [
        "# Sense Probe Run",
        "",
        f"- Started: `{manifest['started_at']}`",
        f"- Device: `{manifest['device']}`",
        f"- Dtype: `{manifest['dtype']}`",
        f"- Max new tokens: `{manifest['max_new_tokens']}`",
        "",
        "## Models",
        "",
    ]
    for model in manifest["models"]:
        lines.append(f"- `{model['key']}`: `{model['model_id']}` revision `{model.get('revision')}`")
    lines.append("")

    for prompt_id, prompt_records in by_prompt.items():
        first = prompt_records[0]
        lines.extend(
            [
                f"## {prompt_id}: {first['title']}",
                "",
                f"Category: `{first['category']}`",
                "",
                first["prompt"],
                "",
                f"Rubric note: {first['rubric']}",
                "",
            ]
        )
        for record in prompt_records:
            lines.extend(
                [
                    f"### {record['model_key']}",
                    "",
                    f"Elapsed: `{record['elapsed_sec']:.2f}s`, output tokens: `{record['output_tokens']}`",
                    "",
                    "```text",
                    record["generated_text"].strip(),
                    "```",
                    "",
                ]
            )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--model", type=parse_model_spec, action="append", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--dtype", default="auto")
    parser.add_argument("--max-context", type=int, default=4096)
    parser.add_argument("--max-new-tokens", type=int, default=180)
    parser.add_argument("--hrm-condition", default="synth,cot")
    parser.add_argument("--baseline-format", choices=("raw", "answer_suffix"), default="answer_suffix")
    parser.add_argument("--harness-mode", choices=("legacy", "official"), default="legacy")
    parser.add_argument("--seed", type=int, default=20260519)
    parser.add_argument("--run-label", default="HRM-Text Sense Probe Run")
    parser.add_argument("--comparison-stage", default="unspecified")
    args = parser.parse_args()

    prompts = load_prompts(args.prompt_file, args.limit)
    device = choose_device(args.device)
    dtype = choose_dtype(device, args.dtype)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    args.out_dir.mkdir(parents=True, exist_ok=False)
    records_path = args.out_dir / "outputs.jsonl"
    manifest_path = args.out_dir / "manifest.json"
    report_path = args.out_dir / "report.md"
    errors_path = args.out_dir / "errors.jsonl"

    manifest = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "prompt_file": str(args.prompt_file),
        "prompt_count": len(prompts),
        "device": device,
        "dtype": str(dtype),
        "max_context": args.max_context,
        "max_new_tokens": args.max_new_tokens,
        "hrm_condition": args.hrm_condition,
        "baseline_format": args.baseline_format,
        "harness_mode": args.harness_mode,
        "seed": args.seed,
        "run_label": args.run_label,
        "comparison_stage": args.comparison_stage,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "models": [
            {
                "key": spec.key,
                "model_id": spec.model_id,
                "kind": spec.kind,
                "revision": hf_revision(spec.model_id),
                "harness": static_harness(spec, args.harness_mode),
            }
            for spec in args.model
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    model_manifest = {model["key"]: model for model in manifest["models"]}

    records: list[dict[str, Any]] = []
    with records_path.open("w", encoding="utf-8") as out:
        error_out = errors_path.open("w", encoding="utf-8")
        for spec in args.model:
            try:
                tokenizer, model = load_model(spec.model_id, dtype, device)
                generation_config, harness_metadata = build_generation_config(
                    tokenizer,
                    model,
                    spec,
                    args.max_new_tokens,
                    args.harness_mode,
                )
                model_manifest[spec.key]["harness"] = harness_metadata
                manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
            except Exception as exc:
                error_out.write(json.dumps({
                    "stage": "load_model",
                    "model_key": spec.key,
                    "model_id": spec.model_id,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                }) + "\n")
                error_out.flush()
                continue

            for prompt_obj in prompts:
                try:
                    formatted, encoded = encode_prompt(
                        tokenizer,
                        prompt_obj["prompt"],
                        spec,
                        args.hrm_condition,
                        args.baseline_format,
                        model_manifest[spec.key].get("harness") or static_harness(spec, args.harness_mode),
                        args.max_context,
                    )
                    result = generate_one(
                        tokenizer,
                        model,
                        spec,
                        encoded,
                        device,
                        generation_config,
                    )
                except Exception as exc:
                    error_out.write(json.dumps({
                        "stage": "generate",
                        "model_key": spec.key,
                        "model_id": spec.model_id,
                        "prompt_id": prompt_obj["id"],
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                        "traceback": traceback.format_exc(),
                    }) + "\n")
                    error_out.flush()
                    continue

                record = {
                    **prompt_obj,
                    **result,
                    "prompt_id": prompt_obj["id"],
                    "model_key": spec.key,
                    "model_id": spec.model_id,
                    "model_kind": spec.kind,
                    "harness": model_manifest[spec.key].get("harness"),
                    "formatted_prompt": formatted,
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
                records.append(record)

            del model
            del tokenizer
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        error_out.close()

    write_report(report_path, manifest, records)
    print(f"Wrote {records_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
