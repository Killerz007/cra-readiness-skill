# Remote data processing solutions

Article 3(2): remote data processing means "data processing at a distance for which the software is designed and developed by the manufacturer, or under the responsibility of the manufacturer, and the absence of which would prevent the product with digital elements from performing one of its functions". A product with digital elements includes its remote data processing solutions (Article 3(1)), so they are inside the product boundary for the risk assessment, the essential requirements and Article 14 reporting (guidance point 178).

## The three cumulative tests (guidance section 8.1)

1. **At a distance.** Processing outside the user's environment, typically cloud or edge computing, whether on public cloud, private cloud or the manufacturer's own premises (points 185 to 187).
2. **Its absence would prevent a function.** "Function" is not limited to core functionality; it includes supporting functions. Examples of qualifying functions: sending commands to a device, synchronising files, onboarding users, configuration and personalisation, automated distribution of updates including security patches, identity and access management (point 190). A function available both remotely and manually still counts (point 191). Telemetry analysed purely for statistics or future development does not count (point 192). A website counts only if it enables or supports a function, for example an authentication portal issuing credentials the product needs (point 194).
3. **Designed and developed by the manufacturer or under its responsibility.** In-house development qualifies, as does software built solely by or for the manufacturer to its designs and specifications. Merely licensing an existing third-party product or service, or a slightly modified version, does not (point 195). Who operates the solution is not decisive (point 196).

Cloud service models (points 197 to 200): with IaaS and PaaS the manufacturer's deployed software qualifies as remote data processing if the other tests are met; a third-party SaaS application integrated into the product does not, because it was not developed by or for the manufacturer.

## What is not inside the product boundary

The manufacturer's corporate IT, HR, CRM, CI/CD pipelines, update distribution edge locations, and auditing or testing systems such as penetration testing infrastructure are not remote data processing solutions (point 182). Elements that do not qualify but affect the product's security (a third-party hypervisor, PaaS operating system, SaaS application) are treated as third-party components subject to Article 13(5) due diligence (point 201). Cloud services themselves fall under NIS2 and Implementing Regulation (EU) 2024/2690 (point 183).

## Assessment consequences

For each qualifying remote data processing solution:

- include it in the architecture, data-flow and trust-boundary documentation;
- include it in the cybersecurity risk assessment and in each Annex I Part I requirement decision (access control, confidentiality, integrity, availability, logging, data minimisation, attack surface);
- include it in the SBOM scope and the vulnerability-handling and update processes;
- include it in the Article 14 process: an actively exploited vulnerability or severe incident in the backend is reportable;
- apply Annex I Part II (3) testing to it;
- where a substantial modification is made to the backend alone, apply `references/substantial-modification.md` (guidance example 55).

For non-qualifying remote services that the product relies on, document the product-level mitigations the risk assessment requires (cryptographic authentication of remote commands, integrity verification of configuration, fail-secure behaviour on outage, security logging) under guidance points 168 to 169.

## Decision record

Record, per remote component: name and owner; the three test answers with evidence; the conclusion (remote data processing solution, third-party component, or out of boundary); and the obligations that follow.
