# Gap severity methodology

Provision status and gap rating are separate. A gap's rating prioritises remediation; it never changes whether a provision is GAP.

## Rating

| Rating | Typical basis |
|---|---|
| Critical | A confirmed exploitable weakness in the product with severe impact, or a missing obligation that is already live and enforceable (for example no Article 14 reporting capability after 11 September 2026), or a scope or classification error that would void the conformity route |
| High | Material shortfall against an essential requirement with practical exploitability, or an absent mandatory process (no CVD policy, no SBOM, no update mechanism), or a support period or documentation decision that cannot be defended |
| Medium | Partial implementation with constrained impact, a process that exists but is not enforced or evidenced, documentation that is incomplete in substance |
| Low | Narrow or defence-in-depth shortfall, documentation formality, evidence hygiene |
| Observation | Improvement opportunity that is not a CRA shortfall |

## Inputs

- Technical severity: CVSS v4.0 where the gap is a confirmed vulnerability; application context over raw score.
- Legal exposure: which provision, whether it is live now or from 11 December 2027, and the Article 64 fine tier.
- Breadth: product population, variants and remote data processing solutions affected.
- Reversibility: whether users can mitigate.

## Confidence

Confirmed (reproduced or directly evidenced); High confidence (strong static evidence); Needs validation (credible indication, insufficient evidence; never presented as confirmed).

## Prioritisation for the remediation register

Order by: live obligations first; then conformity-route blockers; then Critical and High product weaknesses; then documentation completeness; then the rest. Set target dates relative to the applicable legal date and the manufacturer's release plan.
