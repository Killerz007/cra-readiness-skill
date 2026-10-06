# Cybersecurity risk assessment (Article 13(2) to (4))

The risk assessment is the hinge of CRA conformity: it decides which Annex I Part I point (2) requirements apply and how every requirement is implemented, it must be included in the technical documentation, and it must be kept current during the support period. The CRA does not mandate a method (FAQ); this skill uses the structure below and accepts any equivalent documented method (ISO/IEC 27005, IEC 62443-3-2, NIST SP 800-30, threat modelling frameworks) as long as the required content is present.

## Required content (Article 13(3) and Annex VII point 3)

1. **Product identification**: name, version, variants covered, components, remote data processing solutions, intended operating environment.
2. **Intended purpose** (Article 3(23)): as stated in instructions, marketing and technical documentation, including the specific context and conditions of use.
3. **Reasonably foreseeable use** (Article 3(24)) and **reasonably foreseeable misuse** (Article 3(25)).
4. **Conditions of use**: operational environment, assets to be protected (data categories, functions, connected systems, safety), user types.
5. **Expected time in use** and the resulting support period input.
6. **Threat and risk analysis**: threat scenarios per interface and asset, likelihood, impact including health and safety where relevant, risk level.
7. **Applicability and implementation statement for each Annex I Part I point (2) requirement (a) to (m)**: applicable or not, the justification, and how it is implemented. Non-applicability needs a clear justification that goes into the technical documentation (Article 13(4)).
8. **How Annex I Part I point (1) is applied**: any identified risk not covered by (2)(a) to (m) and its treatment (guidance points 164 to 166).
9. **How Annex I Part II vulnerability handling is applied** to this product.
10. **Due diligence on third-party and open-source components** (Article 13(5)): what the product requires from each component, how that was verified (CE marking or conformity evidence, update history, vulnerability databases, tests), and residual concerns (guidance section 7.3).
11. **External dependencies outside the product boundary** and the product-level mitigations (guidance points 168 to 169).
12. **Residual risk statement**: residual risks after treatment, and why they are sufficiently addressed in light of intended purpose and foreseeable use. Internal risk appetite, commercial strategy and cost are not acceptable grounds for leaving a risk untreated (guidance points 157 to 163). Risk cannot be transferred to users to compensate for design shortcomings (point 161), although user information may address residual risks and restrict the intended purpose to trusted environments (point 162, example 66).
13. **Maintenance**: trigger events and review cadence for updating the assessment (Article 13(3) and (7)).

## Applicability patterns that the guidance accepts

- Automatic security updates (2)(c): not for products primarily intended for integration as components, nor for products where users would not reasonably expect automatic updates, such as professional ICT, critical and industrial environments (Recital 56). Notification of updates and the option to postpone still apply where the product does receive updates.
- Secure by default (2)(b): a component is responsible for the configuration it is delivered with, not for how an integrator changes it (FAQ on secure by default). Tailor-made products for a particular business user under explicit contractual terms may deviate from (2)(b) and from free security updates in Part II (8) (Recital 64; FAQ on tailor-made products). Minor customisation of a mass-market product is not tailor-made.
- Known exploitable vulnerabilities (2)(a): applies at placing on the market; a vulnerability is "known" when listed in the EU vulnerability database or other prominent databases, disclosed to the manufacturer, found by its own testing, or prominently reported in reliable media; exploitability is judged under practical operational conditions (guidance points 230 to 237; FAQ examples of the laser-glitch smartphone, unused library and sealed debug interface).
- Pre-CRA designs: existing measures may be relied on where the risk assessment shows they address the risks; no obligation to add features for their own sake (guidance points 33 to 39).
- Product families: one assessment may cover variants that share architecture, security-relevant design and intended purpose (guidance section 7.4).

## Evidence expectations

- The assessment document itself, versioned and dated, with authorship and approval.
- Traceability from each threat scenario to the measures and to the requirement implementation statements.
- Evidence that the assessment informed design (design decisions, backlog items, test cases) or, for pre-CRA designs, a current assessment that explains how the existing design mitigates the risks.
- Update history showing reviews after vulnerabilities, incidents, substantial changes or environment changes.

## Common gaps

- A generic corporate risk register instead of a product-level assessment.
- No per-requirement applicability statement, or "not applicable" without justification.
- Remote data processing solutions omitted.
- Third-party components assessed only by licence, not by security properties.
- Residual risk accepted by reference to cost or risk appetite.
- Assessment never updated after release.

## Output

`06-cybersecurity-risk-assessment.md`, following `templates/risk-assessment.md`, with each Annex I Part I point (2) requirement decision mirrored in `07-requirement-matrix.csv`.
