# EU Cyber Resilience Act Readiness Skill

An open-source, agent-neutral skill that takes a software or hardware product through an evidence-backed readiness assessment against the **EU Cyber Resilience Act** (Regulation (EU) 2024/2847) and leaves the manufacturer with what it needs for its own conformity assessment: scope and classification decisions, a cybersecurity risk assessment, SBOM validation, provision-by-provision evidence, gaps with remediation, an Article 14 reporting playbook, draft technical documentation and declaration, and a formal report in Markdown, DOCX and PDF.

> **Status:** community project. Not affiliated with, endorsed by or acting for the European Commission, ENISA, any market surveillance authority, notified body or standardisation organisation. It does not perform conformity assessment, does not establish conformity or CE marking, and is not legal advice.

## Why this exists

The CRA's reporting obligations have applied since **11 September 2026** to every product with digital elements on the EU market, including products placed on the market before the main obligations start on **11 December 2027**. Fines reach EUR 15 million or 2.5 % of worldwide turnover. No harmonised standard has yet been cited in the Official Journal, so there is no presumption of conformity to lean on and every manufacturer must document its own solutions. This skill turns the regulation into something an AI coding agent can execute against a real codebase and a real organisation, with the legal text pinned and every conclusion traceable.

## What it does

- Pins the Official Journal text of the CRA, Implementing Regulation (EU) 2025/2392 (technical descriptions of important and critical products) and Delegated Regulation (EU) 2026/881 from the EU Publications Office, hashed, and generates a machine-readable catalogue of every assessable provision (96 for the pinned text).
- Carries the Commission's 27 July 2026 guidance (C(2026) 5252) and the Commission FAQ as cited, non-binding interpretive aids, and a dated register of what is still pending (standards, delegated acts, SBOM and notification format acts).
- Decides scope, economic-operator role, remote-data-processing boundary and date regime with confidence levels and a legal-confirmation flag.
- Classifies the product by core functionality against the implementing regulation's technical descriptions and states which Article 32 conformity routes are legally available today.
- Structures the Article 13 cybersecurity risk assessment, including the per-requirement applicability statements the technical documentation must contain.
- Validates SBOMs (CycloneDX and SPDX) against the legal minimum and recommended practice, and reconciles them with lockfiles.
- Assesses all Annex I Part I and Part II requirements, Article 13 and 14 obligations, Annex II user information, Annex VII technical documentation and Annex V declaration content, with an interpretive guide per provision.
- Tests Article 14 reporting readiness, computes 24-hour, 72-hour and final-report deadlines, and supports tabletop drills.
- Screens change sets for substantial modification using the Commission's four-factor test.
- Produces drafts of the technical documentation, EU declaration of conformity (unsigned), user information, CVD policy, security.txt, support-period statement and reporting playbook.
- Produces gaps with stable regression keys, a ticket queue, regression CI comparison and a formal report with mandatory disclaimers.

## Quick start

1. Clone this repository:

   ```bash
   git clone https://github.com/Killerz007/cra-readiness-skill.git
   ```

2. Install it where your agent will find it (table below), or give the agent access to both this repository and the product repository.

3. Ask the agent:

   ```text
   Use the CRA Readiness Skill to perform a complete Cyber Resilience Act readiness assessment of this product. Follow SKILL.md exactly. Use the pinned official texts as criteria, preserve raw evidence, and produce the complete assessment package. Do not claim conformity, CE marking or legal advice.
   ```

   If the agent cannot load skills or instruction files, paste [`prompts/portable-agent-prompt.md`](prompts/portable-agent-prompt.md).

### Install per agent

| Agent | Where it looks | What to do |
|---|---|---|
| Claude Code | `~/.claude/skills/<name>/SKILL.md` or `<product>/.claude/skills/<name>/SKILL.md` | Clone this repo to `~/.claude/skills/cra-readiness`. Optionally copy `.claude/commands/cra-audit.md` into the product's `.claude/commands/`. |
| OpenAI Codex and other `AGENTS.md` readers | `<product>/AGENTS.md` | Add the one-line pointer from `adapters/ai-compatibility.md`, or copy this repo's `AGENTS.md`. |
| Cursor | `<product>/.cursor/rules/*.mdc` | Copy `.cursor/rules/cra-readiness.mdc` into the product repo. |
| GitHub Copilot, Gemini CLI, Windsurf | `.github/copilot-instructions.md`, `GEMINI.md`, `.windsurfrules` | Add the one-line pointer. |
| Agent Skills loaders | the tool's skills directory | Install as `cra-readiness`. |
| ChatGPT and web agents with GitHub access | none | Give the repository URL and use the portable prompt. |

## Modes

`scope`, `classify`, `full` (default), `delta` (substantial-modification screening), `retest`, `regression`, `reporting-drill`, `evidence-pack`. See `SKILL.md` section 4.

## Expected output

```text
cra-assessment/2026-10-06-example-sensor-hub-3-1-0/
  00-assessment-manifest.json
  01-executive-summary.md
  02-scope-determination.md  02-scope-decision.json
  03-classification-and-route.md  03-classification-decision.json
  04-product-architecture.md
  05-sbom/  05-sbom-check.json  05-component-due-diligence-register.csv
  06-cybersecurity-risk-assessment.md
  07-requirement-matrix.csv
  08-evidence-index.csv  09-scanner-register.csv  10-adjudication-log.jsonl
  11-gaps-register.jsonl  11-detailed-gaps.md  12-remediation-register.csv
  13-technical-documentation-draft.md
  14-eu-declaration-of-conformity-DRAFT.md
  15-user-information-annex-ii.md
  16-cvd-policy-draft.md  security.txt
  17-support-period-statement.md
  18-article-14-reporting-playbook.md  18-reporting-drill-record.json
  19-test-procedure-traceability.csv
  20-cra-readiness-report.md  .docx  .pdf
  21-report-rendering-manifest.json
  22-finding-ticket-queue.json  .md
  23-regression-summary.json  .md        # regression mode
  24-retest-results.md                   # retest mode
  25-substantial-modification-screening.json  .md   # delta mode
  evidence/raw  normalized  screenshots  runtime  code
```

The conclusion is one of: **Ready for conformity assessment** (with the route), **Not ready**, **Assessment incomplete**, **Outside CRA scope as assessed**, or **Reporting obligations only**. It is never "CRA compliant" or "CE marked".

## Scripts

| Script | Purpose |
|---|---|
| `scripts/sync_official_text.py` | Fetch, pin and parse the official texts (`--sync`, `--check`, `--rebuild-local`) |
| `scripts/validate_repo.py` | Integrity checks: hashes, catalogue counts, guide coverage, schemas, examples |
| `scripts/init_assessment.py` | Create an assessment directory and manifest |
| `scripts/classify_product.py` | Scope decision and classification decision from structured answers |
| `scripts/screen_substantial_modification.py` | Four-factor substantial-modification screening |
| `scripts/check_sbom.py` | CycloneDX and SPDX validation and lockfile reconciliation |
| `scripts/reporting_deadlines.py` | Article 14 deadline calculator |
| `scripts/support_period_check.py` | Article 13(8), (9), (13), (18) checks and retention dates |
| `scripts/compare_assessments.py` | Regression comparison against an accepted baseline |
| `scripts/export_ticket_queue.py` | Portable GitHub or Jira ticket queue from the gaps register |
| `scripts/hash_evidence.py` | SHA-256 index of an evidence directory |

Run `make validate` to execute the validator and the test suite.

## Legal sources and currency

Everything legal is dated in [`references/legal-status-and-dates.md`](references/legal-status-and-dates.md). The pinned baseline is recorded in [`official/upstream-manifest.json`](official/upstream-manifest.json). A monthly workflow re-fetches the official texts from the Publications Office and opens a review pull request when a pinned document changes. Harmonised standards status, secondary legislation and the ENISA reporting platform are time-sensitive and are re-verified at the start of every assessment.

## Sample

[`examples/sample-assessment/`](examples/sample-assessment/) is a fictional fixture used by the tests and usable as a trial baseline. [`examples/sanitized-assessment-summary.md`](examples/sanitized-assessment-summary.md) shows the shape of a finished assessment.

## Licensing

Original content is licensed under Apache-2.0. EU legal texts and Commission documents in `official/current/` are reused under the Commission's reuse policy (Decision 2011/833/EU) and the EUR-Lex copyright notice, with attribution; only the Official Journal is authentic. See `NOTICE`.
