# Software bill of materials

## Legal requirement

Annex I Part II point (1): manufacturers shall "identify and document vulnerabilities and components contained in products with digital elements, including by drawing up a software bill of materials in a commonly used and machine-readable format covering at the very least the top-level dependencies of the products".

Definition, Article 3(39): "a formal record containing details and supply chain relationships of components included in the software elements of a product with digital elements".

Related provisions:

- Annex VII point 2(b): the SBOM is part of the vulnerability-handling specifications in the technical documentation.
- Annex VII point 8: the SBOM is provided to a market surveillance authority on reasoned request where necessary to check compliance.
- Annex II point 9: if the manufacturer chooses to make the SBOM available to users, the user information says where.
- Article 13(24): the Commission may specify SBOM format and elements by implementing act. None adopted as of the pinned status; check `references/legal-status-and-dates.md`.
- Article 13(25): authorities may request SBOMs for Union-wide dependency assessments.

The legal minimum is therefore: machine-readable, commonly used format, at least top-level dependencies, kept as part of the technical documentation, not required to be published.

## What this skill checks (`scripts/check_sbom.py`)

| Check | Level | Basis |
|---|---|---|
| Parses as CycloneDX (JSON, 1.4 to 1.6) or SPDX (JSON, 2.2 or 2.3) | required | "commonly used and machine-readable format" |
| Identifies the product (name and version) as the root or described component | required | Annex VII traceability |
| Lists at least the top-level dependencies, each with name and version | required | Annex I Part II (1) |
| Each component has a unique identifier (purl, CPE or SPDX ID) | recommended | needed to match vulnerability databases |
| Each component has a supplier or author | recommended | due diligence (Article 13(5)) |
| Dependency relationships are recorded | recommended | "supply chain relationships" in Article 3(39) |
| Creation timestamp and generating tool | recommended | reproducibility |
| Component hashes | optional | integrity |
| Licence information | optional | not a CRA requirement; useful for FOSS due diligence |
| Reconciles with the build's lockfiles or manifests | required where lockfiles exist | the SBOM must describe the product as built |
| Covers remote data processing solutions | required where they exist | they are part of the product |

Transitive dependencies are strongly recommended: vulnerability matching on top-level dependencies alone misses most exploitable issues, and the Commission's due-diligence expectations (Recital 34) are easier to evidence with full depth.

## Recommended practice beyond the minimum

- Generate the SBOM from the build pipeline for every release, not by hand.
- Keep one SBOM per product version and variant; the version that was placed on the market must be reproducible.
- Record the SBOM hash in the evidence index and reference it in the technical documentation.
- Where a national or sector guideline is used (for example the German BSI technical guideline TR-03183 part 2 on SBOM), cite its version; such guidelines are stricter than the CRA minimum and are not themselves legal requirements.
- Pair the SBOM with a vulnerability exploitability statement (VEX, for example CycloneDX VEX or OpenVEX) so that non-exploitable component vulnerabilities are documented rather than silently ignored; this supports the "known exploitable vulnerabilities" analysis under Annex I Part I (2)(a).
- Treat hardware bills of materials and firmware components as in scope for hardware products; the CRA SBOM covers the software elements, but the risk assessment needs the hardware too.

## Tooling (any of these, record the version)

Syft, CycloneDX generators (cdxgen and language-specific plugins), Trivy, SPDX tools, ecosystem-native generators (npm sbom, cargo-sbom, Maven and Gradle plugins). Validation: `scripts/check_sbom.py`, the CycloneDX CLI, SPDX tools.

## Common gaps

- SBOM produced once, never regenerated for later releases.
- SBOM lists only direct dependencies of one package manager and omits vendored code, container base images, firmware blobs or the backend.
- No identifiers, so vulnerability matching is impossible.
- SBOM not referenced from the technical documentation.
- Published SBOM contradicts the shipped build.
