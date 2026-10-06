# Scope determination

Work through the questions in order. Record each answer, the evidence, the article relied on, a confidence level (High, Medium, Low) and whether legal confirmation is recommended. The output schema is `schemas/scope-decision.schema.json`; `scripts/classify_product.py --stage scope` turns the answers into the decision record.

## Q1. Is it a product with digital elements?

Article 3(1): "a software or hardware product and its remote data processing solutions, including software or hardware components being placed on the market separately".

Article 2(1): the CRA applies to products with digital elements made available on the market "the intended purpose or reasonably foreseeable use of which includes a direct or indirect logical or physical data connection to a device or network".

Covered (guidance point 18): standalone software such as apps and programs, whether distributed digitally or physically; hardware with embedded software; standalone hardware such as integrated circuits or motherboards; and combinations of hardware and software supplied separately but intended to operate together.

**Software test (guidance points 20 to 21).** Software is a product with digital elements when it is provided to a user, obtained by that user and operated on, or as part of, an electronic information system on the user's side. Downloaded or installed software qualifies, including browser extensions and web-technology applications supplied for local execution. Software that executes remotely and is merely accessed by the user (a web application in a browser, a SaaS service) is not on that basis a product with digital elements. Such remote processing is covered only where it is a remote data processing solution of a product (Q4).

**Data connection.** "Direct or indirect logical or physical data connection" is broad: any network interface, Bluetooth, USB, serial, or indirect connection through another device counts. Only a product that cannot be connected to anything, directly or indirectly, falls outside Article 2(1).

Evidence: product description, distribution channel, installation model, interface inventory.

## Q2. Is it made available on the EU market in the course of a commercial activity?

Article 3(22): making available means "the supply of a product with digital elements for distribution or use on the Union market in the course of a commercial activity, whether in return for payment or free of charge". Article 3(21): placing on the market is the first making available.

- Internal tools built for one's own use are not placed on the market (FAQ; Blue Guide section 2.3).
- Unfinished software released for testing is permitted for a limited period with a visible non-compliance sign (Article 4(3)); it must still follow a risk assessment and comply "to the extent possible" (Recital 37).
- Free of charge does not mean non-commercial. Monetisation through other services, advertising, or mandatory personal-data processing can make it commercial (guidance section 3.2.2).
- For free and open-source software apply `references/open-source.md` before concluding.

**Standalone software: when is it placed on the market?** When its manufacturing phase is complete and it is first supplied for distribution or use in the EU (guidance points 13 to 14). All copies of the same version are treated as placed on the market at that moment. Variants with different components, configurations or enabled functionalities are distinct products (guidance point 14). A later version is newly placed on the market only when it is a substantial modification (guidance point 15; `references/substantial-modification.md`).

## Q3. Does an exclusion apply?

| Article | Excluded | Note |
|---|---|---|
| 2(2)(a) | Medical devices, Regulation (EU) 2017/745 | |
| 2(2)(b) | In vitro diagnostic medical devices, Regulation (EU) 2017/746 | |
| 2(2)(c) | Vehicle type-approval, Regulation (EU) 2019/2144 | motor vehicles of categories M, N, O and their systems, components and separate technical units |
| 2(3) | Products certified under Regulation (EU) 2018/1139 (civil aviation) | only products actually certified |
| 2(4) | Marine equipment, Directive 2014/90/EU | |
| 2(5) | Sectoral rules may limit or exclude application by delegated act | none adopted as of the pinned status |
| 2(6) | Spare parts replacing identical components, same specifications | identical means same specifications; a newer chip with different security mechanisms is not identical (guidance section 4.2) |
| 2(7) | Products developed or modified exclusively for national security or defence, or designed to process classified information | |

Products also covered by the Machinery Regulation, the Radio Equipment Directive delegated act, the General Product Safety Regulation, the AI Act or the European Health Data Space Regulation remain in scope; the FAQ "Interplay with other legislation" section explains the overlaps. High-risk AI systems that conform to the CRA are deemed to meet the AI Act cybersecurity requirement (Article 12).

## Q4. Which remote data processing solutions are part of the product?

Apply the three cumulative tests in `references/remote-data-processing.md`: processing at a distance; its absence would prevent the product from performing one of its functions; and the software was designed and developed by the manufacturer or under its responsibility. Each qualifying solution is part of the product for the risk assessment, the essential requirements and the reporting obligations. Non-qualifying remote services that affect security are treated as third-party components subject to Article 13(5) due diligence.

## Q5. Which date regime applies?

| Situation | Obligations |
|---|---|
| Unit placed on the market on or after 11 December 2027 | All obligations. |
| Unit placed on the market before 11 December 2027, not substantially modified | Article 14 reporting only (Article 69(3)). Vulnerability handling under Annex I Part II is not legally required for that unit, but the manufacturer must still inform users under Article 14(8). |
| Unit placed on the market before 11 December 2027 and substantially modified from that date | Full obligations for the modified product (Article 69(2)); the modified product is a new placing on the market. |
| Product type designed before 11 December 2027, new units placed from that date | Full obligations; no redesign is required where the risk assessment shows existing measures are adequate (guidance points 33 to 39). |
| Assessment performed before 11 December 2027 | Report states which obligations already apply (Article 14 since 11 September 2026) and which will apply. |

## Q6. Are components placed on the market separately?

A component supplied separately is a product in its own right and gets its own assessment (Article 3(1)). A component supplied only inside the product is assessed as part of the product and through Article 13(5) due diligence. Software modules sold or licensed separately are separate products for classification (guidance point 145).

## Decision record

The scope decision must state:

- the conclusion (in scope; out of scope with reason; in scope for Article 14 only);
- the economic-operator role (see `references/economic-operator-roles.md`);
- the product boundary, including remote data processing solutions and separately supplied components;
- the date regime;
- confidence and whether legal confirmation is recommended;
- the evidence relied on.

Borderline cases that always get `legal_confirmation_recommended = true`: open-source monetisation models, products near an exclusion boundary, remote-processing-heavy products, products whose intended purpose is unclear from the documentation, and any case where the user disagrees with the assessed outcome.
