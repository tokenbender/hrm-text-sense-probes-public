# HRM-Text Expanded 120-Prompt Run

This artifact contains the final expanded around-1B instruct comparison. It is
included so readers can inspect the raw outputs, the harness metadata, and the
companion diagnostics without rerunning the full job.

- Run name: `vibe-2026-expanded-120-harness-20260519T095252Z`
- Outputs: 1320 generations
- Models: 11
- Prompts: 120
- Errors: 0
- Prompt categories: 12, with 10 prompts per category

## Main Files

- `index.html`: browsable report with all prompts, raw model outputs, harness
  metadata, and benchmaxxing controls.
- `raw_prompt_by_prompt.md`: complete raw prompt-by-prompt Markdown dump.
- `diagnostics.md` / `diagnostics.json`: mechanical red-flag summaries.
- `expanded_vibe_verdict.md`: qualitative good/bad-case read.
- `hrm_text_expanded_120_report.pdf`: local PDF rendering of `index.html`.
- `manifest.json`: model revisions and effective harness/sampling metadata.
- `outputs.jsonl`: raw structured generations.
- `report.md`: remote runner's raw Markdown report.

## Shared Copy

The HTML report was also imported into Google Drive as a native Google Doc
during the original analysis:

https://docs.google.com/document/d/11pRm2qH1GiP3MoB67wG-4yIz6oSe_5sT6tLp_o8JkFw

The local PDF rendering remains in this directory as
`hrm_text_expanded_120_report.pdf`.
