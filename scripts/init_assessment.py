#!/usr/bin/env python3
"""Create an assessment directory with the manifest and empty registers.

Usage:
  python scripts/init_assessment.py --product "Acme Gateway" --version 2.4.0 [--commit <sha>] [--mode full] [--role manufacturer] ...
"""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPY = [
    ('requirement-matrix.csv', '07-requirement-matrix.csv'), ('evidence-index.csv', '08-evidence-index.csv'), ('scanner-register.csv', '09-scanner-register.csv'),
    ('adjudication-log.jsonl', '10-adjudication-log.jsonl'), ('gaps-register.jsonl', '11-gaps-register.jsonl'), ('remediation-register.csv', '12-remediation-register.csv'),
    ('component-due-diligence-register.csv', '05-component-due-diligence-register.csv'), ('test-procedure-traceability.csv', '19-test-procedure-traceability.csv'),
    ('report-rendering-manifest.json', '21-report-rendering-manifest.json'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--product', required=True); ap.add_argument('--version', required=True); ap.add_argument('--commit', default=None); ap.add_argument('--repository', default=None)
    ap.add_argument('--product-type', choices=['software', 'hardware_with_software', 'hardware', 'combination'], default='software')
    ap.add_argument('--mode', choices=['scope', 'classify', 'full', 'delta', 'retest', 'regression', 'reporting-drill', 'evidence-pack'], default='full')
    ap.add_argument('--role', choices=['manufacturer', 'authorised_representative', 'importer', 'distributor', 'open_source_steward', 'deemed_manufacturer_article_21', 'deemed_manufacturer_article_22', 'undetermined'], default='manufacturer')
    ap.add_argument('--authorization', choices=['authorized-runtime', 'source-review-only', 'unknown'], default='unknown')
    ap.add_argument('--ticket-mode', choices=['off', 'queue', 'github', 'jira', 'auto'], default='queue'); ap.add_argument('--authorize-ticket-creation', action='store_true')
    ap.add_argument('--output-root', default='cra-assessment')
    args = ap.parse_args()
    upstream = json.loads((ROOT / 'official' / 'upstream-manifest.json').read_text(encoding='utf-8'))
    src = upstream['sources']
    slug = ''.join(ch.lower() if ch.isalnum() else '-' for ch in f'{args.product}-{args.version}').strip('-')
    out = Path(args.output_root) / f'{datetime.now(timezone.utc).date().isoformat()}-{slug}'
    for d in ['evidence/raw', 'evidence/normalized', 'evidence/screenshots', 'evidence/runtime', 'evidence/code', '05-sbom']:
        (out / d).mkdir(parents=True, exist_ok=True)
    manifest = {
        'product_name': args.product, 'product_type': args.product_type, 'product_version': args.version, 'variants_covered': [], 'repository': args.repository, 'commit_sha': args.commit,
        'build_identifiers': [], 'artefact_hashes': {}, 'remote_data_processing_solutions': [], 'target_environment': None,
        'assessment_mode': args.mode, 'economic_operator_role': args.role, 'manufacturer_main_establishment_member_state': None,
        'authorization_status': args.authorization, 'ticket_mode': args.ticket_mode, 'external_ticket_creation_authorized': bool(args.authorize_ticket_creation),
        'started_at_utc': datetime.now(timezone.utc).isoformat(), 'assessor': None,
        'legal_baseline': {'regulation_sha256': src['regulation']['sha256'], 'implementing_regulation_2025_2392_sha256': src.get('implementing_regulation_2025_2392', {}).get('sha256'),
                           'delegated_regulation_2026_881_sha256': src.get('delegated_regulation_2026_881', {}).get('sha256'), 'manifest_last_checked_utc': upstream.get('last_checked_utc'), 'sync_check_result': None},
        'standards_status_check': {'performed_at_utc': None, 'harmonised_standards_cited': False, 'search_performed': None, 'result': 'not yet verified in this assessment; snapshot in references/harmonised-standards-status.md'},
        'date_regime': 'undetermined', 'scanner_versions': {},
    }
    (out / '00-assessment-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    for s, d in COPY:
        (out / d).write_text((ROOT / 'templates' / s).read_text(encoding='utf-8'), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
