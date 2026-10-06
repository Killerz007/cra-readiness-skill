# Regression and CI

A full readiness assessment cannot be reduced to a CI job. Regression CI detects changes against an accepted baseline and forces targeted re-assessment; it never carries a CONFORMANT status forward on its own.

## Baseline

After the product owner accepts a completed assessment, retain: `00-assessment-manifest.json`, `07-requirement-matrix.csv`, `11-gaps-register.jsonl`, the SBOM and its check report, and the repeatable scripts for the provisions chosen for CI.

## CI workflow for a new version

1. Regenerate and validate the SBOM; run SCA, SAST, secrets and configuration checks approved for CI.
2. Run the substantial-modification screening questions against the change set (manual or scripted answers).
3. Produce the current matrix and gaps register for the provisions actually re-checked.
4. Compare with `scripts/compare_assessments.py`.
5. Fail on configured regressions: CONFORMANT to GAP, BLOCKED or NOT_ASSESSED; NOT_APPLICABLE to GAP; reopened or new gaps at or above the severity threshold; loss of required evidence; a screening that indicates a substantial modification.
6. Require human review for scope, classification or legal-baseline changes (a changed pinned source hash, a cited harmonised standard appearing, a new delegated act).

## What CI must not do

Assume unchanged code means unchanged conformance; treat absence of scanner alerts as CONFORMANT; promote BLOCKED or NOT_ASSESSED; reuse evidence from another environment undocumented; claim the product is CRA conformant or CE marked.

## Target repository layout

```text
.cra/
  baseline/   00-assessment-manifest.json, 07-requirement-matrix.csv, 11-gaps-register.jsonl, sbom/
  current/    same files for the new version
  regression/ regression-summary.json, regression-summary.md
```

Use `templates/ci/cra-regression.yml` as a starting point and replace the project-specific scanner step.
