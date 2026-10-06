#!/usr/bin/env python3
"""Validate repository integrity: pinned sources, generated catalogues, assessment guide coverage, schemas, templates, examples."""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {'AI.P1': 15, 'AI.P2': 8, 'AII': 9, 'AV': 8, 'AVII': 8, 'A13': 25, 'A14': 10}
REQUIRED_FILES = [
    'README.md', 'SKILL.md', 'AGENTS.md', 'LICENSE', 'NOTICE', 'CHANGELOG.md',
    'official/upstream-manifest.json', 'official/current/CRA-2024-2847.xhtml', 'official/current/IR-2025-2392.xhtml',
    'references/legal-status-and-dates.md', 'references/scope-determination.md', 'references/product-classification.md', 'references/economic-operator-roles.md',
    'references/assessment-methodology.md', 'references/risk-assessment-methodology.md', 'references/requirement-assessment-guide.json', 'references/sbom-standard.md',
    'references/vulnerability-handling.md', 'references/reporting-obligations.md', 'references/support-period.md', 'references/substantial-modification.md',
    'references/technical-documentation.md', 'references/conformity-assessment-routes.md', 'references/harmonised-standards-status.md', 'references/open-source.md',
    'references/remote-data-processing.md', 'references/evidence-standard.md', 'references/authorized-testing.md', 'references/scanner-matrix.md', 'references/severity-methodology.md',
    'references/adjudication-standard.md', 'references/regression-ci.md', 'references/ticket-integration.md', 'references/reporting-standard.md', 'references/report-design.md', 'references/report-artifact-generation.md',
    'templates/cra-readiness-report.md', 'templates/report-disclaimer.md', 'templates/technical-documentation.md', 'templates/eu-declaration-of-conformity-DRAFT.md', 'templates/risk-assessment.md',
    'templates/article-14-reporting-playbook.md', 'templates/coordinated-vulnerability-disclosure-policy.md', 'templates/security.txt', 'templates/ci/cra-regression.yml',
    'agents/conformity-reviewer.md', 'prompts/portable-agent-prompt.md', 'adapters/ai-compatibility.md',
    'examples/sample-assessment/00-assessment-manifest.json', 'examples/sample-assessment/07-requirement-matrix.csv', 'examples/sample-assessment/11-gaps-register.jsonl', 'examples/sample-sbom.cdx.json',
]


def fail(msg):
    print('ERROR:', msg, file=sys.stderr); return False


def main():
    ok = True
    m = json.loads((ROOT / 'official/upstream-manifest.json').read_text(encoding='utf-8'))
    for key, src in m['sources'].items():
        p = ROOT / 'official' / 'current' / src['local_file']
        if not p.exists():
            ok = fail(f'pinned source missing: {p}') and ok
            continue
        import hashlib
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h != src['sha256']:
            ok = fail(f'{src["local_file"]} hash {h} differs from manifest {src["sha256"]}') and ok
    cat = json.loads((ROOT / 'references/cra-requirements-catalog.generated.json').read_text(encoding='utf-8'))
    reqs = cat['requirements']; ids = [r['id'] for r in reqs]
    if len(ids) != len(set(ids)):
        ok = fail('duplicate provision IDs in catalogue') and ok
    if cat.get('pinned_sha256') != m['sources']['regulation']['sha256']:
        ok = fail('catalogue was generated from a different regulation text than the manifest pins; run sync_official_text.py --rebuild-local') and ok
    # Count top-level items only (AII.8 counts, AII.8a does not) so sub-points cannot mask a missing item.
    counts = {k: sum(1 for i in ids if re.fullmatch(re.escape(k) + r'\.\d+[a-z]?', i) and (k in ('AI.P1',) or not re.search(r'\d[a-z]$', i))) for k in EXPECTED_COUNTS}
    for k, v in EXPECTED_COUNTS.items():
        if counts[k] != v:
            ok = fail(f'catalogue count {k}={counts[k]}, expected {v}') and ok
    empty = [r['id'] for r in reqs if not r.get('text')]
    if empty:
        ok = fail(f'provisions with empty text: {empty}') and ok
    guide = json.loads((ROOT / 'references/requirement-assessment-guide.json').read_text(encoding='utf-8'))['entries']
    missing = sorted(set(ids) - set(guide)); extra = sorted(set(guide) - set(ids))
    if missing:
        ok = fail(f'assessment guide lacks entries for: {missing}') and ok
    if extra:
        ok = fail(f'assessment guide has entries for unknown provisions: {extra}') and ok
    for pid, e in guide.items():
        if e.get('assessable', True) and not (e.get('evidence') and e.get('tests')):
            ok = fail(f'guide entry {pid} lacks evidence or tests') and ok
    cats = json.loads((ROOT / 'references/cra-product-categories.generated.json').read_text(encoding='utf-8'))
    for key, n in (('important_class_I', 19), ('important_class_II', 4), ('critical', 3)):
        if len(cats['annex_iii_iv_categories'][key]) != n:
            ok = fail(f'Annex III/IV category count {key}={len(cats["annex_iii_iv_categories"][key])}, expected {n}') and ok
        if len(cats.get('technical_descriptions', {}).get(key, [])) != n:
            ok = fail(f'technical description count {key} is not {n}') and ok
    for path in sorted((ROOT / 'schemas').glob('*.json')) + sorted((ROOT / 'templates').glob('*.json')):
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except ValueError as e:
            ok = fail(f'{path.relative_to(ROOT)} invalid JSON: {e}') and ok
    for f in REQUIRED_FILES:
        if not (ROOT / f).exists():
            ok = fail(f'missing {f}') and ok
    skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    fm = re.match(r'^---\n(.*?)\n---\n', skill, re.S)
    if not fm or 'name: cra-readiness' not in fm.group(1) or 'description:' not in fm.group(1):
        ok = fail('SKILL.md frontmatter missing name or description') and ok
    else:
        desc = re.search(r'description: >\n((?:  .*\n)+)', fm.group(1))
        if desc and len(' '.join(desc.group(1).split())) > 1024:
            ok = fail('SKILL.md description exceeds 1024 characters') and ok
    if skill.count('\n') > 520:
        ok = fail('SKILL.md exceeds 520 lines; move detail into references/') and ok
    sample = ROOT / 'examples/sample-assessment/07-requirement-matrix.csv'
    if sample.exists():
        with sample.open(newline='', encoding='utf-8') as f:
            rows = {r['provision_id'] for r in csv.DictReader(f)}
        if rows != set(ids):
            ok = fail(f'sample matrix provisions differ from catalogue: missing={sorted(set(ids) - rows)} extra={sorted(rows - set(ids))}') and ok
    print(f'Validated {len(ids)} provisions, {len(guide)} guide entries, {sum(len(v) for v in cats["annex_iii_iv_categories"].values())} product categories; regulation sha256 {m["sources"]["regulation"]["sha256"][:12]}...')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
