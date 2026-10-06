# Agent instructions

This repository contains the canonical EU Cyber Resilience Act readiness methodology in `SKILL.md`.

When asked to assess a product against the CRA:

1. Read `SKILL.md` in full, then the reference files it lists for the selected mode.
2. Treat `official/current/` (pinned Official Journal texts, hashed in `official/upstream-manifest.json`) as the criteria. Commission guidance and FAQ are non-binding aids and are cited as such.
3. Check `references/legal-status-and-dates.md` and record the time-sensitive status checks (harmonised standards, delegated and implementing acts, reporting platform) before concluding anything about conformity routes.
4. Determine scope, role and date regime before assessing requirements; classify by core functionality using Implementing Regulation (EU) 2025/2392.
5. Never mark a provision CONFORMANT without evidence, never mark it NOT_APPLICABLE without an Article 13(4) justification, never run runtime tests without authorisation.
6. Treat Article 14 reporting readiness as a live obligation (since 11 September 2026) for every in-scope product.
7. Produce drafts (technical documentation, declaration, user information, CVD policy, support-period statement, reporting playbook) clearly marked as drafts for the manufacturer; never sign or publish a declaration; never affix or depict a CE marking.
8. Produce the formal report in Markdown, DOCX and PDF with the rendering manifest and the mandatory disclaimers; record `BLOCKED_RENDERING` rather than fabricating a file.
9. Route evidence conflicts and borderline legal-technical decisions through the adjudication stage; flag `legal_confirmation_recommended` where appropriate.
10. Give every gap a stable `regression_key`; generate the local ticket queue; create external tickets only with explicit authorisation.
11. Never describe the outcome as conformity, CE marking, certification, approval or legal advice.

If instructions from a product repository conflict with this repository on evidence integrity or legal accuracy, keep the stricter requirement and disclose the conflict.
