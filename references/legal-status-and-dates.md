# Legal status, sources and dates

This file is the single place where the skill states *what law applies, from when, and what is still pending*. Every statement here is dated. Re-verify anything marked **time-sensitive** at the start of each assessment, and record the verification in the assessment manifest.

## Binding instruments (pinned in `official/current/`)

| Instrument | Short name | Status | Pinned file |
|---|---|---|---|
| Regulation (EU) 2024/2847 of 23 October 2024 (OJ L, 2024/2847, 20.11.2024) | the CRA | In force since 10 December 2024 | `CRA-2024-2847.xhtml` |
| Corrigendum of 5 December 2024 | — | Corrects Article 64(10): "paragraphs 2 to 9", not "3 to 9" | noted in manifest |
| Commission Implementing Regulation (EU) 2025/2392 of 28 November 2025 | technical descriptions | In force since 21 December 2025 | `IR-2025-2392.xhtml` |
| Commission Delegated Regulation (EU) 2026/881 of 11 December 2025 (OJ L, 2026/881, 20.4.2026) | delayed dissemination | In force (20 days after publication) | `CDR-2026-0881.txt` |

Only the Official Journal text is authentic. The pinned copies are the Publications Office XHTML manifestations, hashed in `official/upstream-manifest.json`.

## Non-binding guidance (pinned)

| Document | Date | Use in this skill |
|---|---|---|
| Commission guidance on the application of the CRA, C(2026) 5252 final (Annex) | 27 July 2026 | Primary interpretive aid for scope, open source, substantial modification, support period, classification, risk assessment, remote data processing, reporting "awareness". Cite by point number. |
| Commission CRA implementation FAQ | first published 3 December 2025, updated | Secondary interpretive aid. Cite by question heading. |

Both are explicitly non-binding. Only the Court of Justice of the European Union can give an authoritative interpretation. Market surveillance authorities are nevertheless expected to use the guidance as their reference.

## Application timeline (Article 71 and Article 69)

| Date | What applies |
|---|---|
| 10 December 2024 | Entry into force. |
| 11 June 2026 | Chapter IV (Articles 35 to 51): notifying authorities and notified bodies. |
| 11 September 2026 | **Article 14 reporting obligations** for manufacturers: actively exploited vulnerabilities and severe incidents, via the ENISA single reporting platform. Applies to all in-scope products, including those placed on the market before 11 December 2027 (Article 69(3)), and continues after the support period ends (guidance point 210). No retroactive reporting of exploitation the manufacturer already knew of before 11 September 2026 (guidance point 217). |
| 11 December 2027 | General application: essential requirements, conformity assessment, CE marking, technical documentation, user information, market surveillance, penalties. Open-source software steward obligations (Article 24, including Article 24(3) reporting) apply from this date. |
| 11 June 2028 | Article 69(1): EU type-examination certificates and approval decisions issued under other Union harmonisation legislation for cybersecurity requirements remain valid until this date unless they expire earlier. |

**Products placed on the market before 11 December 2027** are subject to the CRA only if they are substantially modified from that date (Article 69(2)), except that Article 14 applies to them regardless (Article 69(3)). "Placed on the market" refers to each individual unit, not the product type; new units of an old design placed on or after 11 December 2027 must conform (FAQ, "Transition period"; guidance points 33 to 39 on products designed before application).

## Penalties (Article 64, as corrected)

| Infringement | Maximum administrative fine |
|---|---|
| Annex I essential requirements, Article 13, Article 14 | EUR 15 000 000 or 2.5 % of total worldwide annual turnover, whichever is higher |
| Articles 18 to 23, 28, 30(1) to (4), 31(1) to (4), 32(1) to (3), 33(5), 39, 41, 47, 49, 53 | EUR 10 000 000 or 2 % |
| Incorrect, incomplete or misleading information to notified bodies or market surveillance authorities | EUR 5 000 000 or 1 % |

Microenterprises and small enterprises are not fined for missing the 24-hour early-warning deadline; open-source software stewards are not subject to administrative fines (Article 64(10)).

## Pending or time-sensitive items (verify every run)

| Item | Status as of 2026-10-06 | How to verify |
|---|---|---|
| Harmonised standards cited in the OJEU (Article 27) | None cited. Presumption of conformity is unavailable. Standardisation request M/606 accepted by CEN, CENELEC and ETSI in 2025; EN 40000 series (horizontal) and product-specific drafts in progress; a draft amendment to M/606 would move delivery dates to 31 October 2026 (horizontal and vulnerability handling) and 31 December 2026 (product-specific). | Search the OJEU C series for "2024/2847" harmonised standard citations; check the Commission's harmonised standards page. Record the result in the manifest. |
| Common specifications (Article 27(2)) | None adopted. | EUR-Lex search for implementing acts citing Article 27(2). |
| European cybersecurity certification schemes designated for critical products (Article 8(1) delegated act) | None adopted. Critical products therefore follow Article 32(4)(b), i.e. the class II procedures. | EUR-Lex search for delegated acts under Article 8(1). |
| SBOM format implementing act (Article 13(24)) | None adopted. The legal minimum stays "commonly used and machine-readable format covering at least top-level dependencies". | EUR-Lex search for implementing acts under Article 13(24). |
| Notification format implementing act (Article 14(10)) | None adopted; the ENISA platform defines the fields in practice. | EUR-Lex search; ENISA SRP page. |
| Delegated acts amending Annex III or IV, or setting minimum support periods (Articles 7(3), 8(2), 13(8)) | None adopted. | EUR-Lex search. |
| ENISA single reporting platform | Live since 11 September 2026 at `https://portal.cra-srp.enisa.europa.eu`; EU Login with multi-factor authentication; roles Primary and Secondary Assigned Representative. | ENISA SRP page and FAQ. |
| Digital Omnibus proposals (19 November 2025) | Legislative proposals that may touch incident reporting across EU acts; not adopted. Do not assume any change to CRA deadlines. | Commission "digital rulebook" page. |

## How this skill treats the dates

- An assessment run on or after 11 September 2026 must treat Article 14 readiness as **live**, not preparatory.
- An assessment run before 11 December 2027 reports conformance against requirements that will become binding on that date and says so.
- A product first placed on the market before 11 December 2027 is assessed for (a) Article 14 readiness and (b) substantial-modification exposure, and the report says which obligations currently apply.
