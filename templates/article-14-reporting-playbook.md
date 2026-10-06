# Article 14 Reporting Playbook - DRAFT

> Draft procedure for the manufacturer's actively-exploited-vulnerability and severe-incident reporting under Article 14 of Regulation (EU) 2024/2847, applicable since 11 September 2026 to all in-scope products including those placed on the market before 11 December 2027 and those past their support period. Adapt, approve and rehearse.

## 0. Standing preparations
| Item | Value | Owner | Verified on |
|---|---|---|---|
| CSIRT designated as coordinator (Article 14(7)) | {{CSIRT}} ({{MEMBER_STATE}}) | | |
| Basis: main establishment where cybersecurity decisions are predominantly taken, or fallback order (authorised representative, importer, distributor, users) | {{BASIS}} | | |
| Single reporting platform account: Primary Assigned Representative | {{PRIMARY_AR}} (EU Login with MFA) | | |
| Secondary Assigned Representatives (up to 20) | {{SECONDARY_ARS}} | | |
| Platform URL | https://portal.cra-srp.enisa.europa.eu | | |
| 24/7 on-call rota covering the 24-hour early warning | {{ROTA}} | | |
| Product inventory with Member States where each product is made available | {{INVENTORY}} | | |
| User notification channels (customers, registered devices, public advisory, machine-readable feed) | {{CHANNELS}} | | |
| Templates: early warning, 72-hour notification, final report (see `article-14-notification-forms.md`) | | | |
| Decision authority for "awareness" and for submitting | {{DECIDER}} | | |

## 1. Detection and intake
Sources: CVD intake, customer or partner reports, threat intelligence, government or CSIRT notices, telemetry and monitoring, researcher reports, media. Log every potential event with timestamp and source.

## 2. Initial assessment (start immediately; log start time)
Determine with a reasonable degree of certainty whether:
- a vulnerability in our product is being actively exploited (reliable evidence of exploitation by a malicious actor without the system owner's permission, Article 3(42)); or
- a severe incident has occurred that compromised the product's security (Article 14(5): capable of negatively affecting availability, authenticity, integrity or confidentiality of sensitive or important data or functions; or introduction or execution of malicious code in the product or a user's systems).

Record: evidence considered; whether the vulnerable code is reachable and exploited in our product (a third-party component vulnerability not exploitable in our product is not reportable, Article 15 voluntary reporting optional); the **awareness timestamp** and who decided.

## 3. Early warning (within 24 hours of awareness)
Submit via the platform to the designated CSIRT endpoint: product, nature of the event, Member States where the product is known to be available, for incidents whether unlawful or malicious acts are suspected, sensitivity indication and any request to delay dissemination with reasons (Article 16(2); Delegated Regulation (EU) 2026/881). Compute deadlines with `scripts/reporting_deadlines.py`.

## 4. Notification (within 72 hours of awareness)
Vulnerability: general information on the product, the general nature of the exploit and vulnerability, corrective or mitigating measures taken and measures users can take, sensitivity. Incident: nature, initial assessment, measures taken and available to users, sensitivity.

## 5. Inform users (Article 14(8))
Inform impacted users and where appropriate all users of the vulnerability or incident and of mitigations, risk-based and proportionate, where appropriate in structured machine-readable form. Record what was sent, to whom and when.

## 6. Remediation and advisory
Develop and distribute the security update or mitigation under the vulnerability-handling process; publish the advisory once the update is available (Annex I Part II point (4)); report upstream and share fixes for component vulnerabilities (Article 13(6)).

## 7. Final report
Vulnerability: no later than 14 days after a corrective or mitigating measure is available: description with severity and impact, malicious actor information where available, details of the update or corrective measures. Incident: within one month after the 72-hour notification: detailed description with severity and impact, type of threat or root cause, applied and ongoing mitigations. Answer CSIRT requests for intermediate reports (Article 14(6)).

## 8. Records and review
Keep the full timeline, submissions, platform receipts, decisions and communications. Hold a post-event review; update the risk assessment (Article 13(7)); feed into regular testing (Annex I Part II point (3)).

## 9. Drill schedule
Rehearse at least {{DRILL_FREQUENCY}} with a fictional scenario; never file test notifications on the live platform. Record drills with `schemas/reporting-drill-record.schema.json`.
