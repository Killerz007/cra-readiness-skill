# Product classification

Classification determines the conformity assessment procedure (Article 32) and therefore whether a notified body or a European certification scheme is required. Get it wrong in either direction and the manufacturer is exposed: understating the class breaches Article 32 (fines under Article 64(3)); overstating it wastes money and time.

## The test: core functionality

Article 7(1): products "which have the core functionality of a product category set out in Annex III" are important products. Article 8 and Annex IV do the same for critical products. The technical descriptions of every category are in Implementing Regulation (EU) 2025/2392 (`references/cra-product-categories.generated.json`).

Core functionality is "that product's main features and technical capabilities, without which it would not be able to meet its intended purpose", assessed objectively from the instructions for use, promotional and sales material and the technical documentation (guidance point 139).

Rules from the guidance and the implementing regulation:

1. **Additional functions do not disqualify.** An operating system with a calculator is still an operating system (recital 4 of the implementing regulation; guidance point 140).
2. **Integration does not qualify.** A smartphone integrating an OS and a password manager is neither (Article 7(1); recital 5 of the implementing regulation; guidance point 141). A news app with an embedded browser is not a browser (recital 3).
3. **Substantially exceeding or falling short.** SOAR software exceeds SIEM; a log viewer without correlation falls short of SIEM (guidance points 142, examples 59 and 60).
4. **Marketing cannot be used to escape.** Inconsistencies between promotional material, instructions and technical documentation are a red flag (guidance point 143).
5. **One core functionality per product.** Identify it explicitly in the technical documentation (guidance point 144).
6. **Separately sold modules are separate products.** A suite sold as a whole is classified as a whole; modules offered separately are classified individually (guidance point 145, example 61).
7. **Hardware security tiers** use Common Criteria AVA_VAN levels: tamper-resistant microprocessors and microcontrollers are designed for AVA_VAN 2 or 3 (class II); secure elements for at least AVA_VAN.4 (critical).

## Categories (Annex III and IV, with implementing-regulation technical descriptions)

**Important, class I (19):** identity and privileged access management; standalone and embedded browsers; password managers; anti-malware; VPN products; network management systems; SIEM; boot managers; PKI and certificate issuance; physical and virtual network interfaces; operating systems; routers, internet modems and switches; microprocessors with security functionality; microcontrollers with security functionality; ASIC and FPGA with security functionality; smart home general purpose virtual assistants; smart home security products (locks, cameras, baby monitors, alarms); internet-connected toys with social interactive or location features; health-monitoring wearables not covered by medical-device law, and wearables for children.

**Important, class II (4):** hypervisors and container runtimes; firewalls, intrusion detection and prevention systems (including web application firewalls and anti-spam gateways); tamper-resistant microprocessors; tamper-resistant microcontrollers.

**Critical (3):** hardware devices with security boxes (payment terminals, HSMs, tachographs); smart meter gateways and other devices for advanced security purposes including secure cryptoprocessing; smartcards and similar devices including secure elements (TPMs, embedded UICCs, payment and identity cards).

Always read the full technical description before concluding. Several descriptions carry explicit inclusions ("includes but is not limited to") and limits (for example, a toy that merely senses proximity has no location-tracking feature).

## Classification procedure

1. State the intended purpose from the user information, marketing and technical documentation. Note contradictions.
2. List the main features without which the product would not meet that purpose.
3. For each Annex III or IV category whose description overlaps, decide: matches the core functionality; is merely an integrated or ancillary function; substantially exceeds; or substantially falls short. Cite the description text.
4. Where the product is sold as modules, repeat per module.
5. Conclude: default, important class I, important class II, or critical. Record confidence and the strongest counter-argument.
6. Hand the result to `references/conformity-assessment-routes.md`.

Use `python scripts/classify_product.py --answers <json> --stage classify` to produce the decision record (`schemas/classification-decision.schema.json`).

## Consequences by class (summary; details in `references/conformity-assessment-routes.md`)

| Class | Article 32 routes |
|---|---|
| Default | Module A (internal control), or B+C, or H, or an applicable European certification scheme. |
| Important class I | B+C or H, unless harmonised standards, common specifications or a European certification scheme at assurance level at least "substantial" are applied in full, in which case module A is available (Article 32(2)). As of the pinned status none exist, so module A is not available. |
| Important class II | B+C, H, or a European certification scheme at assurance level at least "substantial" (Article 32(3)). |
| Critical | A European certification scheme where a delegated act under Article 8(1) requires it; otherwise the class II routes (Article 32(4)). No such delegated act exists as of the pinned status. |
| Free and open-source products in Annex III categories | Any Article 32(1) route, including module A, provided the technical documentation is made public at placing on the market (Article 32(5)). |

Presumption of conformity under harmonised standards covers only the requirements the standard addresses; additional functions do not trigger a stricter route by themselves (guidance section 6.3).
