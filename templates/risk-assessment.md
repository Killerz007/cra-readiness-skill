# Cybersecurity Risk Assessment (Article 13(2) to (4), Annex VII point 3)

**Product:** {{PRODUCT_NAME}} {{PRODUCT_VERSION}} | **Variants covered:** {{VARIANTS}} | **Version of this assessment:** {{RA_VERSION}} ({{RA_DATE}})  
**Author / approver:** {{AUTHOR}} / {{APPROVER}}

> Draft prepared by an independent readiness assessment. The manufacturer owns this assessment, must review and approve it, and must keep it updated during the support period (Article 13(3)).

## 1. Product identification and boundary
- Product, components, variants, hardware and software versions affecting compliance.
- Remote data processing solutions inside the boundary (Article 3(2)): {{RDPS}}
- Separately supplied components: {{SEPARATE_COMPONENTS}}
- Third-party services outside the boundary that the product relies on: {{EXTERNAL_SERVICES}}

## 2. Intended purpose (Article 3(23))
{{INTENDED_PURPOSE}}

## 3. Reasonably foreseeable use and misuse (Article 3(24), (25))
{{FORESEEABLE_USE}}

## 4. Conditions of use, operational environment and assets to be protected
{{CONDITIONS_AND_ASSETS}}

## 5. Expected time in use
{{EXPECTED_USE_TIME}} (feeds the support-period determination, Article 13(8))

## 6. Threat and risk analysis
| ID | Interface / asset | Threat scenario | Likelihood | Impact (incl. health and safety) | Risk | Treatment | Residual |
|---|---|---|---|---|---|---|---|
{{RISK_TABLE}}

## 7. Applicability and implementation of Annex I Part I point (2) requirements
| Requirement | Applicable? | Justification (goes into technical documentation per Article 13(4)) | Implementation (how the requirement is met) | Evidence |
|---|---|---|---|---|
| (a) no known exploitable vulnerabilities | | | | |
| (b) secure by default, reset to original state | | | | |
| (c) security updates; automatic updates where applicable | | | | |
| (d) protection from unauthorised access; reporting | | | | |
| (e) confidentiality | | | | |
| (f) integrity; reporting of corruption | | | | |
| (g) data minimisation | | | | |
| (h) availability and denial-of-service resilience | | | | |
| (i) minimise impact on other devices and networks | | | | |
| (j) limit attack surfaces | | | | |
| (k) exploitation mitigation | | | | |
| (l) security logging with opt-out | | | | |
| (m) secure data removal and transfer | | | | |

## 8. Application of Annex I Part I point (1)
Risks not covered by (2)(a) to (m) and their treatment: {{POINT_1_TREATMENT}}

## 9. Application of Annex I Part II vulnerability handling to this product
{{PART_II_APPLICATION}}

## 10. Due diligence on third-party and open-source components (Article 13(5))
See `component-due-diligence-register.csv`. Summary: {{DUE_DILIGENCE_SUMMARY}}

## 11. External dependencies outside the boundary and product-level mitigations
{{EXTERNAL_MITIGATIONS}}

## 12. Residual risk statement
{{RESIDUAL_RISK}}

Residual risks are sufficiently addressed in light of the intended purpose and reasonably foreseeable use: {{YES_NO_WITH_REASONING}}. Cost, commercial feasibility and internal risk appetite were not used as grounds for leaving a risk untreated.

## 13. Maintenance
Triggers for update: new vulnerabilities or incidents, substantial modifications, environment changes, new threat intelligence, changes in cited standards. Review cadence: {{CADENCE}}. Change log: {{CHANGE_LOG}}
