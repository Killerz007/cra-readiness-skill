# Economic operator roles

The CRA attaches obligations to roles, not to company types. Identify the role for *this product* before assessing anything; a company can be manufacturer of one product and steward or distributor of another.

## Manufacturer (Article 3(13), Articles 13 and 14)

"A natural or legal person who develops or manufactures products with digital elements or has products with digital elements designed, developed or manufactured, and markets them under its name or trademark, whether for payment, monetisation or free of charge."

The full obligation set: essential requirements, risk assessment, due diligence on components, vulnerability handling for the support period, reporting, technical documentation, conformity assessment, EU declaration of conformity, CE marking, identification and contact details, user information, corrective action, cooperation with authorities, and notification on cessation of operations.

**Deemed manufacturers.** An importer or distributor that markets the product under its own name or trademark, or substantially modifies a product already on the market, becomes the manufacturer (Article 21). Any other person who substantially modifies a product and makes it available becomes the manufacturer for the modified part, or the whole product if the modification affects the product's cybersecurity as a whole (Article 22).

## Authorised representative (Article 3(15), Article 18)

Established in the EU with a written mandate. Must at least keep the declaration of conformity and technical documentation available for 10 years or the support period, whichever is longer; provide information on reasoned request; and cooperate with authorities. The mandate cannot transfer Article 13(1) to (11), the first subparagraph of Article 13(12), or Article 13(14). A non-EU manufacturer is not obliged to appoint one, but the Article 14(7) fallback order for the reporting CSIRT starts with the Member State of the authorised representative.

## Importer (Article 3(16), Article 19)

Places on the EU market a product bearing the name or trademark of a person established outside the EU. Before placing on the market the importer must verify that the manufacturer carried out the conformity assessment, drew up technical documentation, affixed the CE marking, supplied the declaration and Annex II user information in an understandable language, and complied with identification, contact and support-period display duties (Article 13(15), (16), (19)). The importer adds its own contact details, must not place a non-conforming product on the market, informs the manufacturer and authorities of vulnerabilities and significant risks, keeps the declaration for 10 years or the support period, and cooperates with authorities.

## Distributor (Article 3(17), Article 20)

Makes the product available without affecting its properties. Verifies CE marking and that manufacturer and importer complied with identification, contact, user-information, support-period and declaration duties; acts on non-conformity; passes vulnerability information to the manufacturer; informs authorities of significant risks; and informs authorities and users when it learns the manufacturer has ceased operations.

## Open-source software steward (Article 3(14), Article 24)

"A legal person, other than a manufacturer, that has the purpose or objective of systematically providing support on a sustained basis for the development of specific products with digital elements, qualifying as free and open-source software and intended for commercial activities, and that ensures the viability of those products."

Light regime: a documented, verifiable cybersecurity policy fostering secure development and effective vulnerability handling, including voluntary reporting; cooperation with market surveillance authorities; reporting of actively exploited vulnerabilities to the extent the steward is involved in development, and of severe incidents affecting the infrastructure it provides for development (Article 24(3)). Steward obligations apply from 11 December 2027. Stewards are not subject to administrative fines (Article 64(10)(b)). See `references/open-source.md`.

## Individual contributors

Contributors to a project they do not control are outside the CRA, including when they contribute security fixes (guidance section 3.4). A natural person cannot be a steward.

## Users and integrators

Users have no CRA obligations. An integrator that places its own product on the market is the manufacturer of that product and must exercise due diligence on integrated components (Article 13(5)); it must report upstream vulnerabilities it finds in components and share fixes (Article 13(6)).

## Role decision record

State the role, the basis (who develops, whose name or trademark, where established, whether modification occurred), and the consequences for this assessment: which of Articles 13, 14, 18, 19, 20, 24 are assessed, and whether the fallback CSIRT order under Article 14(7) is relevant.
