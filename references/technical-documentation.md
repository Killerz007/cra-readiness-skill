# Technical documentation (Article 31, Annex VII)

The technical documentation is what the manufacturer shows a market surveillance authority or notified body. It must be drawn up before placing on the market, kept continuously updated at least during the support period, and retained for 10 years after placing on the market or the support period, whichever is longer (Articles 13(12), 13(13), 31(2)). It must contain at least the Annex VII elements, as applicable to the product.

## Annex VII content and how this skill fills it

| Annex VII | Content | Source in the assessment package |
|---|---|---|
| 1(a) | Intended purpose | scope decision, risk assessment |
| 1(b) | Versions of software affecting compliance with essential requirements | assessment manifest, architecture |
| 1(c) | For hardware: photographs or illustrations of external features, marking and internal layout | manufacturer supplies; marked TO COMPLETE if absent |
| 1(d) | User information and instructions as set out in Annex II | `15-user-information-annex-ii.md` |
| 2(a) | Design and development information, including system architecture and how software components build on or feed into each other | `04-product-architecture.md` |
| 2(b) | Vulnerability-handling processes: SBOM, CVD policy, evidence of a contact address for reporting, secure update distribution design | `05-sbom`, `16-cvd-policy-draft.md`, `security.txt`, architecture |
| 2(c) | Production and monitoring processes and their validation | manufacturer process documents; build pipeline evidence |
| 3 | Cybersecurity risk assessment including how Annex I Part I requirements apply | `06-cybersecurity-risk-assessment.md` |
| 4 | Information taken into account to determine the support period | `17-support-period-statement.md` |
| 5 | Harmonised standards, common specifications or certification schemes applied, and where not applied, descriptions of the solutions adopted to meet Annex I Parts I and II, including other technical specifications; for partial application, which parts | requirement matrix and the standards status record |
| 6 | Reports of tests verifying conformity of the product and of the vulnerability-handling processes with Annex I Parts I and II | evidence index, scanner register, test records |
| 7 | A copy of the EU declaration of conformity | `14-eu-declaration-of-conformity-DRAFT.md` until the manufacturer signs |
| 8 | Where applicable, the SBOM, on reasoned request from a market surveillance authority | `05-sbom` |

## Rules

- One set of technical documentation per product (or product family under guidance section 7.4); where other Union acts also require technical documentation, a single set contains everything (Article 31(3)).
- Any language; a notified body may require its own language; an authority may require a language it understands (Article 31(4); FAQ).
- The Commission may add elements by delegated act (Article 31(5)); none adopted as of the pinned status.
- For products designed before the CRA applies, the documentation need not recreate historical design or test records where the current risk assessment shows existing measures are adequate; it must show how the vulnerability-handling processes are met (guidance points 37 to 39).
- Pre-market: module A requires the manufacturer to draw up this documentation and keep it (Annex VIII Part I); modules B and H submit it to the notified body.

## Assessment approach

Score each Annex VII item: present and adequate (CONFORMANT), present but incomplete (GAP with the missing elements listed), absent (GAP), not applicable with justification (for example item 1(c) for software-only products). Produce `13-technical-documentation-draft.md` from `templates/technical-documentation.md` with every item either filled from the assessment outputs or marked **TO COMPLETE BY MANUFACTURER** with what is needed.
