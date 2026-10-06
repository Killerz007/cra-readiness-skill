#!/usr/bin/env python3
"""Hash every file under an evidence directory and write evidence-hashes.csv (artifact, sha256, bytes)."""
import argparse, csv, hashlib
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('evidence_dir'); ap.add_argument('--output', default='evidence-hashes.csv'); args = ap.parse_args()
    base = Path(args.evidence_dir); out = base / args.output
    rows = [(str(p.relative_to(base)), digest(p), p.stat().st_size) for p in sorted(x for x in base.rglob('*') if x.is_file() and x != out)]
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['artifact', 'sha256', 'bytes']); w.writerows(rows)
    print(out)


if __name__ == '__main__':
    main()
