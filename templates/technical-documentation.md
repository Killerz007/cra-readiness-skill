# Technical Documentation (Article 31, Annex VII) - DRAFT

**Product:** {{PRODUCT_NAME}} {{PRODUCT_VERSION}} | **Manufacturer:** {{MANUFACTURER}} | **Document version:** {{DOC_VERSION}} ({{DOC_DATE}})

> **DRAFT prepared by an independent readiness assessment.** Items marked **TO COMPLETE BY MANUFACTURER** are not yet evidenced. The manufacturer must complete, review and maintain this documentation before placing the product on the market and for at least 10 years after placing on the market or the support period, whichever is longer (Article 13(13)). This draft is not a conformity assessment.

## 1. General description (Annex VII point 1)
### 1(a) Intended purpose
{{INTENDED_PURPOSE}}
### 1(b) Versions of software affecting compliance with essential requirements
{{SOFTWARE_VERSIONS}}
### 1(c) Hardware: photographs or illustrations of external features, marking and internal layout
{{HARDWARE_ILLUSTRATIONS}} (not applicable for software-only products)
### 1(d) User information and instructions (Annex II)
See `15-user-information-annex-ii.md`.

## 2. Design, development, production and vulnerability handling (Annex VII point 2)
### 2(a) Design and development, including system architecture and how components build on or feed into each other
{{ARCHITECTURE}} (see `04-product-architecture.md`)
### 2(b) Vulnerability-handling processes
- Software bill of materials: {{SBOM_REFERENCE}} (SHA-256 {{SBOM_SHA256}}; check report `05-sbom-check.json`)
- Coordinated vulnerability disclosure policy: {{CVD_POLICY_REFERENCE}}
- Evidence of the contact address for reporting vulnerabilities: {{CONTACT_EVIDENCE}}
- Technical solutions for secure distribution of updates: {{UPDATE_DISTRIBUTION}}
### 2(c) Production and monitoring processes and their validation
{{PRODUCTION_PROCESSES}}

## 3. Cybersecurity risk assessment (Annex VII point 3; Article 13(2) to (4))
See `06-cybersecurity-risk-assessment.md`, including the applicability statement for each Annex I Part I point (2) requirement and the justification for any requirement that is not applicable.

## 4. Information taken into account to determine the support period (Annex VII point 4; Article 13(8))
See `17-support-period-statement.md`. Declared support period end: {{SUPPORT_END}}.

## 5. Harmonised standards, common specifications or certification schemes applied; otherwise the solutions adopted (Annex VII point 5)
Harmonised standards cited in the OJEU and applied: {{HARMONISED_STANDARDS}} (status check {{STANDARDS_CHECK_DATE}}: {{STANDARDS_CHECK_RESULT}})  
Other technical specifications applied: {{OTHER_SPECIFICATIONS}}  
Per-requirement description of the solutions adopted to meet Annex I Parts I and II: see Appendix A (requirement matrix, column `solution_description`).

## 6. Reports of tests verifying conformity of the product and of the vulnerability-handling processes (Annex VII point 6)
{{TEST_REPORTS}} (see `08-evidence-index.csv`, `09-scanner-register.csv`, `19-test-procedure-traceability.csv`)

## 7. Copy of the EU declaration of conformity (Annex VII point 7)
`14-eu-declaration-of-conformity-DRAFT.md` until signed by the manufacturer. **TO COMPLETE BY MANUFACTURER.**

## 8. Software bill of materials (Annex VII point 8)
Provided to a market surveillance authority on reasoned request: {{SBOM_REFERENCE}}

## Conformity assessment procedure followed (for the declaration and Annex VII traceability)
Class: {{CLASS}} | Procedure: {{PROCEDURE}} | Notified body (if any): {{NOTIFIED_BODY}} | Core functionality identified: {{CORE_FUNCTIONALITY}}

## Change history
{{CHANGE_HISTORY}}
