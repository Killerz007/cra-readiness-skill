# Evidence standard

Every provision status and every gap must be traceable to evidence that a market surveillance authority or notified body could follow.

## Evidence record fields (`schemas/evidence-record.schema.json`)

evidence ID; provision IDs; evidence type; source or tool; product version and commit; environment or target; timestamp; collector; procedure performed; expected result; observed result; conclusion supported; raw artefact path; SHA-256 of the raw artefact; redaction note; limitations.

## Evidence types, strongest first

1. Runtime observation of the built product or representative installation, with the request, response, screenshot or log, plus the code or configuration producing the behaviour.
2. Build artefacts: SBOM generated from the build, signed release manifests, update packages and their signatures.
3. Process records: tickets, advisories, release history, CVD intake logs, reporting-drill logs, platform registration confirmation.
4. Source and configuration excerpts with file and line references.
5. Machine-readable scanner output with versions and commands.
6. Policies, procedures and design documents.
7. Third-party attestations (component conformity evidence, certificates, audit reports).
8. Statements by the manufacturer without artefacts (acceptable only for facts that cannot have artefacts, such as commercial intent, and always labelled as statements).

## Standards per status

- `CONFORMANT`: evidence shows the legal text is satisfied for this product version; for process requirements, the process exists and has run or has been exercised in a drill.
- `NOT_APPLICABLE`: a written Article 13(4) justification tied to the risk assessment, with the facts that make it inapplicable.
- `GAP`: the shortfall is described against the text, not just against a best practice.
- `BLOCKED`: what was needed and why it could not be obtained.
- `NOT_ASSESSED`: not yet executed; never used to hide a gap.

## Raw evidence integrity

Never edit raw output after collection. Normalise separately. Hash material artefacts with `scripts/hash_evidence.py` and record hashes in `08-evidence-index.csv`.

## Sensitive information

Redact credentials, keys, tokens, personal data and unpatched exploit details. Record that redaction occurred. Never commit live secrets.
