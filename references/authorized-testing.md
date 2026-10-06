# Authorised and safe testing

Runtime testing is performed only against products, devices, installations and remote data processing solutions that the operator is authorised to test.

## Before any runtime test, record

target (device, firmware or build hash, installation, backend endpoint); environment owner; authorisation basis; permitted window; test accounts and roles; excluded endpoints, devices or services; whether third-party systems are reachable through the product.

## Prohibited

denial-of-service or resource-exhaustion attacks against production or shared infrastructure; high-volume brute force or credential stuffing; destructive modification outside dedicated test data or test devices; persistence, malware or backdoors; lateral movement into unrelated systems; extraction of real personal data; testing of third-party services the product depends on but the operator does not own; bypassing rate limits by distributing traffic; retrieval of real cloud credentials through metadata services; social engineering; physical attacks on devices that are not dedicated test units.

## Safe patterns for CRA requirements

- **Secure by default (2)(b):** inspect factory or first-boot configuration on a test unit; verify forced credential change, closed services, disabled debug interfaces, reset to original state.
- **Updates (2)(c), Part II (7) and (8):** on a test unit, apply a legitimate update and a tampered package; observe signature verification, transport protection, rollback behaviour and user notification. Never push tampered packages to production channels.
- **Access control (2)(d):** two test identities and test resources; verify unauthorised access is refused and reported.
- **Confidentiality and integrity (2)(e), (f):** inspect data at rest on a test unit and traffic from it; use protocol analysis, not interception of real users.
- **Availability (2)(h), (i):** review design and configuration; run bounded load tests only on isolated test environments with written authorisation.
- **Attack surface (2)(j):** port and interface inventory on test units; firmware image analysis.
- **Logging (2)(l):** generate test events and confirm records and opt-out behaviour.
- **Data removal (2)(m):** perform factory reset or account deletion on test data and verify residual data.
- **Vulnerability contact and CVD (Part II (5), (6)):** send a clearly labelled test report and record the handling.
- **Article 14 drill:** tabletop with a fictional scenario; never file a test notification on the live platform unless ENISA provides a test facility and the manufacturer authorises it.

If a requirement cannot be verified safely, mark it BLOCKED rather than escalating.
