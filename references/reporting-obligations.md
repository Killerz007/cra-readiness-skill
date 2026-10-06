# Reporting obligations (Article 14, Articles 15 to 17, Delegated Regulation (EU) 2026/881)

Article 14 applies from **11 September 2026** to every in-scope product, including products placed on the market before 11 December 2027 (Article 69(3)), and continues after the support period ends. Readiness is therefore assessed as a live obligation.

## What must be reported

**Actively exploited vulnerability** (Article 3(42)): a vulnerability for which there is reliable evidence that a malicious actor has exploited it in a system without permission of the system owner. Zero-days found by researchers, bug-bounty hunters or test labs with no evidence of malicious exploitation are not reportable (voluntary reporting under Article 15 remains possible). A vulnerability in a third-party component is reportable by the product manufacturer if it is exploited in its product; if the vulnerable code is unreachable or has not been exploited in the product, it is not (guidance point 218; FAQ).

**Severe incident having an impact on the security of the product** (Article 14(5)): an incident that negatively affects, or is capable of negatively affecting, the product's ability to protect the availability, authenticity, integrity or confidentiality of sensitive or important data or functions; or that has led or could lead to the introduction or execution of malicious code in the product or in a user's network and information systems.

## Becoming aware (guidance points 211 to 217)

The clock starts when, after an initial assessment, the manufacturer has a reasonable degree of certainty that a vulnerability in its product is being actively exploited or that a severe incident has occurred and compromised the product's security. The initial assessment must be prompt; its start, steps and conclusion must be logged, because the awareness timestamp will be scrutinised. The guidance aligns this with NIS2 implementing regulation (EU) 2024/2690 recital 31 and the GDPR breach guidelines. No retroactive reporting of exploitation already known before 11 September 2026; exploitation first learned of after that date is reportable even if the vulnerability itself was known earlier.

## Timeline

| Step | Actively exploited vulnerability (Article 14(2)) | Severe incident (Article 14(4)) |
|---|---|---|
| Early warning | Without undue delay, in any event within **24 hours** of awareness; indicate Member States where the product is known to be available | Within **24 hours**; include whether unlawful or malicious acts are suspected; Member States |
| Notification | Within **72 hours** of awareness: product, general nature of exploit and vulnerability, corrective or mitigating measures taken and available to users, sensitivity indication | Within **72 hours**: nature, initial assessment, measures taken and available to users, sensitivity |
| Final report | No later than **14 days after a corrective or mitigating measure is available**: description with severity and impact, information on the malicious actor where available, details of the update or corrective measures | Within **one month after the 72-hour notification**: detailed description with severity and impact, type of threat or root cause, applied and ongoing mitigation |
| Intermediate reports | On request of the CSIRT (Article 14(6)) | Same |

Information already supplied in an earlier step need not be repeated. `scripts/reporting_deadlines.py` computes the deadlines from the awareness timestamp.

## Where to report

Via the ENISA single reporting platform (Article 16), simultaneously to the CSIRT designated as coordinator and ENISA:

- Platform: `https://portal.cra-srp.enisa.europa.eu` (live since 11 September 2026). EU Login with multi-factor authentication. One Primary Assigned Representative per manufacturer, up to 20 Secondary Assigned Representatives who can submit and update notifications.
- CSIRT: the endpoint of the Member State of the manufacturer's **main establishment**, meaning where cybersecurity decisions for its products are predominantly taken, or failing that where it has the most employees in the EU (Article 14(7)).
- Manufacturers without an EU establishment use, in order: the Member State of the authorised representative acting for the most products; of the importer placing the most products on the market; of the distributor making the most products available; of the most users. Subsequent reports may go to the same CSIRT first used (Article 14(7)).
- The platform fields are defined by ENISA's glossary; no implementing act on format under Article 14(10) has been identified as adopted.

## Informing users (Article 14(8))

After becoming aware, the manufacturer must inform impacted users and, where appropriate, all users, of the vulnerability or incident and of mitigations, where appropriate in a structured, machine-readable format. This is risk-based and proportionate: detailed disclosure may be limited to affected customers while exploitation risk is high, with broader disclosure once mitigated (guidance points 219 to 221). If the manufacturer fails to inform users in time, the CSIRT may.

## Confidentiality and delayed dissemination

The receiving CSIRT normally disseminates the notification to the CSIRTs of the Member States where the product is available. Under Article 16(2) and Delegated Regulation (EU) 2026/881 it may delay dissemination on cybersecurity-related grounds: sensitivity of the information where a mitigation is expected within 72 hours, where the information would enable easy exploitation, where partial sharing suffices, or where the CSIRT is a trusted intermediary in an ongoing coordinated disclosure (Article 3 of the delegated regulation); doubts about a specific CSIRT's confidentiality (Article 4); or a compromised platform (Article 5). The manufacturer can request a delay and should indicate sensitivity in the notification, but the decision is the CSIRT's and the manufacturer's deadlines do not change. In particularly exceptional circumstances under Article 16(2), third subparagraph, ENISA initially receives only limited information.

## Other provisions

- Voluntary reporting of other vulnerabilities, threats, incidents and near misses (Article 15) does not create extra obligations and may be prioritised below mandatory reports.
- Notification does not increase the notifying person's liability (Article 17(4)).
- After a fix is available, ENISA adds publicly known notified vulnerabilities to the EU vulnerability database in agreement with the manufacturer (Article 17(5)).
- CSIRTs provide helpdesk support, in particular to microenterprises and SMEs (Article 17(6)).
- Open-source software stewards report under Article 24(3) from 11 December 2027.

## Readiness checklist (assessed in every `full` run and in `reporting-drill`)

1. The organisation has decided which CSIRT it reports to and why (main establishment or fallback order), and recorded it.
2. Primary Assigned Representative registered on the platform with EU Login and multi-factor authentication; at least one Secondary Assigned Representative; access tested.
3. A written procedure from detection through initial assessment, awareness decision, early warning, 72-hour notification, final report, user information, CSIRT follow-up and record keeping, with named roles and 24/7 contactability.
4. Decision criteria and log template for "awareness".
5. Pre-drafted templates for the three notification stages, matching the platform fields.
6. Integration with the vulnerability-handling and incident-response processes, including the product's remote data processing solutions.
7. Evidence of at least one drill with timestamps, and lessons learned.
8. Awareness that the obligation covers products placed on the market before 11 December 2027 and products past their support period.

`templates/article-14-reporting-playbook.md` and `templates/article-14-notification-forms.md` provide the procedure and the forms.
