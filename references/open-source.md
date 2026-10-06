# Free and open-source software under the CRA

Definition, Article 3(48): software whose source code is openly shared and which is made available under a free and open-source licence providing all rights to make it freely accessible, usable, modifiable and redistributable.

The CRA applies to free and open-source software (FOSS) only where it is **made available on the market in the course of a commercial activity** (Recital 18: provision of FOSS "that are not monetised by their manufacturers should not be considered to be a commercial activity"). The Commission guidance, section 3, gives the operative tests. Apply them per project, because one legal person can be manufacturer of one FOSS product and steward of another (guidance points 72 to 74).

## Step 1: who is responsible for the software?

Identify the natural or legal person under whose responsibility the FOSS is developed and released (guidance section 3.1). Contributors who do not control development, releases or distribution decisions have no obligations, even when they contribute security patches (section 3.4).

## Step 2: is it placed on the market? (guidance section 3.2)

| Fact pattern | Outcome |
|---|---|
| A price is charged for the software itself (for example for binaries) | Placed on the market; the person is a manufacturer (3.2.1). |
| Free "community" version alongside a paid or enhanced version (open core) | The paid version is placed on the market; the community version is not. A legal person is steward of the community version (3.2.1, points 52 to 53). |
| Software monetises other products or services through it (advertising, commissions, paid add-ons) | Placed on the market (3.2.2, examples 14 and 15). |
| Use is conditional on processing personal data for purposes other than security, compatibility or interoperability | Placed on the market (3.2.2, example 16). |
| Optional paid consultancy, training or professional services around freely available software | Not placed on the market (3.2.3, example 18). |
| Access to a version, maintenance, binaries, updates or guaranteed fixes is conditional on payment or on a "donation" | Placed on the market (3.2.3 point 57; 3.2.4 examples 21 and 22). |
| Voluntary donations without conditions, even above cost | Not a commercial activity (3.2.4, example 20). |
| A natural person charges only to recover actual costs including reasonable living expenses | Not a commercial activity (3.2.3, point 58). |
| Development funded or sponsored by a company, result freely shared | Funding does not make it commercial (3.2.5, example 23). The funder exercises Article 13(5) due diligence if it integrates it. |
| Not-for-profit entity using all earnings after costs for not-for-profit objectives | Not placed on the market; the entity is a steward (3.2.6, example 24). |
| Published for integration by other manufacturers and not monetised by the publisher | Not placed on the market; publisher may be a steward (3.2.7, examples 25 and 26). |

Note in the decision record that these tests are the Commission's non-binding reading; where money flows in any form, set `legal_confirmation_recommended = true`.

## Step 3: if not placed on the market, is the entity a steward?

Steward (Article 3(14)): a legal person, other than a manufacturer, that systematically provides sustained support for the development of specific FOSS intended for commercial activities and ensures its viability. Sustained support includes hosting and managing collaboration platforms, hosting source code, governing or steering development (Recital 19; guidance 3.3.1). Foundations are stewards for the specific projects they support in this way, not for everything they host (guidance point 78). A steward can provide only non-technical support and still be a steward; obligations are proportionate to the support provided.

Steward obligations (Article 24), applicable from 11 December 2027:

1. a documented, verifiable cybersecurity policy fostering secure development and effective vulnerability handling, including voluntary reporting (Article 15), covering documenting, addressing and remediating vulnerabilities and sharing information within the community;
2. cooperation with market surveillance authorities, including providing that policy on reasoned request;
3. reporting actively exploited vulnerabilities under Article 14(1) to the extent the steward is involved in development, and severe incidents under Article 14(3) and (8) where they affect the development infrastructure the steward provides.

Stewards are exempt from administrative fines (Article 64(10)(b)). A voluntary security attestation programme for FOSS may be established by the Commission (Article 25).

## Manufacturers integrating FOSS components

- Due diligence under Article 13(5) applies to every integrated component, including FOSS not placed on the market. Proportionate actions (Recital 34): check whether the component manufacturer demonstrated conformity (CE marking), check the security-update history, check vulnerability databases including the EU vulnerability database, run additional tests.
- Vulnerabilities found in a component must be reported upstream and fixes shared, where appropriate in machine-readable form and in a licence-compatible manner (Article 13(6); guidance 9.2.1). Reporting upstream is not required where the maintainer is already aware, where the component has no maintainer, or for vulnerabilities arising only from the integration.
- Integration has no effect on the component's own CRA status; the maintainer owes the integrator nothing under the CRA.
- The integrating manufacturer remains responsible for the whole product, including fixing or replacing an unsupported component (FAQ on integrated components).

## Conformity route for FOSS products in Annex III categories

Article 32(5): manufacturers of FOSS products in Annex III categories may use any Article 32(1) procedure, including module A, provided the technical documentation is made public at placing on the market.

## Assessment outputs

Record in the scope decision: the FOSS test applied, the monetisation facts, the resulting role (manufacturer, steward, none), and the obligations assessed. For stewards, assess Article 24 only, plus Article 14 readiness to the extent of Article 24(3).
