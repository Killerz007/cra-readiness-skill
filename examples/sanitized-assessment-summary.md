# Sanitised assessment summary (fictional)

**Product:** Example Sensor Hub 3.1.0 (industrial sensor gateway with manufacturer-developed cloud backend) | **Role:** manufacturer, main establishment NL | **Mode:** full | **Assessment period:** 1 to 6 October 2026

**Legal baseline:** Regulation (EU) 2024/2847 as pinned; Implementing Regulation (EU) 2025/2392; Delegated Regulation (EU) 2026/881; Commission guidance C(2026) 5252 (non-binding). Harmonised standards status check on 1 October 2026: none cited; presumption of conformity unavailable.

## Scope and classification

In scope: hardware with embedded software and a qualifying remote data processing solution (cloud device management backend developed by the manufacturer). Third-party SaaS analytics treated as an external component under Article 13(5). Not yet placed on the market; all obligations apply at placing on the market; Article 14 already applies. Classification: default category (core functionality is sensor data collection and forwarding; no routing, firewall or residential security function). Routes available: module A, B+C, H. Confidence High; counter-argument recorded (residential alarm use case).

## Results

| Status | Count |
|---|---:|
| Conformant | 83 |
| Gap | 7 |
| Not applicable (justified) | 4 |
| Blocked | 1 |
| Not assessed | 1 |

## Gaps

- **CRA-G-002 (Critical, live):** No Article 14 reporting capability: no single reporting platform registration, no CSIRT determination, no awareness procedure. Target: 15 November 2026.
- **CRA-G-001 (High):** Shared default administrator password in factory firmware (Annex I Part I (2)(b), (2)(d)). Target: before placing on the market.

## Conclusion

**Not ready.** One live obligation (Article 14) is unmet and one product requirement is in gap. Once remediated and retested, and with the blocked resilience evidence obtained on an isolated environment, the product would be a candidate for **Ready for conformity assessment (module A)**.

> Independent readiness assessment. Not a conformity assessment, notified-body evaluation, certification or legal advice. The manufacturer alone is responsible for conformity, the EU declaration of conformity and CE marking.
