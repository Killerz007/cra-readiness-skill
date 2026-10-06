# Scanner and test tool matrix

Tools produce leads and supporting evidence. No tool output alone makes a provision CONFORMANT. Record tool, version, command, scope, timestamps, output hash and adjudication status for every run (`09-scanner-register.csv`).

| Area | Tools and techniques | Provisions supported |
|---|---|---|
| SBOM generation and validation | Syft, cdxgen, Trivy, ecosystem generators; `scripts/check_sbom.py`, CycloneDX CLI, SPDX tools | AI.P2.1, AVII.2b, AVII.8 |
| Software composition analysis and known exploited vulnerabilities | OSV-Scanner, Grype, Trivy, Dependency-Track; cross-check EU vulnerability database, CISA KEV, vendor advisories; VEX for exploitability | AI.P1.2a, AI.P2.1, AI.P2.2, A13.5 |
| SAST | Semgrep, CodeQL, language linters with security rules | AI.P1.2d, 2e, 2f, 2j, 2k; AI.P2.3 |
| Secrets | Gitleaks, TruffleHog | AI.P1.2e, 2j |
| Configuration and defaults | Firmware analysis (binwalk, EMBA), container and IaC scanners (Trivy, Checkov), manual first-boot review | AI.P1.2b, 2j |
| Update mechanism | Manual protocol review, signature verification tests, TLS configuration checks (testssl.sh, sslyze) | AI.P1.2c, AI.P2.7, AI.P2.8 |
| Cryptography | Code review, cryptographic configuration review, protocol analysis | AI.P1.2e, 2f |
| Runtime and DAST | OWASP ZAP, Burp, manual API testing for the product's own interfaces and its remote data processing solutions | AI.P1.2d, 2f, 2h, 2j |
| Fuzzing | libFuzzer, AFL++, protocol fuzzers on test units | AI.P1.2k, AI.P2.3 |
| Logging and monitoring | Manual event generation and log review | AI.P1.2l |
| Data minimisation and deletion | Data-flow review, reset and deletion tests | AI.P1.2g, 2m |
| Availability | Design review, bounded load tests in isolated environments | AI.P1.2h, 2i |
| Process evidence | Ticket exports, advisory archives, release logs, drill records, platform registration screenshots | AI.P2.2 to 2.8, A13.x, A14.x |

## Limitations to disclose

SAST misses runtime configuration and authorisation logic; SCA reports package vulnerabilities, not exploitability in context; secret scanners report fixtures; DAST misses role-specific paths without accounts; firmware scanners miss custom formats; no scanner evaluates process obligations. State these limitations in the report.
