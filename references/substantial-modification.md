# Substantial modification

Article 3(30): "a change to the product with digital elements following its placing on the market, which affects the compliance of the product with digital elements with the essential cybersecurity requirements set out in Part I of Annex I or which results in a modification to the intended purpose for which the product with digital elements has been assessed".

Why it matters:

- A substantially modified product is treated as a new product and its making available is a new placing on the market (guidance point 132). A new conformity assessment, updated technical documentation, updated declaration and a newly declared support period follow (guidance points 128 and 131).
- It brings products placed on the market before 11 December 2027 into the full regime (Article 69(2)).
- It turns an importer, distributor or any other person into a manufacturer for the modified part or the whole product (Articles 21 and 22).

## Software updates (guidance section 4.3)

The test is risk-based, not size-based (point 107). A change is substantial where it alters the level of cybersecurity risk and that altered or additional risk was not considered in the risk assessment (Recital 39; point 104).

**Likely substantial:** new functionality that changes the intended purpose as a whole (point 105; examples 40 and 41); seemingly minor features that introduce unassessed risks, such as a persistent login storing tokens locally (example 44) or an unencrypted diagnostics export (example 45).

**Likely not substantial:** functionality the risk assessment anticipated and mitigated (point 106; examples 42 and 43); security updates that fix vulnerabilities or harden configuration without changing the intended purpose or adding risk, even when technically significant (point 108; examples 46 to 48).

**Security updates that are substantial:** where the update changes the intended purpose beyond what was foreseen or materially alters the product's boundaries or dependency structure, for example by moving local processing to a remote service (example 49) or by introducing an external key-management dependency (example 50) (point 109).

### The four questions (point 110)

Does the update:

a. introduce new threat vectors (interfaces, communication channels, execution environments, external dependencies)?
b. enable new attack scenarios (new ways in which unauthorised access, manipulation, interference or misuse could plausibly occur)?
c. change the likelihood of previously identified attack scenarios (lower effort or expertise, increased exposure to untrusted actors, weakened safeguards)?
d. change the potential impact of previously identified attack scenarios (scope of affected data or functions, severity of consequences, ability to detect, contain or recover)?

Four "no" answers, with the risk assessment's assumptions and mitigations still valid, indicate no substantial modification (point 111). Any "yes" indicates the risk assessment must be updated and the change is likely substantial unless the risk was already covered.

## Hardware repairs and spare parts (guidance sections 4.1 and 4.2)

Repairs restoring the original state are not modifications. Spare parts replacing identical components manufactured to the same specifications are excluded from the CRA (Article 2(6)); a replacement with different cryptography or secure-boot behaviour is not identical.

## Consequences (guidance section 4.4)

- By the original manufacturer: new placing on the market, re-assessment against the Article 13(8) criteria for the support period (reassessment does not automatically reset or extend the period; guidance points 133 to 135), updated documentation and declaration.
- By another person: that person becomes the manufacturer for the affected part or the whole product (Article 22).

## Screening procedure (`delta` mode)

1. Describe the change set: features, interfaces, dependencies, data flows, deployment and configuration changes, with commits or release notes.
2. Answer the four questions with evidence, referring to the existing risk assessment.
3. Decide: not substantial; substantial; or undetermined pending risk-assessment update.
4. List the Annex I provisions whose evidence is invalidated by the change and must be re-assessed.
5. Record the decision with `python scripts/screen_substantial_modification.py` (`schemas/substantial-modification-screening.schema.json`).
6. Flag `legal_confirmation_recommended` when the change touches intended purpose, remote data processing or the product boundary.
