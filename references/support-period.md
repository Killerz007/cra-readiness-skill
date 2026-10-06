# Support period

Definition, Article 3(20): the period during which the manufacturer must ensure that vulnerabilities of the product are handled effectively in accordance with Annex I Part II.

## Determination (Article 13(8))

The support period must reflect the length of time the product is expected to be in use, taking into account in particular:

- reasonable user expectations;
- the nature of the product, including its intended purpose;
- relevant Union law determining product lifetime.

The manufacturer may also take into account support periods of similar products from other manufacturers, availability of the operating environment, support periods of integrated third-party components providing core functions, and ADCO or Commission guidance. All factors are weighed proportionately.

**Floor:** at least five years, unless the product is expected to be in use for less than five years, in which case the support period equals the expected use time. Five years is a safeguard, not a default; products expected to be used longer need longer periods (guidance point 126; Recital 60 names hardware components, network devices, operating systems and industrial products as typical longer-use products). Shorter periods are justified only by a genuinely shorter expected use, such as a pandemic contact-tracing app or subscription-only software that stops working when the subscription ends (Recital 60; FAQ).

**Documentation:** the information taken into account must be in the technical documentation (Article 13(8), last subparagraph; Annex VII point 4).

**Delegated acts** may set minimum support periods for specific categories (Article 13(8)); none adopted as of the pinned status.

## Related obligations

| Obligation | Article |
|---|---|
| Security updates made available during the support period must remain available for at least 10 years after issue or for the remainder of the support period, whichever is longer | 13(9) |
| Remediation only for the latest substantially modified version is allowed where users of earlier versions can move to it free of charge and without additional costs to adjust their hardware and software environment; CVD policy and information-sharing measures continue for all versions | 13(10) |
| Public software archives of historical versions are allowed with clear, accessible risk information | 13(11) |
| Technical documentation and declaration kept for 10 years after placing on the market or the support period, whichever is longer | 13(13) |
| User information kept available, and if online kept online, for 10 years or the support period, whichever is longer | 13(18) |
| End date of the support period, at least month and year, clearly specified at the time of purchase, and on the product, packaging or by digital means where applicable; end-of-support notification where technically feasible | 13(19) |
| Annex II point 7: type of security support and end date of the support period in the user information | Annex II |

"Additional costs" in Article 13(10) does not include reasonable operational effort such as staff time, testing, configuration or dependency upgrades; it does include mandatory new hardware, infrastructure replacement or fundamental environment changes (guidance point 130).

## Iterative software (guidance points 128 to 131)

Each substantially modified version placed on the market needs a declared support period meeting Article 13(8). The manufacturer may rely on Article 13(10) to stop remediating earlier versions once users can upgrade free of charge and without additional costs, while continuing the other Part II obligations and Article 14 reporting for all versions. Users who have not upgraded should be told when remediation of their version stops, where technically feasible (Article 13(19)).

## Substantial modification and the support period (guidance section 5.1)

A substantial modification triggers reassessment against the Article 13(8) criteria but does not automatically reset or extend the period. Where the factors that set the expected use time (for example hardware durability) are unchanged, the support period of the modified product aligns with the remaining expected use time (examples 54 and 55). Where those factors change, recalculate.

## Assessment checklist

1. Is a support period declared for this product version? What is it?
2. Is the determination documented against each Article 13(8) factor, with the evidence (user expectations, product nature, Union law, comparable products, operating environment, component support, guidance)?
3. Is it at least five years, or is a shorter period justified by demonstrably shorter expected use?
4. Is the end date (month and year) shown at the time of purchase and in the user information?
5. Is there an end-of-support notification mechanism where technically feasible?
6. Are issued security updates retained for at least 10 years or the remainder of the support period?
7. For multi-version software: is Article 13(10) relied on, and are its conditions met and documented?
8. Are retention periods for documentation and user information calculated correctly?

`python scripts/support_period_check.py` computes the dates and flags the checks.

## After the support period

Vulnerability-handling obligations end, but Article 14 reporting continues for the product's lifetime (guidance point 210). Products can still be made available after the period ends; newly placed units need a new support period (FAQ).
