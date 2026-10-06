#!/usr/bin/env python3
"""Validate an SBOM against the Cyber Resilience Act minimum and recommended practice.

Legal minimum (Annex I Part II point (1)): a software bill of materials "in a commonly used and
machine-readable format covering at the very least the top-level dependencies of the products".
This script checks CycloneDX JSON (1.4 to 1.6) and SPDX JSON (2.2, 2.3) documents, optionally
reconciles them with a lockfile or manifest, and writes a report (schemas/sbom-check-report.schema.json).

Usage:
  python scripts/check_sbom.py sbom.cdx.json [--lockfile package.json] [--output report.json] [--markdown report.md]

Exit codes: 0 PASS or PASS_WITH_WARNINGS, 2 FAIL, 1 error.
"""
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

LEGAL = 'Annex I Part II point (1), Regulation (EU) 2024/2847'


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


class Report:
    def __init__(self):
        self.checks = []

    def add(self, cid, level, status, message, legal=None):
        self.checks.append({'id': cid, 'level': level, 'status': status, 'message': message, 'legal_basis': legal})

    def result(self):
        if any(c['level'] == 'required' and c['status'] == 'fail' for c in self.checks):
            return 'FAIL'
        if any(c['status'] in ('fail', 'warn') for c in self.checks):
            return 'PASS_WITH_WARNINGS'
        return 'PASS'

# ----------------------------------------------------------------------------- parsers

def parse_cyclonedx(doc: dict, r: Report):
    spec = str(doc.get('specVersion', ''))
    if spec not in {'1.4', '1.5', '1.6'}:
        r.add('format.spec_version', 'required', 'warn' if spec else 'fail', f'CycloneDX specVersion {spec or "missing"}; expected 1.4 to 1.6', LEGAL)
    else:
        r.add('format.spec_version', 'required', 'pass', f'CycloneDX {spec}', LEGAL)
    meta = doc.get('metadata', {}) or {}
    root = meta.get('component') or {}
    root_ref = root.get('bom-ref')
    if root.get('name') and root.get('version'):
        r.add('product.identified', 'required', 'pass', f"Product identified as {root['name']} {root['version']}", 'Annex VII point 1(b)')
    else:
        r.add('product.identified', 'required', 'fail', 'metadata.component must identify the product with name and version', 'Annex VII point 1(b)')
    if meta.get('timestamp'):
        r.add('metadata.timestamp', 'recommended', 'pass', f"Created {meta['timestamp']}")
    else:
        r.add('metadata.timestamp', 'recommended', 'warn', 'No creation timestamp')
    tools = meta.get('tools')
    if tools:
        r.add('metadata.tool', 'recommended', 'pass', 'Generating tool recorded')
    else:
        r.add('metadata.tool', 'recommended', 'warn', 'No generating tool recorded')
    comps = doc.get('components', []) or []
    deps = {d.get('ref'): d.get('dependsOn', []) for d in (doc.get('dependencies', []) or [])}
    top = deps.get(root_ref) if root_ref in deps else None
    return {'components': comps, 'top_level': top, 'has_dependency_graph': bool(deps), 'name_key': 'name', 'version_key': 'version',
            'id_of': lambda c: c.get('purl') or c.get('cpe') or (c.get('swid') or {}).get('tagId'),
            'supplier_of': lambda c: (c.get('supplier') or {}).get('name') or c.get('author') or c.get('publisher'),
            'hashes_of': lambda c: c.get('hashes'), 'license_of': lambda c: c.get('licenses'), 'ref_of': lambda c: c.get('bom-ref')}


def parse_spdx(doc: dict, r: Report):
    ver = str(doc.get('spdxVersion', ''))
    if ver not in {'SPDX-2.2', 'SPDX-2.3'}:
        r.add('format.spec_version', 'required', 'warn' if ver else 'fail', f'SPDX version {ver or "missing"}; expected SPDX-2.2 or SPDX-2.3', LEGAL)
    else:
        r.add('format.spec_version', 'required', 'pass', ver, LEGAL)
    pkgs = doc.get('packages', []) or []
    by_id = {p.get('SPDXID'): p for p in pkgs}
    described = doc.get('documentDescribes') or [rel.get('relatedSpdxElement') for rel in doc.get('relationships', []) if rel.get('relationshipType') == 'DESCRIBES']
    root = by_id.get(described[0]) if described else None
    if root and root.get('name') and root.get('versionInfo'):
        r.add('product.identified', 'required', 'pass', f"Product identified as {root['name']} {root['versionInfo']}", 'Annex VII point 1(b)')
    else:
        r.add('product.identified', 'required', 'fail', 'Document must DESCRIBE a root package with name and versionInfo', 'Annex VII point 1(b)')
    ci = doc.get('creationInfo', {}) or {}
    r.add('metadata.timestamp', 'recommended', 'pass' if ci.get('created') else 'warn', f"Created {ci.get('created')}" if ci.get('created') else 'No creation timestamp')
    r.add('metadata.tool', 'recommended', 'pass' if any(str(c).startswith('Tool:') for c in ci.get('creators', [])) else 'warn', 'Generating tool recorded' if any(str(c).startswith('Tool:') for c in ci.get('creators', [])) else 'No generating tool recorded')
    rels = doc.get('relationships', []) or []
    top = None
    if root:
        top = [rel.get('relatedSpdxElement') for rel in rels if rel.get('spdxElementId') == root.get('SPDXID') and rel.get('relationshipType') in ('DEPENDS_ON', 'CONTAINS')]
        top = top or None
    comps = [p for p in pkgs if not root or p.get('SPDXID') != root.get('SPDXID')]

    def id_of(c):
        for ref in c.get('externalRefs', []) or []:
            if ref.get('referenceType') in ('purl', 'cpe23Type', 'cpe22Type'):
                return ref.get('referenceLocator')
        return None
    return {'components': comps, 'top_level': top, 'has_dependency_graph': any(rel.get('relationshipType') in ('DEPENDS_ON', 'CONTAINS') for rel in rels), 'name_key': 'name', 'version_key': 'versionInfo',
            'id_of': id_of, 'supplier_of': lambda c: c.get('supplier') or c.get('originator'), 'hashes_of': lambda c: c.get('checksums'),
            'license_of': lambda c: c.get('licenseConcluded') or c.get('licenseDeclared'), 'ref_of': lambda c: c.get('SPDXID')}

# ----------------------------------------------------------------------------- lockfile reconciliation

def lockfile_names(path: Path):
    text = path.read_text(encoding='utf-8', errors='replace'); name = path.name
    if name == 'package.json':
        d = json.loads(text); return set(d.get('dependencies', {})) | set(d.get('optionalDependencies', {})), 'package.json dependencies'
    if name == 'package-lock.json':
        d = json.loads(text); root = (d.get('packages') or {}).get('', {}); return set(root.get('dependencies', {})), 'package-lock.json root dependencies'
    if name == 'requirements.txt':
        names = set()
        for line in text.splitlines():
            line = line.split('#')[0].strip()
            if line and not line.startswith('-'):
                names.add(re.split(r'[<>=!~\[; ]', line, 1)[0].lower())
        return names, 'requirements.txt'
    if name == 'go.mod':
        names = set(); block = False
        for line in text.splitlines():
            s = line.strip()
            if s.startswith('require ('):
                block = True; continue
            if block and s == ')':
                block = False; continue
            if block and s and not s.startswith('//'):
                names.add(s.split()[0])
            elif s.startswith('require ') and not s.endswith('('):
                names.add(s.split()[1])
        return names, 'go.mod require'
    if name == 'pyproject.toml':
        m = re.search(r'dependencies\s*=\s*\[(.*?)\]', text, re.S)
        names = set(re.split(r'[<>=!~\[; ]', x.strip().strip('"\''), 1)[0].lower() for x in (m.group(1).split(',') if m else []) if x.strip())
        return names, 'pyproject.toml [project].dependencies'
    if name == 'Cargo.toml':
        m = re.search(r'\[dependencies\](.*?)(?:\n\[|\Z)', text, re.S)
        names = set(line.split('=')[0].strip() for line in (m.group(1).splitlines() if m else []) if '=' in line and not line.strip().startswith('#'))
        return names, 'Cargo.toml [dependencies]'
    raise ValueError(f'unsupported lockfile or manifest: {name}')

# ----------------------------------------------------------------------------- main

def check(path: Path, lockfile: Path | None):
    r = Report(); doc = json.loads(path.read_text(encoding='utf-8'))
    if doc.get('bomFormat') == 'CycloneDX':
        fmt = 'CycloneDX'; p = parse_cyclonedx(doc, r); spec = str(doc.get('specVersion', ''))
    elif str(doc.get('spdxVersion', '')).startswith('SPDX-'):
        fmt = 'SPDX'; p = parse_spdx(doc, r); spec = doc.get('spdxVersion')
    else:
        r.add('format.recognised', 'required', 'fail', 'Not a CycloneDX JSON (bomFormat) or SPDX JSON (spdxVersion) document', LEGAL)
        return r, {'format': 'unknown', 'spec_version': None, 'component_count': 0, 'top_level_dependency_count': None}, None
    r.add('format.recognised', 'required', 'pass', f'{fmt} JSON is a commonly used machine-readable format', LEGAL)
    comps = p['components']
    if not comps:
        r.add('components.present', 'required', 'fail', 'No components listed; the CRA minimum is at least the top-level dependencies', LEGAL)
    else:
        r.add('components.present', 'required', 'pass', f'{len(comps)} components listed', LEGAL)
    missing_nv = [c for c in comps if not (c.get(p['name_key']) and c.get(p['version_key']))]
    r.add('components.name_version', 'required', 'fail' if missing_nv else 'pass', f'{len(missing_nv)} components lack name or version' if missing_nv else 'All components have name and version', LEGAL)
    if p['top_level'] is None:
        r.add('top_level.identified', 'recommended', 'warn', 'Top-level dependencies cannot be distinguished: no dependency relationship from the product root. All components are treated as the flat inventory.', LEGAL)
        top_count = None
    else:
        top_count = len(p['top_level']); r.add('top_level.identified', 'recommended', 'pass', f'{top_count} top-level dependencies linked from the product root', LEGAL)
    r.add('dependency_graph', 'recommended', 'pass' if p['has_dependency_graph'] else 'warn', 'Dependency relationships recorded' if p['has_dependency_graph'] else 'No dependency relationships (Article 3(39) refers to supply chain relationships)', 'Article 3(39)')
    no_id = [c for c in comps if not p['id_of'](c)]
    r.add('components.identifier', 'recommended', 'warn' if no_id else 'pass', f'{len(no_id)} components lack a purl, CPE or SWID identifier (needed for vulnerability matching)' if no_id else 'All components carry a purl, CPE or SWID identifier')
    no_sup = [c for c in comps if not p['supplier_of'](c)]
    r.add('components.supplier', 'recommended', 'warn' if no_sup else 'pass', f'{len(no_sup)} components lack supplier or author' if no_sup else 'All components have a supplier or author', 'Article 13(5) due diligence')
    no_hash = [c for c in comps if not p['hashes_of'](c)]
    r.add('components.hashes', 'optional', 'warn' if no_hash else 'pass', f'{len(no_hash)} components lack hashes' if no_hash else 'All components have hashes')
    no_lic = [c for c in comps if not p['license_of'](c)]
    r.add('components.license', 'optional', 'warn' if no_lic else 'pass', f'{len(no_lic)} components lack licence information (not a CRA requirement)' if no_lic else 'Licence information present')
    recon = None
    if lockfile:
        names, label = lockfile_names(lockfile)
        sbom_names = {str(c.get(p['name_key'], '')).lower() for c in comps} | {str(c.get(p['name_key'], '')).lower().split('/')[-1] for c in comps}
        missing = sorted(n for n in names if n.lower() not in sbom_names and n.lower().split('/')[-1] not in sbom_names)
        recon = {'lockfile': str(lockfile), 'source': label, 'declared': len(names), 'missing_from_sbom': missing}
        r.add('lockfile.reconciliation', 'required', 'fail' if missing else 'pass', f'{len(missing)} declared top-level dependencies missing from the SBOM: {missing[:10]}' if missing else f'All {len(names)} declared dependencies from {label} appear in the SBOM', LEGAL)
    return r, {'format': fmt, 'spec_version': spec, 'component_count': len(comps), 'top_level_dependency_count': top_count}, recon


def markdown(report: dict) -> str:
    lines = [f"# SBOM check: {report['sbom_path']}", '', f"**Result:** {report['result']} | **Format:** {report['format']} {report.get('spec_version') or ''} | **Components:** {report['component_count']} | **SHA-256:** `{report['sha256']}`", '',
             '| Check | Level | Status | Message | Legal basis |', '|---|---|---|---|---|']
    for c in report['checks']:
        lines.append(f"| {c['id']} | {c['level']} | {c['status']} | {c['message']} | {c.get('legal_basis') or ''} |")
    if report.get('lockfile_reconciliation'):
        lr = report['lockfile_reconciliation']
        lines += ['', f"Lockfile reconciliation against {lr['source']}: {lr['declared']} declared, missing from SBOM: {lr['missing_from_sbom'] or 'none'}"]
    lines += ['', 'A PASS means the document meets the checked minimum; it does not establish conformity with the Cyber Resilience Act.', '']
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('sbom'); ap.add_argument('--lockfile'); ap.add_argument('--output'); ap.add_argument('--markdown')
    args = ap.parse_args()
    path = Path(args.sbom)
    r, meta, recon = check(path, Path(args.lockfile) if args.lockfile else None)
    report = {'sbom_path': str(path), 'sha256': sha256(path), **meta, 'result': r.result(), 'checks': r.checks, 'lockfile_reconciliation': recon, 'generated_at': datetime.now(timezone.utc).isoformat()}
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True); Path(args.output).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    if args.markdown:
        Path(args.markdown).write_text(markdown(report), encoding='utf-8')
    print(json.dumps({'result': report['result'], 'format': report['format'], 'components': report['component_count'], 'failed_required': [c['id'] for c in r.checks if c['level'] == 'required' and c['status'] == 'fail']}))
    return 2 if report['result'] == 'FAIL' else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f'ERROR: {type(e).__name__}: {e}', file=sys.stderr); sys.exit(1)
