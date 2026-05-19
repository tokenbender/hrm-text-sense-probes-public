# Expanded Prompt Taxonomy

The 120-prompt suite expands the original 12 nonce probes into 10 unique
questions per area. It is mined from the observed good and bad cases in the
post-trained comparison: where models were strong, the expansion asks for
repeat evidence; where models failed, it varies the surface form so the run does
not test the exact same trick twice.

## Areas

| Area | Prior signal | Expansion target |
| --- | --- | --- |
| `state_tracking` | HRM, SmolLM2, and Qwen were good; Llama and OLMo moved objects with nearby containers. | Vary labels, lids, photos, hooks, trays, and moved objects. |
| `update_handling` | All loadable models handled the simple correction. | Check partial overrides, swapped roles, old-note invalidation, and safety-critical corrections. |
| `instruction_boundaries` | HRM collapsed; Llama partly followed quoted bad text; OLMo was strongest. | Vary quoted commands in transcripts, labels, forms, forwarded email, and object text. |
| `causal_sense` | Larger instruct models were best; small models sometimes invented wrong mechanism classes. | Test recurrence after interventions and condition-linked faults. |
| `ambiguity` | Strong models asked clarification; weak rows collapsed nearby meanings. | Use workplace polysemy without repeating the original seal-crate challenge. |
| `negation` | Most instruct models handled the anchor; HRM was terse. | Add unless, only-if, not-both, exception, and current-status variants. |
| `epistemic_restraint` | SmolLM2 overclaimed payment; OLMo sometimes overstated what was known. | Use limited observations where the answer must separate known, unknown, and next check. |
| `compression` | Qwen and OLMo preserved exceptions; HRM lost an exclusion. | Stress one-sentence compression with bans, exceptions, and log codes. |
| `contradiction_detection` | HRM and OLMo handled the anchor; others invented pickup events. | Vary conflict pairs where the safe assumption must preserve possible current location. |
| `style_control` | Many models obeyed the simple shape; weak rows had plausibility drift. | Add exact count, banned words, short notices, and exact-format constraints. |
| `reference_resolution` | The badge-swap anchor was broadly hard. | Vary possessives and old/spare/expired object distinctions. |
| `stop_condition` | Qwen and OLMo obeyed best; smaller rows missed tray/reason constraints. | Test first-match, missing-item, exact-answer, and stop-after-answer behavior. |

## Controls

- 120 prompts total.
- 10 prompts per category.
- No prompt text duplicates inside the expanded file.
- No prompt text duplicates from the original 12-prompt file.
- Names, codes, and objects are nonce/mundane rather than drawn from common
  benchmark tasks.
