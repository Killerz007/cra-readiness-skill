# Assessment methodology

## Objective

Determine, with evidence, whether a specific product version and the manufacturer's processes meet the CRA essential requirements and manufacturer obligations, identify every gap, and leave the manufacturer with the material it needs for its own conformity assessment: a risk assessment, technical documentation draft, test reports, SBOM, vulnerability-handling and reporting processes, user information, and a declaration draft.

## Assurance model

The CRA is a product-law instrument built on the New Legislative Framework. Conformity is demonstrated by the manufacturer through a conformity assessment procedure and documented in technical documentation. This skill therefore assesses two things at once:

1. **The product**: does it have the properties in Annex I Part I, as applied through the risk assessment?
2. **The manufacturer's processes**: do the vulnerability-handling processes in Annex I Part II, the lifecycle obligations in Article 13 and the reporting process in Article 14 exist, operate and leave evidence?

A product can be technically strong and still not ready because the processes or documentation are missing. A policy can exist and still not be conformant because it is not enforced.

## Lifecycle

1. **Initiation**: access, authorisation, pinning of law and product, role identification.
2. **Scope**: product with digital elements, commercial activity, exclusions, remote data processing, date regime, separately supplied components.
3. **Classification**: core functionality, class, available conformity routes, standards status.
4. **Discovery**: architecture, components, interfaces, data flows, update and logging mechanisms, remote services.
5. **Risk assessment**: Article 13(2) to (4), applicability of each Annex I Part I point (2) requirement, due diligence on components.
6. **Evidence collection and testing**: static, composition, configuration, runtime and process evidence.
7. **Provision assessment**: one status per provision, evidence-linked.
8. **Adjudication**: resolve conflicts and borderline decisions.
9. **Gaps and remediation**: prioritised against the legal deadlines.
10. **Documentation drafts**: Annex VII, Annex V, Annex II, CVD policy, support-period statement, reporting playbook.
11. **Report**: Markdown, DOCX, PDF with mandatory disclaimers.
12. **Retest, delta, regression** as requested.

## Evidence hierarchy

Strongest: reproducible runtime observation of the built product plus the code or configuration that produces the behaviour, plus process records (tickets, advisories, logs) showing the process actually ran. Weaker: policy documents, design intentions, vendor attestations. Weakest: statements without artefacts. Documentation-only evidence is acceptable for documentation obligations (Annex II, Annex VII, Annex V) and for process obligations where the process has not yet had occasion to run, provided the report says so.

## Sampling

Where a product family shares architecture, security-relevant design and intended purpose, a single risk assessment, technical documentation set and conformity assessment may cover the family (guidance section 7.4). Variants that differ in interfaces, software stacks, update mechanisms or remote connectivity must be assessed for those differences. Disclose the sampling and the variants covered.

## Applicability decisions

Annex I Part I point (2) requirements apply "on the basis of the cybersecurity risk assessment ... and where applicable". The decision belongs to the risk assessment and is written into the technical documentation with a clear justification (Article 13(4)). Typical justified exclusions: automatic-update behaviour for components intended for integration and for products in professional or industrial networks where users would not expect automatic updates (Recital 56); secure-by-default and free security updates for tailor-made products under explicit contractual terms with a business user (Annex I Part I (2)(b) and Part II (8); FAQ on tailor-made products). Part II requirements, Article 13 and Article 14 are never excluded on applicability grounds, although their implementation is proportionate to the risks.

## Independence of severity and conformance

A gap's rating prioritises remediation. A provision's status states conformance. A Low-rated gap can still make a provision GAP and the product not ready.

## What this assessment is not

It is not a conformity assessment procedure under Annex VIII, even when the manufacturer intends to use module A; the manufacturer performs that procedure itself using this material. It is not a notified-body EU-type examination. It is not legal advice; scope and classification conclusions are technical assessments of the facts against the text and the Commission guidance, and borderline cases are flagged for counsel.
