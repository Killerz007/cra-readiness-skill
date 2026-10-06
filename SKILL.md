---
name: cra-readiness
version: 1.0.0
description: >
  Evidence-backed readiness assessment of a software or hardware product against the EU
  Cyber Resilience Act, Regulation (EU) 2024/2847, using the pinned Official Journal text,
  Implementing Regulation (EU) 2025/2392 and the Commission's 2026 guidance. Use when the
  user mentions the CRA, Cyber Resilience Act, CE marking for software, products with
  digital elements, Annex I essential requirements, SBOM obligations, vulnerability
  handling, the 11 September 2026 reporting duty, ENISA single reporting platform,
  support period, substantial modification, important or critical products, or asks to
  prepare technical documentation or an EU declaration of conformity. Produces scope and
  classification decisions, a cybersecurity risk assessment, requirement-by-requirement
  evidence, gaps with remediation, an Article 14 reporting playbook, draft technical
  documentation and a formal readiness report. Never claims conformity, CE marking or
  legal advice.
---

# CRA Readiness Assessment Skill

## 1. Purpose

Use this skill when a manufacturer, developer, importer, distributor or open-source steward wants to know where a product with digital elements stands against the EU Cyber Resilience Act (CRA) and what must change before it can be placed on the EU market, or before the manufacturer can answer a market surveillance authority, a notified body or a customer.

This is an **independent readiness methodology**. It is not a conformity assessment, not a notified-body service, not legal advice, and it never results in CE marking. The manufacturer alone signs the EU declaration of conformity under its sole responsibility (Article 28(4)).

## 2. Non-negotiable principles

1. **Official text first.** The pinned Official Journal text of Regulation (EU) 2024/2847, Implementing Regulation (EU) 2025/2392 and Delegated Regulation (EU) 2026/881 are the criteria. Commission guidance C(2026) 5252 and the Commission FAQ are interpretive aids and are cited as non-binding. Blog posts, vendor material and training content are never criteria.
2. **Pin the law and the product.** Record the source hashes from `official/upstream-manifest.json`, the date-sensitive status checks in `references/legal-status-and-dates.md`, and the exact product version, commit, build artefacts, deployment and remote data processing solutions assessed.
3. **Scope before anything else.** No requirement is assessed until the product is confirmed to be a product with digital elements in scope, the economic-operator role is identified, and the applicable date regime (Article 69 and 71) is recorded. Scope and classification decisions carry a confidence level and, where the facts are borderline, a `legal_confirmation_recommended` flag.
4. **Risk assessment drives applicability.** Annex I Part I point (2) requirements apply "on the basis of the cybersecurity risk assessment and where applicable" (Article 13(3)). A requirement is marked not applicable only with a written justification that will go into the technical documentation (Article 13(4)). Part II vulnerability-handling requirements and Article 13 and 14 obligations are not optional.
5. **No conformant status without evidence.** A provision is CONFORMANT only when evidence directly shows the legal text is satisfied for this product version. A clean scanner, a policy document that is not enforced, or a plan is not evidence of conformance.
6. **Dynamic requirements need dynamic evidence.** Secure-by-default, update mechanisms, access control, logging, data deletion and denial-of-service resilience are verified on the built product or a representative environment, not inferred from source alone, unless the risk assessment justifies otherwise.
7. **Reporting readiness is live.** Article 14 applies from 11 September 2026 to every in-scope product, including products placed on the market before 11 December 2027. A `full` assessment always tests the reporting process, not just the product.
8. **No destructive testing.** Follow `references/authorized-testing.md`.
9. **Preserve evidence.** Raw tool output, SBOMs, requests and responses, screenshots and code references are hashed and indexed.
10. **Adjudicate conflicts.** Contradictory evidence, challenged not-applicable decisions and status upgrades are resolved through `references/adjudication-standard.md`, preferably by a fresh reviewer context.
11. **Separate readiness from conformity.** The report uses the conclusions in section 20. It never says "CRA compliant", "CE marked", "certified" or "approved".
12. **Separate tracking from closure.** Gaps go to a local ticket queue by default; external tickets only with explicit authorisation; ticket closure never closes a gap.
13. **Professional deliverables.** `full`, `retest` and `evidence-pack` runs render the report as Markdown, DOCX and PDF from one frozen source, using the environment's document tooling or the fallback toolchain in `references/report-artifact-generation.md`.
14. **Drafts are drafts.** The technical documentation outline, the EU declaration of conformity and the user information are produced as clearly marked drafts for the manufacturer to complete, review with counsel and sign. The skill never produces a signed declaration or affixes a CE marking.

## 3. Required reading by mode

Read each file once. Do not load the 700 KB XHTML into context; use the generated JSON and open `official/current/` only to quote exact wording.

**Every mode:**

1. `official/upstream-manifest.json`
2. `references/legal-status-and-dates.md`
3. `references/scope-determination.md`
4. `references/economic-operator-roles.md`
5. `references/assessment-methodology.md`
6. `references/evidence-standard.md`

**`classify`, `full`, `delta`, `retest`, `evidence-pack`:** add

7. `references/product-classification.md`
8. `references/conformity-assessment-routes.md`
9. `references/harmonised-standards-status.md`
10. `references/cra-product-categories.generated.json`

**`full`, `retest`, `evidence-pack`:** add

11. `references/risk-assessment-methodology.md`
12. `references/requirement-assessment-guide.json` (one entry per provision: what it means, evidence expected, test methods, common gaps)
13. `references/cra-requirements-catalog.generated.json` (verbatim text; consult the entry for each provision as you assess it)
14. `references/sbom-standard.md`, `references/vulnerability-handling.md`, `references/reporting-obligations.md`, `references/support-period.md`, `references/technical-documentation.md`
15. `references/authorized-testing.md`, `references/scanner-matrix.md`, `references/severity-methodology.md`, `references/adjudication-standard.md`
16. `references/reporting-standard.md`, `references/report-design.md`, `references/report-artifact-generation.md`, `references/ticket-integration.md`

**`delta`:** add `references/substantial-modification.md`.
**`reporting-drill`:** add `references/reporting-obligations.md` and `templates/article-14-reporting-playbook.md`.
**`regression`:** add `references/regression-ci.md`.
**Open-source products or components:** add `references/open-source.md`.
**Any cloud, backend or companion service:** add `references/remote-data-processing.md`.

If the upstream check is older than 45 days and the network is available, run:

```bash
python scripts/sync_official_text.py --check
```

Exit code 2 means a pinned source changed: stop, record it, and continue only against the pinned baseline with the discrepancy disclosed. Offline, rebuild catalogues with `python scripts/sync_official_text.py --rebuild-local`.

## 4. Assessment modes

- `scope`: scope, role, date regime and remote-data-processing determination only. Output: `02-scope-determination.md`, `02-scope-decision.json`.
- `classify`: `scope` plus product classification and conformity-route options. Output adds `03-classification-and-route.md`, `03-classification-decision.json`.
- `full`: the complete readiness assessment and deliverable package (default).
- `delta`: substantial-modification screening of a change set against a previously assessed baseline, plus the list of provisions that need re-assessment.
- `retest`: re-verify previously open gaps and blocked provisions.
- `regression`: compare the current repeatable results with an accepted baseline (CI).
- `reporting-drill`: tabletop exercise of the Article 14 process with a fictional scenario, producing timed evidence of readiness.
- `evidence-pack`: normalise existing material into the formal package without claiming unperformed work.

Default to `full` unless the user clearly asks for another mode.

## 5. Phase 0: access, authorisation and baseline

1. Confirm read access to the full source, build configuration, infrastructure-as-code, release pipeline and any remote data processing solution. Record inaccessible areas.
2. Record product name, type and version, repository and commit SHA, build identifiers, firmware or package hashes, and the target environment.
3. Identify the economic operator the user represents (manufacturer, authorised representative, importer, distributor, steward, modifier under Article 21 or 22).
4. Confirm authorisation for runtime testing. Without it, perform source and configuration review only and mark runtime-dependent provisions BLOCKED.
5. Run `python scripts/sync_official_text.py --check` where the network allows; record the result and the time-sensitive status checks from `references/legal-status-and-dates.md`.
6. Create the assessment directory with `python scripts/init_assessment.py` and complete `00-assessment-manifest.json` (schema in `schemas/assessment-manifest.schema.json`).

## 6. Phase 1: scope determination

Follow `references/scope-determination.md`. Decide and document, with article citations, confidence and evidence:

1. Is it a **product with digital elements** (Article 3(1)) with a direct or indirect data connection (Article 2(1))? Standalone software, hardware with embedded software, standalone hardware, or a combination. Web applications accessed only through a browser are not themselves products with digital elements (guidance points 20 to 21).
2. Is it **made available on the EU market in the course of a commercial activity** (Article 3(21) and (22))? For free and open-source software apply the commercial-activity tests in `references/open-source.md`.
3. Does any **exclusion** apply (Article 2(2) to (7): medical devices, in vitro diagnostics, vehicles, civil aviation, marine equipment, spare parts, national security or defence)?
4. Which **remote data processing solutions** form part of the product (Article 3(2); guidance section 8)?
5. Which **date regime** applies: placed on the market before or after 11 December 2027; Article 69(2) substantial-modification trigger; Article 69(3) reporting applies regardless.
6. Are any **components** placed on the market separately and therefore products in their own right?

Record the outcome with `python scripts/classify_product.py --answers <json> --stage scope`. If the product is out of scope, produce the scope report, state the reasoning and the residual Article 14 position, and stop unless the user asks to continue voluntarily.

## 7. Phase 2: classification and conformity route

Follow `references/product-classification.md` and `references/conformity-assessment-routes.md`.

1. Identify the product's **core functionality** (guidance points 139 to 145) and compare it with the technical descriptions in Implementing Regulation (EU) 2025/2392 (`references/cra-product-categories.generated.json`).
2. Classify as default, important class I, important class II, or critical. Integration of an important component does not by itself make the product important (Article 7(1)). Modules sold separately are classified separately (guidance point 145).
3. Record the **conformity assessment routes available** under Article 32 and the status of harmonised standards. As of the pinned status no harmonised standard is cited in the OJEU, so important class I products cannot use module A self-assessment unless that changes (Article 32(2)). Free and open-source products in Annex III categories may use module A if the technical documentation is public (Article 32(5)).
4. Produce `03-classification-and-route.md` and `03-classification-decision.json` with `python scripts/classify_product.py --answers <json> --stage classify`.

## 8. Phase 3: product discovery and architecture

Document in `04-product-architecture.md`: components and their suppliers, languages and frameworks, interfaces and protocols, trust boundaries, data flows and data categories, authentication and authorisation, cryptography, update mechanism and signing, logging, remote data processing solutions and third-party services, build and release pipeline, hardware security features, and the deployment environments. Generate or obtain the SBOM (Phase 5).

## 9. Phase 4: cybersecurity risk assessment (Article 13(2) to (4))

Follow `references/risk-assessment-methodology.md`. Produce `06-cybersecurity-risk-assessment.md` containing: intended purpose, reasonably foreseeable use and misuse, operational environment and assets, expected time in use, threat scenarios, risk evaluation, the applicability decision and implementation statement for every Annex I Part I point (2) requirement, how point (1) and Part II are applied, residual risk, and the due-diligence record for third-party and open-source components (Article 13(5)). A pre-existing risk assessment is reviewed against the same structure rather than rewritten.

## 10. Phase 5: SBOM and component evidence

Follow `references/sbom-standard.md`. Obtain or generate an SBOM in CycloneDX or SPDX, validate it with `python scripts/check_sbom.py`, and reconcile it with the lockfiles and build outputs. Run software composition analysis and check known exploitable vulnerabilities against the EU vulnerability database, CISA KEV and vendor advisories. Record the component due-diligence register.

## 11. Phase 6: provision-by-provision assessment

Assess every provision in `references/cra-requirements-catalog.generated.json` using the matching entry in `references/requirement-assessment-guide.json`:

- Annex I Part I (1) and (2)(a) to (m): product properties.
- Annex I Part II (1) to (8): vulnerability-handling processes.
- Article 13 paragraphs: manufacturer obligations (support period, documentation retention, identification, contact point, user information, declaration, corrective action, cessation).
- Article 14: reporting readiness.
- Annex II: user information and instructions.
- Annex VII: technical documentation content.
- Annex V: declaration of conformity content.

Allowed statuses: `CONFORMANT`, `GAP`, `NOT_APPLICABLE` (with Article 13(4) justification), `BLOCKED`, `NOT_ASSESSED`. Record for each provision the test method, evidence IDs, gap IDs and adjudication IDs in `07-requirement-matrix.csv`. No provision may be missing from the matrix.

## 12. Phase 7: testing

Use the methods in `references/scanner-matrix.md` and `references/authorized-testing.md`. At minimum: SBOM validation and SCA; SAST; secret scanning; configuration review of defaults, exposed services, debug interfaces and credentials; update-mechanism verification (integrity, authenticity, transport, rollback behaviour, automatic update default and opt-out where applicable); access-control and logging checks; data deletion and reset; cryptography review; denial-of-service resilience review proportionate to the product; and a check that the vulnerability contact point, CVD policy and advisory channel actually work. Store raw output under `evidence/raw/` with hashes.

## 13. Phase 8: Article 14 reporting readiness

Follow `references/reporting-obligations.md`. Verify: single reporting platform registration (Primary Assigned Representative with EU Login and multi-factor authentication), the CSIRT designated as coordinator for the manufacturer's main establishment or the Article 14(7) fallback order, the written awareness-to-notification procedure with 24-hour, 72-hour and final-report steps, the user-information step under Article 14(8), templates, on-call coverage, and evidence of at least one drill. Use `python scripts/reporting_deadlines.py` to compute deadlines in drills.

## 14. Phase 9: adjudication

Follow `references/adjudication-standard.md`. Adjudicate when evidence conflicts, when a not-applicable decision changes the outcome, when a GAP or BLOCKED provision is proposed to become CONFORMANT, or when scope or classification is borderline. Append records to `10-adjudication-log.jsonl`.

## 15. Phase 10: gaps and remediation

Create a gap for every GAP provision and every material weakness (`schemas/gap.schema.json`): stable `regression_key`, provisions affected, rating per `references/severity-methodology.md`, legal exposure, evidence, remediation with concrete technical change, documentation change, retest criterion and target date relative to the applicable legal deadline. Write `11-gaps-register.jsonl`, `11-detailed-gaps.md`, `12-remediation-register.csv`.

## 16. Phase 11: documentation drafts

Produce, as marked drafts, from the templates: `13-technical-documentation-draft.md` (Annex VII structure, with every item either filled from evidence or marked TO COMPLETE), `14-eu-declaration-of-conformity-DRAFT.md` (Annex V structure, unsigned), `15-user-information-annex-ii.md`, `16-cvd-policy-draft.md` plus `security.txt`, `17-support-period-statement.md` (with `python scripts/support_period_check.py`), and `18-article-14-reporting-playbook.md`.

## 17. Phase 12: retest, delta and regression

- `retest`: rerun the original failing check for each gap; statuses Closed, Partially Remediated, Open, Unable to Retest. Never close a gap because code changed.
- `delta`: apply the four-factor test in `references/substantial-modification.md` with `python scripts/screen_substantial_modification.py`; list provisions requiring re-assessment; flag that a substantial modification is a new placing on the market with a new declared support period.
- `regression`: run `python scripts/compare_assessments.py`; a regression PASS means only that no configured regression was detected.

## 18. Phase 13: tickets

Generate `22-finding-ticket-queue.json` and `.md` with `python scripts/export_ticket_queue.py` unless `ticket_mode=off`. Create external tickets only when the manifest or the user explicitly authorises it; search for duplicates by gap ID and regression key first.

## 19. Phase 14: formal report

Follow `references/reporting-standard.md`, `references/report-design.md`, `references/report-artifact-generation.md`, `templates/cra-readiness-report.md` and `templates/report-disclaimer.md`. Freeze the canonical Markdown, hash it, render DOCX and PDF from the same content, and record everything in `21-report-rendering-manifest.json`. If rendering is impossible, record `BLOCKED_RENDERING`; never fabricate a binary.

## 20. Readiness conclusion

Use exactly one:

- **Ready for conformity assessment** (state the route: module A self-assessment; module B+C or H with a notified body; or a European cybersecurity certification scheme). Only when every applicable provision is CONFORMANT or justified NOT_APPLICABLE, no provision is BLOCKED or NOT_ASSESSED, the technical documentation draft is complete, the reporting process is in place and tested, and the pinned legal baseline is current.
- **Not ready**: one or more GAP.
- **Assessment incomplete**: BLOCKED or NOT_ASSESSED provisions, unresolved scope or classification, or stale legal baseline.
- **Outside CRA scope as assessed**: with the reasoning and any residual obligations.
- **Reporting obligations only**: product placed on the market before 11 December 2027 and not substantially modified; Article 14 applies.

Never substitute a percentage for the conclusion.

## 21. Mandatory disclaimers

Every rendered report carries the wording in `templates/report-disclaimer.md` on the cover, in the executive summary, in the conclusion and in the footer. At minimum it states that the review is an independent readiness assessment, not a conformity assessment, notified-body evaluation, certification or legal advice; that the manufacturer alone is responsible for conformity, the EU declaration of conformity and CE marking; that market surveillance authorities, notified bodies and the Court of Justice determine outcomes; that conclusions are limited to the stated product version, scope, evidence and date; and that no review can guarantee the absence of vulnerabilities.

## 22. Confidentiality

Never place live credentials, tokens, keys, personal data or unpatched exploit details in the report. Redact and record the redaction.

## 23. Completion quality gate

Before delivery verify: product version and commit recorded; legal baseline hashes and status checks recorded; scope and classification decisions documented with confidence; every catalogue provision appears exactly once in the matrix; every CONFORMANT has evidence; every NOT_APPLICABLE has an Article 13(4) justification; every GAP maps to a gap with a regression key; every BLOCKED or NOT_ASSESSED is disclosed; the risk assessment covers every Annex I Part I point (2) requirement; the SBOM check ran; the Article 14 process was tested; drafts are marked as drafts; disclaimers are present; Markdown, DOCX and PDF are synchronised or `BLOCKED_RENDERING` is recorded; no secrets in outputs.
