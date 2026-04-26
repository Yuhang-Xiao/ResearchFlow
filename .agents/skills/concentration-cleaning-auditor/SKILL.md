---
name: concentration-cleaning-auditor
description: Audit and repair contaminant concentration cleaning before MOE/EDI, POMDP, belief-MDP, DQN, or risk reporting. Use for AFB1 detection, pollutant label verification, detection-value parsing, regulatory-limit parsing, unit normalization, exceedance labels, exceedance multiples, manual-review flags, concentration distribution summaries, and downstream impact checks.
---

# Concentration Cleaning Auditor

## When To Trigger

Use this skill before any downstream task that relies on concentration values, AFB1 labels, exceedance flags, exposure assessment, or risk states.

## Pollutant And AFB1 Checks

- Search source text fields for AFB1 variants: `黄曲霉毒素B₁`, `黄曲霉毒素B1`, `黄曲霉毒素B`, `黄曲霉毒素 B₁`, `黄曲霉毒素B₁μg/kg`, `黄曲霉毒素B₁，µg/kg`, initial/retest descriptions, `黄曲霉`, `AFB`, `B₁`, and reasonable `B1` variants.
- Do not classify every `生物毒素` record as AFB1. Require AFB1-specific context or mark it for manual review.
- Compare detected candidates against existing `是否AFB1相关` and `AFB1识别依据`.

## Detection Value Parsing

Verify that `检测数值` preserves the original value and parses initial-test value, retest value, final adopted value, numeric value, unit, parsing status, and parsing-failure reason.

Handle simple values, empty values, `/`, `合格`, `未检出`, mixed multi-project text, and initial/retest patterns such as `初检结果：128μg/kg复检结果：51.8μg/kg`. Prefer retest value for final adopted concentration when it is available and parseable.

## Regulatory Limit Parsing

Verify `法规限制` parsing for original limit text, numeric value, unit, comparison operator, and whether the unit was inferred from context. Handle `≤20μg/kg`, `≤20µg/kg`, `20μg/kg`, `20µg/kg`, `≤20`, `20`, whitespace, and line breaks.

For AFB1, infer `μg/kg` for numeric-only limits only when the pollutant context is clearly AFB1 and record that inference.

## Unit, Exceedance, And Multiples

- Normalize AFB1 concentration and limit units to `μg/kg` when possible.
- Compute `是否超标` by comparing normalized final concentration and normalized limit before falling back to judgment text.
- Compute `超标倍数` from normalized values only.
- Cross-check parsed exceedance against original `判定结果`; conflicts should be flagged for review.

## Manual Review And Issue Logs

Flag records when AFB1 is suspicious but not certain, concentration cannot be parsed, limit cannot be parsed, units are incompatible, exceedance conflicts with judgment, or multi-project values cannot be safely separated.

Do not silently drop important records.

## Regeneration And Downstream Impact

If repairs change AFB1 labels, final concentration, limits, exceedance labels, or counts, regenerate affected concentration tables, concentration distribution summaries, issue logs, cleaning reports, count panels, Beta-Binomial states, and belief-MDP state features as needed.

If downstream artifacts do not need regeneration, explain why in the verification report.
