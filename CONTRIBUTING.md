# Contributing

Changes to assessment logic must be traceable to the Official Journal text, a published Commission act or guidance, or a cited harmonised standard.

For legal changes:

1. Link the EUR-Lex ELI or the Commission page; never a secondary summary alone.
2. If a pinned text changed, run `python scripts/sync_official_text.py --sync` and review `official/UPSTREAM_CHANGE_REVIEW.md`.
3. Update `references/legal-status-and-dates.md` with the date and effect.
4. Update `references/requirement-assessment-guide.json` for any provision whose wording or interpretation changed.
5. Add or update tests; run `make validate`.
6. Do not weaken evidence requirements to reduce gaps.

Keep `SKILL.md` under about 500 lines; put detail in `references/`. EU documents keep their EU reuse terms; original content is Apache-2.0.
