# Benchmaxxing Controls For Vibe 2026

This run is still a qualitative probe, not proof of general intelligence and not
a contamination audit of every public or private training corpus. The goal is to
reduce common benchmark and synthetic-task leakage.

Controls used:

- Prompts are freshly written for this repo and contain nonce details such as
  `MOSS-41`, `QUARTZ-8`, Bay 6, North Pier, Sable review, and Orion demo.
- No prompt is copied from GSM8K, MMLU, ARC, HellaSwag, Winogrande, BoolQ,
  DROP, MATH, Minerva, BigBench, or common instruction-following suites.
- The prompt file avoids school-exam framing, multiple-choice format, "show your
  work", "let's think step by step", and generic synthetic Q/A templates.
- Baseline models receive raw prompts, not an added `Answer:` suffix.
- HRM is run with `direct`, not `synth,cot`.
- Raw outputs are preserved and read qualitatively; there is no scalar score to
  optimize against.
- Exact nonce phrase searches should be recorded before the run. Search can
  reduce visible-web reuse risk, but it cannot prove absence from all training
  corpora.

Known residual risk:

- The tasks still belong to broad capability families that are common in
  synthetic data: state tracking, contradiction detection, ambiguity handling,
  negation, and compression.
- Nonce details lower memorization risk but do not eliminate pattern learning.
- A single prompt set can be overfit after publication; future reruns should use
  newly generated canaries and paraphrase variants.

