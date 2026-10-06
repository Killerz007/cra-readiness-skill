# Harmonised standards status

**Snapshot date: 2026-10-06. This file is time-sensitive. Verify before relying on it and record the verification in the assessment manifest.**

## Legal effect

Only harmonised standards whose references are published in the Official Journal of the European Union give a presumption of conformity (Article 27(1)). Draft standards (prEN, FprEN), published standards not yet cited, international standards and industry frameworks give no presumption. They remain useful as "other relevant technical specifications applied" in the technical documentation (Annex VII point 5) and as the content of the manufacturer's own solutions.

## Status as of the snapshot

- **No harmonised standard supporting the CRA has been cited in the OJEU.** Consequences: no presumption of conformity for any requirement; important class I products cannot use module A (Article 32(2)).
- **Standardisation request M/606** to CEN, CENELEC and ETSI was accepted in 2025. It requests horizontal standards (a cybersecurity principles and risk-management standard; a vulnerability-handling standard; a generic security-requirements standard for Annex I Part I) and product-specific standards for the Annex III and IV categories. The FAQ gives the original delivery dates: horizontal design and vulnerability-handling standards by 30 August 2026, product-specific standards by 30 October 2026, the Annex I Part I properties standard by 30 October 2027. A Commission draft amendment published in July 2026 proposes moving the first two to 31 October 2026 and the product-specific set to 31 December 2026; as of the snapshot that amendment was reported as not yet adopted.
- **Horizontal drafts (CEN-CENELEC JTC 13):** prEN 40000-1-1 (vocabulary), prEN 40000-1-2 (cyber resilience principles and risk management), prEN 40000-1-3 (vulnerability handling), prEN 40000-1-4 (generic security requirements), plus a technical report on threats and security objectives. The vulnerability-handling part was the furthest advanced at the snapshot.
- **Product-specific drafts:** ETSI drafts for most Annex III categories (public enquiry opened August 2026); CENELEC drafts for semiconductors and smartcards; the prEN 50770 series for operational technology products.
- **Common specifications (Article 27(2)):** none.
- **European cybersecurity certification schemes:** the EUCC scheme (Implementing Regulation (EU) 2024/482) exists under the Cybersecurity Act; no Article 8(1) delegated act requires its use for critical products, and no Article 27(8) or (9) designation for CRA presumption was identified.

## How to verify

1. Search EUR-Lex for Commission implementing decisions citing Regulation (EU) 2024/2847 and Regulation (EU) No 1025/2012 (harmonised standard citations are published as implementing decisions in the OJ L series since 2023).
2. Check the Commission's harmonised standards pages and the CEN-CENELEC and ETSI work programmes for the EN 40000 and product-specific series.
3. Record the date, the search performed, and the result in `00-assessment-manifest.json` under `standards_status_check`.

## How the assessment uses standards

- Where a cited harmonised standard exists and is applied in full: record it in Annex VII point 5 and in the declaration; assess conformance with the standard and note that presumption covers only its scope.
- Where only drafts exist: the manufacturer may align with them as its documented solution; the assessment says "aligned with draft prEN 40000-1-3 (version, date)" and never "presumed conformant".
- Where the manufacturer relies on other specifications (IEC 62443-4-1 and 4-2, ETSI EN 303 645, ISO/IEC 27001, NIST SSDF, OWASP ASVS and SAMM): record them under Annex VII point 5 as other technical specifications applied, mapped to the Annex I requirements they support. Mapping documents are evidence of method, not of conformance.
