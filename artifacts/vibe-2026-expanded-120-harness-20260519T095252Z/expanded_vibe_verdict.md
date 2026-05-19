# Expanded 120-Prompt Vibe Verdict

Run: `vibe-2026-expanded-120-harness-20260519T095252Z`

This is a qualitative read over the raw run, not a hidden benchmark score. The
run completed cleanly: 120 unique prompts, 11 models, 1320 generations, 0
errors. The prompt set expands the original 12 nonce probes into 12 areas with
10 unique questions per area and has no exact prompt overlap with the original
12-prompt file.

## Harness Notes

- All models used the registered official harness path recorded in
  `manifest.json` and the HTML harness table.
- The Qwen3 rows use the official/default thinking chat path. Under a 256-token
  answer cap this often emits reasoning without a final answer. That is a
  behavior finding for this short-answer probe, not an adapter failure.
- Raw decoding intentionally preserves stop markers such as `<|im_end|>`,
  `<|box_end|>`, and `</s>`. The diagnostics count those as
  `special_token_leak`; use that as an output-cleanliness flag rather than a
  correctness score.

## Broad Verdict

HRM-Text-1B is not fast in generated-token throughput in this run. It often
looks quick at the prompt level because it emits very short answers: 17.2 output
tokens on average, with a 1.7 second median latency. Its decoded throughput was
about 5 output tokens per second. The stronger standard Transformer rows
usually decoded around 20 to 37 output tokens per second while producing longer
and more useful answers. The throughput measure is `output_tokens / generate
elapsed_seconds`, so it includes short-prompt prefill cost rather than isolating
only the final decode loop.

On quality, HRM sometimes lands the core state update, but it is too brittle
for general English sense checking. It collapses to one token in several
ordinary prompts (`A`, `Door 2`, `Bo's`, `inbox`) and often drops required
exceptions or the second half of a question. It looks more like a terse pattern
extractor than a robust instruction-following text model.

The failure pattern differs from the regular Transformer rows. The standard
instruct models tend to fail by overexplaining, drifting, echoing the prompt, or
adding plausible but unsupported context. HRM more often fails by compression:
it selects a nearby answer-shaped fragment and stops before preserving the full
instruction or all constraints.

## Where HRM Looked Useful

HRM's best pocket was short-answer extraction. It was strongest when the task
asked for the first matching item, one failed check, one room assignment, or one
current status. In the stop-condition group, the HRM row matched the expected
short answer on all ten prompts by manual read: `Shelf B`, `Door 2`, `blue`,
`B`, `Kit 2`, `10`, `box B`, `Towel 2`, `south`, and `latch failed`.

It also handled several compact update/status prompts. Good examples include
the walnut tart allergen correction, the Room E / Room F setup edit, the Vera /
MOSS shipment-status swap, and the current invoice-recipient prompt where
`Mira` was the needed answer.

That strength did not look unique for its weight class in this run. The better
standard Transformer instruct rows usually matched those easy extraction wins
and were much better when the prompt required explanation, multiple
constraints, epistemic restraint, or reference tracking. The interesting HRM
signal is therefore not "better small model." It is a distinctive operating
profile: short, decisive, sometimes exactly right, and often prematurely
compressed.

Among the around-1B instruct comparators, the strongest practical rows came
from SmolLM2-1.7B-Instruct, LFM2.5-1.2B-Instruct, Qwen2.5-1.5B-Instruct, and
Falcon3-1B-Instruct, depending on the area. SmolLM2 had the best compact
follow-through vibe for mundane state/update/reference prompts. LFM2.5 and
Qwen2.5-1.5B were often more explanatory and coherent, but both over-expanded
and sometimes drifted. Falcon3 was useful but verbose and frequently hit the
token cap. Qwen2.5-0.5B, TinyLlama, and Danube3-500M were visibly weaker on
state, ambiguity, and stop-condition probes. Danube2-1.8B was coherent but
often overclaimed or added irrelevant rationale.

Qwen3-0.6B and Qwen3-1.7B should not be compared as plain short-answer models
from this artifact without acknowledging the official thinking harness. They
mostly spent the budget in `<think>` and often never reached the answer. That
may be the official harness, but it is a poor fit for these short, exact-answer
vibe probes at `max_new_tokens=256`.

## Good Cases

- `exp_state_05` / Notebook Under Scale: SmolLM2 answered the physical state
  correctly and compactly: notebook under the scale spot, timer on the empty
  spot. HRM moved the notebook to the counter and put the timer "in the scale";
  Qwen2.5-0.5B drifted into generic possibilities.
- `exp_update_02` / Poster Approval Revision: SmolLM2 and LFM2.5 cleanly used
  the later correction: email banner approved, poster still needs Camila. HRM
  collapsed to `A`; Danube3 and Falcon initially repeated the stale broad
  approval.
- `exp_compress_01` / Lab Door Rule: LFM2.5, Falcon3, SmolLM2, and
  Qwen2.5-1.5B preserved the closure time, freezer-alarm exception, visitor
  ban, and log code. HRM omitted the required log code.
- `exp_ref_04` / Badge Clip: SmolLM2, Falcon3, and LFM2.5 got both references:
  Bo's visitor badge is on Bo's jacket, and Cy took Ana's cracked badge.
- `exp_stop_02` / First Unlocked Door: HRM, SmolLM2, Qwen2.5, Falcon3, LFM2.5,
  and Danube2 answered Door 2. Danube3 said Door 3 and TinyLlama said Door 1.

## Bad Cases

- HRM brittleness: 58 of 120 HRM outputs were mechanically flagged as
  `too_terse`. Examples include `exp_update_02` -> `A`, `exp_boundary_01` ->
  `A`, `exp_ref_04` -> `Bo's`, and `exp_state_08` -> `headphones`. These are
  not just style misses; they often fail the requested answer shape.
- Thinking-model budget loss: Qwen3-0.6B hit the token cap on 111/120 rows and
  had 103 unfinished thinking rows; Qwen3-1.7B hit the cap on 117/120 rows and
  had 115 unfinished thinking rows. On `exp_stop_02`, both reason through the
  door sequence but do not deliver the required exact answer within the budget.
- Prompt echo and instruction-boundary weakness: Danube3-500M had 17 prompt-echo
  flags and frequently repeated the problem text instead of answering. In
  `exp_update_02`, it preserved the stale "approved by Jules" status despite
  the correction.
- Causal-sense overgeneration: causal prompts produced the highest token-cap
  pressure. Many models named a broad "scanner malfunction" but missed the
  intended cold-start/warmup/calibration mechanism, as in `exp_cause_01`.
- Epistemic restraint remained hard. On `exp_epistemic_01`, most models
  overclaimed that payment was actually received. The safer answer is only that
  the subject line says so; the body/payment system still need checking. HRM
  even changed `LARK-5` to `EBR-5`.

## Area Read

- Stronger areas: simple stop conditions, simple update handling, and
  single-step state tracking when the answer shape is obvious.
- Mixed areas: compression and style control. Stronger instruct models preserve
  constraints; HRM and small baselines often drop one required clause or add
  extra explanation.
- Weak areas: instruction boundaries, causal diagnosis, epistemic restraint,
  and reference resolution with multiple possessives. These expose whether the
  model is tracking the sentence meaning or just producing a plausible support
  response.

## Files To Inspect

- HTML report: `index.html`
- Complete raw dump: `raw_prompt_by_prompt.md`
- Mechanical diagnostics: `diagnostics.md` and `diagnostics.json`
- Original remote raw report: `report.md`
