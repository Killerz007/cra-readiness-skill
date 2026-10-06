# AI compatibility

The methodology is agent-neutral. The portable core is:

- `SKILL.md`: canonical methodology with Agent Skills style frontmatter (`name`, `description`);
- `AGENTS.md`: generic repository-agent instructions;
- `prompts/portable-agent-prompt.md`: fallback for systems that can read files but not skills;
- `.claude/commands/cra-audit.md`: Claude Code command adapter (copy into the product repository's `.claude/commands/`);
- `.cursor/rules/cra-readiness.mdc`: Cursor adapter (copy into the product repository's `.cursor/rules/`).

The adapters shipped here only take effect once placed inside the **product** repository or the agent's own skills or rules directory.

## One-line pointer for instruction-file agents

For agents that read a project-level instruction file (`AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.windsurfrules`, `CLAUDE.md`), add this line to the product repository's file, adjusting the path:

```text
When assessing a product against the EU Cyber Resilience Act (Regulation (EU) 2024/2847), read and follow ../cra-readiness-skill/SKILL.md in full. Use the pinned official texts as criteria, never claim conformity or CE marking, and never give legal advice.
```

## Per-agent notes

| Agent | Discovery mechanism | Notes |
|---|---|---|
| Claude Code | `SKILL.md` under `~/.claude/skills/<name>/` or `<product>/.claude/skills/<name>/` | Clone this repository directly as the skill folder. The `description` frontmatter drives triggering. |
| OpenAI Codex | `AGENTS.md` in the product repository | One-line pointer, or copy this repository's `AGENTS.md`. |
| Cursor | `.cursor/rules/*.mdc` | Copy the shipped `.mdc` and fix the path. |
| GitHub Copilot | `.github/copilot-instructions.md` | One-line pointer. |
| Gemini CLI | `GEMINI.md` | One-line pointer. |
| Windsurf | `.windsurfrules` | One-line pointer. |
| Agent Skills loaders (`npx skills add` and similar) | tool-specific skills directory | Install as `cra-readiness`. |
| ChatGPT and browser agents with GitHub access | none | Provide the repository URL and the portable prompt. |

## Capabilities that change the output

- Document rendering: without a DOCX or PDF skill, use the Pandoc, LibreOffice or headless-browser fallback in `references/report-artifact-generation.md`; without any shell, record `BLOCKED_RENDERING`.
- Network: without network access the agent works against the pinned baseline and must state its age; the time-sensitive checks in `references/legal-status-and-dates.md` are then recorded as "not verified".
- Runtime access: without an authorised test unit or environment, runtime-dependent provisions are BLOCKED.
