#!/usr/bin/env python3
"""Compare a current CRA readiness assessment with an accepted baseline (regression CI).

Exit codes: 0 no blocking regression, 1 input error, 2 blocking regression (or review-required items with --strict).

The script never promotes a provision to CONFORMANT. It compares recorded outputs only and is not
a substitute for re-assessment after a substantial modification.
"""
import argparse, csv, json, sys
from datetime import datetime, timezone
from pathlib import Path

MATRIX = '07-requirement-matrix.csv'; GAPS = '11-gaps-register.jsonl'; MANIFEST = '00-assessment-manifest.json'
NEGATIVE = {'GAP', 'BLOCKED', 'NOT_ASSESSED'}; POSITIVE = {'CONFORMANT', 'NOT_APPLICABLE'}
SEVERITY = {'Observation': 0, 'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}


def norm(v):
    v = (v or '').strip().upper().replace(' ', '_').replace('-', '_')
    return {'N/A': 'NOT_APPLICABLE', 'NA': 'NOT_APPLICABLE'}.get(v, v)


def read_matrix(base: Path):
    p = base / MATRIX
    if not p.exists():
        raise FileNotFoundError(p)
    out = {}
    with p.open(newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            pid = (row.get('provision_id') or '').strip()
            if not pid:
                continue
            if pid in out:
                raise ValueError(f'duplicate provision {pid} in {p}')
            row = dict(row); row['status'] = norm(row.get('status')); out[pid] = row
    return out


def read_gaps(base: Path):
    p = base / GAPS
    if not p.exists():
        return {}
    out = {}
    for n, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
        if line.strip():
            g = json.loads(line); key = g.get('regression_key') or g.get('gap_id')
            if not key:
                raise ValueError(f'gap without regression_key/gap_id at {p}:{n}')
            out[str(key)] = g
    return out


def read_manifest(base: Path):
    p = base / MANIFEST
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def gap_open(g):
    return str(g.get('status', '')).lower() not in {'closed', 'resolved', 'accepted-risk'}


def markdown(s):
    lines = ['# CRA regression summary', '', f"Generated: {s['generated_at']}", '', f"Baseline: `{s['baseline']}`  ", f"Current: `{s['current']}`", '',
             f"**Result:** {s['result']} | blocking regressions: {len(s['blocking_regressions'])} | review required: {len(s['review_required'])} | improvements: {len(s['improvements'])}", '']
    for title, items in (('Blocking regressions', s['blocking_regressions']), ('Review required', s['review_required']), ('Improvements', s['improvements'])):
        lines += [f'## {title}', ''] + ([f"- **{x.get('type')}**: {x.get('message')}" for x in items] or ['None.']) + ['']
    lines += ['## Limitation', '', s['limitation'], '']
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--baseline', required=True); ap.add_argument('--current', required=True); ap.add_argument('--output', required=True)
    ap.add_argument('--minimum-severity', choices=list(SEVERITY), default='Medium')
    ap.add_argument('--partial', action='store_true', help='current matrix may contain only the provisions re-checked')
    ap.add_argument('--strict', action='store_true', help='fail when review-required items exist')
    args = ap.parse_args()
    b, c, out = Path(args.baseline), Path(args.current), Path(args.output); out.mkdir(parents=True, exist_ok=True)
    bm, cm = read_matrix(b), read_matrix(c); bg, cg = read_gaps(b), read_gaps(c); bman, cman = read_manifest(b), read_manifest(c)
    reg, review, imp = [], [], []

    bsha = (bman.get('legal_baseline') or {}).get('regulation_sha256'); csha = (cman.get('legal_baseline') or {}).get('regulation_sha256')
    if bsha and csha and bsha != csha:
        review.append({'type': 'legal-baseline-change', 'message': 'Pinned regulation text hash changed between baseline and current; re-establish the baseline after human review.'})
    for key in ('date_regime', 'economic_operator_role'):
        if bman.get(key) and cman.get(key) and bman[key] != cman[key]:
            review.append({'type': f'{key}-change', 'message': f'{key} changed from {bman[key]} to {cman[key]}; scope decision must be reviewed.'})
    bcls = (bman.get('classification') or {}).get('class'); ccls = (cman.get('classification') or {}).get('class')
    if bcls and ccls and bcls != ccls:
        review.append({'type': 'classification-change', 'message': f'Classification changed from {bcls} to {ccls}; conformity route must be reviewed.'})
    if (cman.get('substantial_modification_screening') or {}).get('conclusion') == 'substantial':
        review.append({'type': 'substantial-modification', 'message': 'Current manifest records a substantial modification: new placing on the market; full re-assessment required.'})

    for pid, brow in sorted(bm.items()):
        if pid not in cm:
            if not args.partial:
                reg.append({'type': 'missing-current-provision', 'provision_id': pid, 'message': f'{pid} exists in baseline but is missing from the current matrix.'})
            continue
        bs, cs = brow['status'], cm[pid]['status']
        if bs in POSITIVE and cs in NEGATIVE:
            reg.append({'type': 'provision-regression', 'provision_id': pid, 'from': bs, 'to': cs, 'message': f'{pid} regressed {bs} -> {cs}.'})
        elif bs in POSITIVE and cs in POSITIVE and bs != cs:
            review.append({'type': 'applicability-change', 'provision_id': pid, 'message': f'{pid} changed {bs} -> {cs}; review the Article 13(4) justification.'})
        elif bs in NEGATIVE and cs in POSITIVE:
            imp.append({'type': 'provision-improvement', 'provision_id': pid, 'message': f'{pid} improved {bs} -> {cs}; closure depends on current evidence.'})
        elif bs == 'GAP' and cs in {'BLOCKED', 'NOT_ASSESSED'}:
            reg.append({'type': 'evidence-regression', 'provision_id': pid, 'from': bs, 'to': cs, 'message': f'{pid} changed {bs} -> {cs}; the prior gap is not shown remediated.'})
    for pid in sorted(set(cm) - set(bm)):
        review.append({'type': 'new-provision', 'provision_id': pid, 'message': f'{pid} is present in the current matrix but not the baseline; review catalogue or scope change.'})

    th = SEVERITY[args.minimum_severity]
    for key, cur in cg.items():
        sev = SEVERITY.get(str(cur.get('rating', 'Observation')), 0)
        if gap_open(cur) and sev >= th:
            base = bg.get(key)
            if base is None:
                reg.append({'type': 'new-gap', 'gap_key': key, 'message': f"New open {cur.get('rating')} gap {cur.get('gap_id', key)}: {cur.get('title', '')}"})
            elif not gap_open(base):
                reg.append({'type': 'reopened-gap', 'gap_key': key, 'message': f"Previously closed gap reopened: {cur.get('gap_id', key)} {cur.get('title', '')}"})
    for key, base in bg.items():
        cur = cg.get(key)
        if cur and gap_open(base) and not gap_open(cur):
            imp.append({'type': 'gap-closed', 'gap_key': key, 'message': f"Gap closed: {cur.get('gap_id', key)} {cur.get('title', '')}"})

    summary = {'generated_at': datetime.now(timezone.utc).isoformat(), 'baseline': str(b), 'current': str(c), 'partial_comparison': args.partial,
               'minimum_gap_severity': args.minimum_severity, 'blocking_regressions': reg, 'review_required': review, 'improvements': imp,
               'result': 'FAIL' if reg or (args.strict and review) else 'PASS',
               'limitation': 'This comparison detects differences in recorded readiness outputs. It is not a conformity assessment, does not carry CONFORMANT forward where new evidence is required, and does not replace re-assessment after a substantial modification.'}
    (out / 'regression-summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    (out / 'regression-summary.md').write_text(markdown(summary), encoding='utf-8')
    print(json.dumps({'result': summary['result'], 'regressions': len(reg), 'review_required': len(review), 'improvements': len(imp)}))
    return 2 if summary['result'] == 'FAIL' else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f'ERROR: {type(e).__name__}: {e}', file=sys.stderr); sys.exit(1)
