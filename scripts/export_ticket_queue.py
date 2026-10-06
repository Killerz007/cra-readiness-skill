#!/usr/bin/env python3
"""Generate a portable GitHub/Jira-ready ticket queue from the CRA gaps register.

This script never creates external tickets. External creation is an explicitly authorised
agent or connector action as described in references/ticket-integration.md.
"""
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

SEVERITY = {'Observation': 0, 'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
PRIORITY = {'Critical': 'highest', 'High': 'high', 'Medium': 'normal', 'Low': 'low', 'Observation': 'backlog'}


def gap_open(g):
    return str(g.get('status', '')).lower() not in {'closed', 'resolved', 'accepted-risk'}


def body(g, version, commit):
    le = g.get('legal_exposure') or {}
    return f"""**Gap ID:** {g.get('gap_id', '')}
**Regression key:** `{g.get('regression_key') or g.get('gap_id', '')}`
**Severity:** {g.get('rating', '')}
**CRA provisions:** {', '.join(g.get('provision_ids') or [])}
**Applies from:** {le.get('applies_from', 'see report')} (live now: {le.get('live_now', 'unknown')})
**Assessed version:** `{version or 'not recorded'}` / `{commit or 'not recorded'}`

## Finding

{g.get('finding', '')}

## Risk and implication

{g.get('risk_and_implication', '')}

## Remediation

{g.get('recommendation', '')}

## Implementation guidance

{g.get('implementation_guidance') or ''}

## Documentation change

{g.get('documentation_change') or ''}

## Retest criteria

{g.get('retest_criteria', '')}

## Evidence references

{', '.join(g.get('evidence_ids') or []) or 'See assessment evidence index.'}

> This work item tracks remediation of an independent CRA readiness gap. Closing the ticket does not close the gap; retest evidence is required. It does not establish conformity with Regulation (EU) 2024/2847.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--assessment-dir', required=True); ap.add_argument('--output', default='')
    ap.add_argument('--minimum-severity', choices=list(SEVERITY), default='Low'); ap.add_argument('--include-observations', action='store_true')
    args = ap.parse_args()
    base = Path(args.assessment_dir); gpath = base / '11-gaps-register.jsonl'
    if not gpath.exists():
        raise FileNotFoundError(gpath)
    manifest = json.loads((base / '00-assessment-manifest.json').read_text(encoding='utf-8')) if (base / '00-assessment-manifest.json').exists() else {}
    version, commit = manifest.get('product_version'), manifest.get('commit_sha')
    th = SEVERITY[args.minimum_severity]; queue = []
    for n, line in enumerate(gpath.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        g = json.loads(line); sev = g.get('rating', 'Observation')
        if not gap_open(g) or (sev == 'Observation' and not args.include_observations) or SEVERITY.get(sev, 0) < th:
            continue
        key = g.get('regression_key') or g.get('gap_id')
        if not key:
            raise ValueError(f'gap at line {n} has no regression key or id')
        queue.append({'gap_id': g.get('gap_id'), 'regression_key': key, 'title': f"[CRA] {g.get('gap_id', '')} - {g.get('title', '')}", 'severity': sev,
                      'recommended_priority': PRIORITY.get(sev, 'normal'), 'provision_ids': g.get('provision_ids', []), 'dedupe_search_terms': [g.get('gap_id'), key], 'body': body(g, version, commit)})
    out = Path(args.output) if args.output else base; out.mkdir(parents=True, exist_ok=True)
    payload = {'generated_at': datetime.now(timezone.utc).isoformat(), 'assessment_product_version': version, 'ticket_creation_authorized': False,
               'note': 'Portable queue only. Search for duplicates and obtain explicit authorisation before creating external tickets.', 'tickets': queue}
    (out / '22-finding-ticket-queue.json').write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    md = ['# CRA gap ticket queue', '', f'Open queued gaps: **{len(queue)}**', '', '> Queue generation does not authorise external ticket creation.', '']
    for t in queue:
        md += [f"## {t['title']}", '', f"- Severity: **{t['severity']}**", f"- Recommended priority: `{t['recommended_priority']}`", f"- Regression key: `{t['regression_key']}`", '', t['body'], '']
    (out / '22-finding-ticket-queue.md').write_text('\n'.join(md), encoding='utf-8')
    print(json.dumps({'queued': len(queue), 'output': str(out)}))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f'ERROR: {type(e).__name__}: {e}', file=sys.stderr); sys.exit(1)
