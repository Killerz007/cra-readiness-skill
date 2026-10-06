# Conformity assessment routes (Article 32, Annex VIII)

The manufacturer must assess both the product against Annex I Part I and its own processes against Annex I Part II (Article 32(1)). The available procedures depend on classification (see `references/product-classification.md`) and on whether harmonised standards, common specifications or European certification schemes exist and are applied.

## Procedures (Annex VIII)

**Module A, internal control (Part I).** The manufacturer draws up the technical documentation, takes all measures necessary so that design, development, production and vulnerability handling ensure compliance, affixes the CE marking and draws up the EU declaration of conformity on its sole responsibility. No notified body. Expected activities (FAQ): implement mitigations from the risk assessment, verify compliance by testing or other means, draw up technical documentation, affix CE marking, sign the declaration, keep production in conformity.

**Module B, EU-type examination (Part II), followed by Module C, conformity to type based on internal production control (Part III).** A single notified body examines the technical documentation, supporting evidence and specimens of critical parts, carries out examinations and tests, issues an EU-type examination certificate, and performs periodic audits of the vulnerability-handling processes. The manufacturer must inform the notified body of modifications affecting conformity, which require an addition to the certificate. Under module C the manufacturer ensures production conformity with the approved type, affixes the CE marking and draws up the declaration.

**Module H, full quality assurance (Part IV).** The manufacturer operates a notified-body-approved quality system covering design, development, final inspection and testing, and vulnerability handling, maintained for the support period and subject to surveillance audits. The CE marking is followed by the notified body's identification number (Article 30(4)).

**European cybersecurity certification scheme** under Regulation (EU) 2019/881 at assurance level at least "substantial", where available and applicable (Article 32(1)(d), (3)(c), (4)(a)).

## Route by class

| Class | Routes | Notes |
|---|---|---|
| Default | A, B+C, H, or certification scheme | Manufacturer's choice. |
| Important class I | B+C or H, unless harmonised standards, common specifications or a certification scheme at least "substantial" are applied in full, in which case module A is also available | Article 32(2). As of the pinned status no harmonised standard is cited and no common specification or applicable scheme exists, so module A is **not** available for class I. Re-verify each run. |
| Important class II | B+C, H, or certification scheme at least "substantial" | Article 32(3). Always third-party or certification. |
| Critical | Certification scheme where an Article 8(1) delegated act requires it; otherwise the class II routes | Article 32(4). No delegated act as of the pinned status. |
| FOSS products in Annex III categories | Any Article 32(1) route including module A, if technical documentation is public at placing on the market | Article 32(5). |

Manufacturers may always choose a stricter procedure. Fees for SMEs must be reduced proportionately (Article 32(6)).

## Presumption of conformity (Article 27)

Products and processes conforming to harmonised standards whose references are published in the OJEU are presumed to conform with the essential requirements those standards cover. The same applies to common specifications adopted by implementing act and to European certification schemes designated under Article 27(8) and (9). Presumption covers only the requirements and the product scope the standard addresses; anything outside must be demonstrated otherwise (guidance section 6.3). Where no harmonised standard exists, the manufacturer describes in the technical documentation the solutions adopted to meet each requirement, including other technical specifications applied (Annex VII point 5); using draft standards, international standards or industry frameworks as evidence is permissible but gives no presumption.

## What the assessment records

1. The class and the routes legally available today, with the status checks in `references/harmonised-standards-status.md` performed and dated.
2. The route the manufacturer intends to use and whether the assessment supports it.
3. For module A: whether the manufacturer's own conformity assessment activities are in place.
4. For B+C or H: whether the technical documentation and supporting evidence are at the level a notified body will examine, and that the notified body must be one notified for the CRA (Chapter IV applies from 11 June 2026; lists are published in NANDO).
5. For certification schemes: whether a scheme applicable to the product exists at assurance level at least "substantial".

## Related obligations

- EU declaration of conformity (Article 28, Annex V): content, updated as appropriate, in the languages required by the Member State of making available; single declaration where several Union acts apply; drawing it up means assuming responsibility.
- Simplified declaration (Article 13(20), Annex VI): allowed with the product if it gives the exact internet address of the full declaration.
- CE marking (Articles 29 and 30): affixed visibly, legibly and indelibly to the product, or to the packaging and the declaration; for software, to the declaration or on the website accompanying the product in an easily and directly accessible section; before placing on the market; followed by the notified body number for module H.
- Type, batch or serial number and manufacturer identification and contact details on the product, packaging or accompanying document (Article 13(15) and (16)).
