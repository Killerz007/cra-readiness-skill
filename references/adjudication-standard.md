# Evidence adjudication standard

Adjudication prevents the last reviewer, tool or agent to run from silently overriding stronger contradictory evidence, and it records the reasoning behind borderline legal-technical decisions.

## When adjudication is mandatory

1. Static review and runtime behaviour conflict.
2. Tools or reviewers disagree on exploitability, applicability or status.
3. A material scanner finding is proposed as a false positive.
4. CONFORMANT depends on indirect or incomplete evidence.
5. A NOT_APPLICABLE decision is disputed or changes the readiness conclusion.
6. A GAP, BLOCKED or NOT_ASSESSED provision is proposed to become CONFORMANT without self-evident new evidence.
7. Scope, role or classification is borderline, or the user disagrees with the assessed outcome.
8. A substantial-modification screening is contested.
9. A regression comparison shows a material change needing interpretation.

## Evidence precedence

No automatic "runtime wins" rule. Weigh: the exact legal text and the Commission guidance; representativeness of the tested environment and version; whether source evidence covers all paths; whether runtime tests exercised the relevant interface, role or remote component; tool reliability; timing and version of evidence; compensating controls and whether they satisfy the text.

## Independence

Prefer a fresh reviewer or agent context (`agents/conformity-reviewer.md`). Where only one context exists, perform a second-pass challenge review and record the limitation.

## Decision rules

Allowed outcomes: CONFORMANT, GAP, NOT_APPLICABLE, BLOCKED, NOT_ASSESSED, or for scope and classification the specific decision with confidence. Unreconciled contradiction never yields CONFORMANT. Dismissing a scanner finding requires the reasoning, the compensating or framework behaviour relied on, and the evidence; the original finding is preserved and linked.

## Record

Use `schemas/adjudication-record.schema.json`; append to `10-adjudication-log.jsonl`; reference the adjudication ID from affected matrix rows, gaps and decision records.
