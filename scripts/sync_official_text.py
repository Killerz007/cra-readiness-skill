#!/usr/bin/env python3
"""Fetch, pin and parse the official Cyber Resilience Act texts.

Sources (all official EU publications, fetched from the Publications Office "cellar"):

* Regulation (EU) 2024/2847 (the CRA)                       CELEX 32024R2847
* Commission Implementing Regulation (EU) 2025/2392         CELEX 32025R2392
  (technical descriptions of important/critical products)
* Commission Delegated Regulation (EU) 2026/881             CELEX 32026R0881
  (grounds for delaying dissemination of notifications)

The script uses only the Python standard library. It writes the pinned XHTML into
``official/current/`` and rebuilds the generated catalogues under ``references/``.

Modes:
  --sync            download, pin and rebuild (network)
  --check           report whether any pinned source changed; exit 2 if so (network)
  --rebuild-local   rebuild catalogues from official/current without network
  --summary-json F  also write the run summary to F (for CI)

The cellar materialises a document manifestation lazily: the first request for an
uncached document can return HTTP 200 with an empty body. The fetcher therefore retries
with a short back-off and treats an empty body as "not ready yet".
"""
import argparse, hashlib, html, json, re, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / 'official' / 'current'
MANIFEST = ROOT / 'official' / 'upstream-manifest.json'
REFERENCES = ROOT / 'references'
UA = 'Mozilla/5.0 (compatible; cra-readiness-skill/1.0; +https://github.com/Killerz007/cra-readiness-skill)'

SOURCES = {
    'regulation': {
        'celex': '32024R2847',
        'title': 'Regulation (EU) 2024/2847 of the European Parliament and of the Council of 23 October 2024 (Cyber Resilience Act)',
        'eli': 'http://data.europa.eu/eli/reg/2024/2847/oj',
        'oj': 'OJ L, 2024/2847, 20.11.2024',
        'local_file': 'CRA-2024-2847.xhtml',
        'required': True,
    },
    'implementing_regulation_2025_2392': {
        'celex': '32025R2392',
        'title': 'Commission Implementing Regulation (EU) 2025/2392 of 28 November 2025 on the technical description of the categories of important and critical products with digital elements',
        'eli': 'http://data.europa.eu/eli/reg_impl/2025/2392/oj',
        'oj': 'OJ L, 2025/2392, 1.12.2025',
        'local_file': 'IR-2025-2392.xhtml',
        'required': True,
    },
    'delegated_regulation_2026_881': {
        'celex': '32026R0881',
        'title': 'Commission Delegated Regulation (EU) 2026/881 of 11 December 2025 specifying the terms and conditions for applying the cybersecurity-related grounds in relation to delaying the dissemination of notifications',
        'eli': 'http://data.europa.eu/eli/reg_del/2026/881/oj',
        'oj': 'OJ L, 2026/881, 20.4.2026',
        'local_file': 'CDR-2026-0881.xhtml',
        'required': False,
    },
}

# ----------------------------------------------------------------------------- fetching

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fetch_cellar(celex: str, attempts: int = 6, pause: float = 5.0) -> bytes:
    """Fetch the English XHTML manifestation of a CELEX document from the Publications Office."""
    url = f'http://publications.europa.eu/resource/celex/{celex}'
    last_err = None
    for i in range(attempts):
        req = urllib.request.Request(url, headers={
            'User-Agent': UA,
            'Accept': 'application/xhtml+xml',
            'Accept-Language': 'en',
        })
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
            if len(body) > 1000:
                return body
            last_err = f'empty body (attempt {i + 1})'
        except Exception as e:  # noqa: BLE001
            last_err = f'{type(e).__name__}: {e}'
        time.sleep(pause)
    raise RuntimeError(f'cellar fetch failed for {celex}: {last_err}')

# ----------------------------------------------------------------------------- text utilities

LABEL_RE = re.compile(r'^\((?:[a-z]{1,3}|[ivx]{1,5}|\d{1,3})\)$|^\d{1,3}\.$|^\d{1,3}\.\d{1,2}\.$')


def clean(s: str) -> str:
    s = html.unescape(s).replace('\xa0', ' ')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def tokens(fragment: str):
    """Yield text tokens in document order from an XHTML fragment.

    Each <p> and each top-level <span> becomes one token. Labels such as "(a)" or "1." are
    emitted as their own tokens because the OJ markup always places them in their own cell.
    """
    for m in re.finditer(r'<p[^>]*>(.*?)</p>|<span[^>]*>(.*?)</span>', fragment, re.S):
        raw = m.group(1) if m.group(1) is not None else m.group(2)
        if raw is None:
            continue
        if '<p' in raw:  # nested paragraph inside span: skip the wrapper, inner <p> is matched separately
            continue
        t = clean(re.sub(r'<[^>]+>', ' ', raw))
        if t:
            yield t


def structure(fragment: str):
    """Turn a fragment into [{'label': 'a'|None, 'path': 'c.i', 'text': ...}] preserving nesting.

    A label token applies to the next text token. Nesting is inferred from label type:
    numeric > letter > roman.
    """
    items = []
    pending = None
    stack = []  # (kind, label)

    def kind(label):
        core = label.strip('().')
        if core.isdigit() or re.fullmatch(r'\d+\.\d+', core):
            return 0
        if re.fullmatch(r'[ivx]+', core):
            # "(i)", "(v)" and "(x)" are ambiguous between a letter and a roman numeral.
            # If an open letter list is at the letter immediately before this one, it is the next letter.
            letters = [l for k, l in stack if k == 1]
            if letters and len(letters[-1]) == 1 and chr(ord(letters[-1]) + 1) == core:
                return 1
            return 2
        return 1

    for t in tokens(fragment):
        if LABEL_RE.match(t):
            pending = t
            continue
        if pending:
            k = kind(pending)
            while stack and stack[-1][0] >= k:
                stack.pop()
            stack.append((k, pending.strip('().')))
            items.append({'label': pending.strip('().'), 'path': '.'.join(l for _, l in stack), 'text': t})
            pending = None
        else:
            items.append({'label': None, 'path': '.'.join(l for _, l in stack) if stack else '', 'text': t})
    return items

# ----------------------------------------------------------------------------- regulation parsing

def parse_articles(doc: str):
    """Return {number: {'title': str, 'paragraphs': {pnum: {'text': str, 'points': [...]}}}}."""
    out = {}
    for m in re.finditer(r'<div class="eli-subdivision" id="art_(\d+)">(.*?)(?=<div class="eli-subdivision" id="art_\d+">|<div class="eli-subdivision" id="fnp_1">)', doc, re.S):
        num = int(m.group(1)); body = m.group(2)
        tm = re.search(r'<p class="oj-sti-art">(.*?)</p>', body, re.S)
        title = clean(re.sub(r'<[^>]+>', ' ', tm.group(1))) if tm else ''
        paragraphs = {}
        pdivs = list(re.finditer(r'<div id="(\d{3})\.(\d{3})">(.*?)(?=<div id="\d{3}\.\d{3}">|\Z)', body, re.S))
        if pdivs:
            for pm in pdivs:
                pnum = int(pm.group(2))
                items = structure(pm.group(3))
                text_parts = [it['text'] for it in items if it['label'] is None]
                points = [it for it in items if it['label'] is not None]
                # strip the leading "8. " numbering from the first subparagraph
                if text_parts:
                    text_parts[0] = re.sub(r'^\d{1,3}\.\s*', '', text_parts[0])
                paragraphs[pnum] = {'text': '\n'.join(text_parts), 'points': points}
        else:
            # unnumbered article: everything after the title
            after = body.split('</div>', 1)[1] if '</div>' in body else body
            items = structure(after)
            paragraphs[1] = {'text': '\n'.join(it['text'] for it in items if it['label'] is None),
                             'points': [it for it in items if it['label'] is not None]}
        out[num] = {'title': title, 'paragraphs': paragraphs}
    if len(out) < 60:
        raise ValueError(f'article parser found only {len(out)} articles; upstream format may have changed')
    return out


def parse_annexes(doc: str):
    """Return {'I': fragment_html, ...} for each annex container."""
    out = {}
    for m in re.finditer(r'<div class="eli-container" id="anx_([IVX]+)">(.*?)(?=<div class="eli-container" id="anx_|</body>)', doc, re.S):
        out[m.group(1)] = m.group(2)
    if set(out) != {'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'}:
        raise ValueError(f'annex parser found {sorted(out)}; expected I..VIII')
    return out


def annex_items(fragment: str, heading_filter=None):
    """Split an annex into headed sections (Part I / Class I ...) of structured items."""
    sections = []
    # split on group headings
    parts = re.split(r'(<p[^>]*class="oj-ti-grseq-1"[^>]*>.*?</p>)', fragment, flags=re.S)
    current = {'heading': '', 'items': []}
    for chunk in parts:
        hm = re.match(r'<p[^>]*class="oj-ti-grseq-1"[^>]*>(.*?)</p>', chunk, re.S)
        if hm:
            if current['items'] or current['heading']:
                sections.append(current)
            current = {'heading': clean(re.sub(r'<[^>]+>', ' ', hm.group(1))), 'items': []}
        else:
            current['items'].extend(it for it in structure(chunk) if not re.match(r'^ANNEX\s', it['text']))
    sections.append(current)
    return sections


def build_requirements(doc: str):
    """Generate the machine-readable catalogue of assessable provisions."""
    articles = parse_articles(doc)
    annexes = parse_annexes(doc)
    reqs = []

    # ---- Annex I
    for sec in annex_items(annexes['I']):
        part = 'I' if sec['heading'].startswith('Part I ') or sec['heading'].startswith('Part I ') or ('Part I ' in sec['heading'] and 'Part II' not in sec['heading']) else ('II' if 'Part II' in sec['heading'] else None)
        if part is None:
            continue
        intro = None
        for it in sec['items']:
            if it['label'] is None:
                continue
            path = it['path']
            if part == 'I' and path.isdigit():
                rid = f'AI.P1.{path}'
                reqs.append({'id': rid, 'source': 'Annex I, Part I, point (' + path + ')', 'kind': 'product-requirement', 'text': it['text']})
                intro = it['text'] if path == '2' else None
            elif part == 'I' and re.fullmatch(r'2\.[a-m]', path):
                letter = path.split('.')[1]
                reqs.append({'id': f'AI.P1.2{letter}', 'source': f'Annex I, Part I, point (2)({letter})', 'kind': 'product-requirement',
                             'chapeau': intro, 'text': it['text']})
            elif part == 'II' and path.isdigit():
                reqs.append({'id': f'AI.P2.{path}', 'source': 'Annex I, Part II, point (' + path + ')', 'kind': 'vulnerability-handling-requirement',
                             'chapeau': 'Manufacturers of products with digital elements shall:', 'text': it['text']})
    # ---- Annex II (user information)
    for sec in annex_items(annexes['II']):
        for it in sec['items']:
            if it['label'] is None:
                continue
            p = it['path']
            if re.fullmatch(r'\d+', p):
                reqs.append({'id': f'AII.{p}', 'source': f'Annex II, point {p}', 'kind': 'user-information', 'text': it['text']})
            elif re.fullmatch(r'\d+\.[a-z]', p):
                n, l = p.split('.')
                reqs.append({'id': f'AII.{n}{l}', 'source': f'Annex II, point {n}({l})', 'kind': 'user-information', 'text': it['text']})
    # ---- Annex V (declaration of conformity)
    for sec in annex_items(annexes['V']):
        for it in sec['items']:
            if it['label'] and re.fullmatch(r'\d+', it['path']):
                reqs.append({'id': f'AV.{it["path"]}', 'source': f'Annex V, point {it["path"]}', 'kind': 'declaration-of-conformity', 'text': it['text']})
    # ---- Annex VII (technical documentation)
    for sec in annex_items(annexes['VII']):
        for it in sec['items']:
            if it['label'] is None:
                continue
            p = it['path']
            if re.fullmatch(r'\d+', p):
                reqs.append({'id': f'AVII.{p}', 'source': f'Annex VII, point {p}', 'kind': 'technical-documentation', 'text': it['text']})
            elif re.fullmatch(r'\d+\.[a-z]', p):
                n, l = p.split('.')
                reqs.append({'id': f'AVII.{n}{l}', 'source': f'Annex VII, point {n}({l})', 'kind': 'technical-documentation', 'text': it['text']})
    # ---- Article 13 and 14 paragraphs
    for art, kind in ((13, 'manufacturer-obligation'), (14, 'reporting-obligation')):
        for pnum, para in sorted(articles[art]['paragraphs'].items()):
            entry = {'id': f'A{art}.{pnum}', 'source': f'Article {art}({pnum})', 'kind': kind, 'text': para['text']}
            if para['points']:
                entry['points'] = [{'label': p['path'], 'text': p['text']} for p in para['points']]
            reqs.append(entry)
    # ---- Annex III / IV category lists
    categories = {'important_class_I': [], 'important_class_II': [], 'critical': []}
    for sec in annex_items(annexes['III']):
        key = 'important_class_I' if sec['heading'].startswith('Class I') and not sec['heading'].startswith('Class II') else ('important_class_II' if sec['heading'].startswith('Class II') else None)
        if key is None:
            continue
        for it in sec['items']:
            if it['label'] and re.fullmatch(r'\d+', it['path']):
                categories[key].append({'number': int(it['path']), 'category': it['text']})
    for sec in annex_items(annexes['IV']):
        for it in sec['items']:
            if it['label'] and re.fullmatch(r'\d+', it['path']):
                categories['critical'].append({'number': int(it['path']), 'category': it['text']})

    # sanity checks (these are the counts in the published act)
    counts = {
        'AI.P1': sum(1 for r in reqs if r['id'].startswith('AI.P1.')),
        'AI.P2': sum(1 for r in reqs if r['id'].startswith('AI.P2.')),
        'AII': sum(1 for r in reqs if re.fullmatch(r'AII\.\d+', r['id'])),
        'AV': sum(1 for r in reqs if r['id'].startswith('AV.')),
        'AVII': sum(1 for r in reqs if re.fullmatch(r'AVII\.\d+', r['id'])),
        'A13': sum(1 for r in reqs if r['id'].startswith('A13.')),
        'A14': sum(1 for r in reqs if r['id'].startswith('A14.')),
        'AIII.I': len(categories['important_class_I']),
        'AIII.II': len(categories['important_class_II']),
        'AIV': len(categories['critical']),
    }
    expected = {'AI.P1': 15, 'AI.P2': 8, 'AII': 9, 'AV': 8, 'AVII': 8, 'A13': 25, 'A14': 10, 'AIII.I': 19, 'AIII.II': 4, 'AIV': 3}
    bad = {k: (counts[k], v) for k, v in expected.items() if counts[k] != v}
    if bad:
        raise ValueError(f'catalogue counts differ from the published act (found, expected): {bad}; upstream format may have changed')
    return articles, reqs, categories


def parse_technical_descriptions(doc: str):
    """Parse Implementing Regulation (EU) 2025/2392 annex tables into category -> technical description."""
    out = {'important_class_I': [], 'important_class_II': [], 'critical': []}
    annexes = {m.group(1): m.group(2) for m in re.finditer(r'<div class="eli-container" id="anx_([IVX]+)">(.*?)(?=<div class="eli-container" id="anx_|</body>)', doc, re.S)}
    if set(annexes) != {'I', 'II'}:
        raise ValueError(f'implementing regulation annexes found: {sorted(annexes)}; expected I and II')

    def rows(fragment, key):
        # Each category is an outer row: cell 1 holds a nested numbering table, cell 2 the description paragraphs.
        # Split on the outer row/cell openers: the nested numbering table has its own closing tags,
        # so matching to the next closing tag would end the row too early.
        for row in re.split(r'<tr class="oj-table">', fragment)[1:]:
            cells = re.split(r'<td[^>]*class="oj-table"[^>]*>', row)[1:]
            if len(cells) != 2:
                continue
            normals = [clean(re.sub(r'<[^>]+>', ' ', p)) for p in re.findall(r'<p class="oj-normal">(.*?)</p>', cells[0], re.S)]
            if len(normals) < 2 or not re.fullmatch(r'\d+\.', normals[0]):
                continue
            desc = [clean(re.sub(r'<[^>]+>', ' ', p)) for p in re.findall(r'<p class="oj-tbl-txt">(.*?)</p>', cells[1], re.S)]
            out[key].append({'number': int(normals[0].rstrip('.')), 'category': normals[1], 'technical_description': '\n'.join(p for p in desc if p)})

    # Annex I of the implementing regulation: Class I then Class II, separated by group headings
    pieces = re.split(r'(<p[^>]*class="oj-ti-grseq-1"[^>]*>.*?</p>)', annexes['I'], flags=re.S)
    key = None
    for piece in pieces:
        hm = re.match(r'<p[^>]*class="oj-ti-grseq-1"[^>]*>(.*?)</p>', piece, re.S)
        if hm:
            text = clean(re.sub(r'<[^>]+>', ' ', hm.group(1)))
            key = 'important_class_II' if text.startswith('Class II') else ('important_class_I' if text.startswith('Class I') else None)
            continue
        if key:
            rows(piece, key)
    rows(annexes['II'], 'critical')
    expected = {'important_class_I': 19, 'important_class_II': 4, 'critical': 3}
    bad = {k: (len(out[k]), v) for k, v in expected.items() if len(out[k]) != v}
    if bad:
        raise ValueError(f'technical-description parser counts differ (found, expected): {bad}')
    return out

# ----------------------------------------------------------------------------- writing

def write_catalogues(reg_doc: str, ir_doc: str | None, manifest_sources: dict):
    articles, reqs, categories = build_requirements(reg_doc)
    now = datetime.now(timezone.utc).isoformat()
    base = {'source': SOURCES['regulation']['title'], 'eli': SOURCES['regulation']['eli'], 'oj': SOURCES['regulation']['oj'],
            'pinned_sha256': manifest_sources.get('regulation', {}).get('sha256'), 'generated_at': now}
    (REFERENCES / 'cra-articles-index.json').write_text(json.dumps({**base, 'articles': [
        {'number': n, 'title': a['title'], 'paragraphs': len(a['paragraphs'])} for n, a in sorted(articles.items())]}, indent=2) + '\n', encoding='utf-8')
    (REFERENCES / 'cra-requirements-catalog.generated.json').write_text(json.dumps({**base,
        'note': 'Verbatim provisions extracted from the pinned Official Journal text. IDs are this repository\'s stable keys, not official numbering. Interpretive guidance lives in references/requirement-assessment-guide.json.',
        'requirements': reqs}, indent=2) + '\n', encoding='utf-8')
    cats = {**base, 'annex_iii_iv_categories': categories}
    if ir_doc:
        cats['technical_descriptions'] = parse_technical_descriptions(ir_doc)
        cats['technical_descriptions_source'] = SOURCES['implementing_regulation_2025_2392']['title']
        cats['technical_descriptions_eli'] = SOURCES['implementing_regulation_2025_2392']['eli']
    (REFERENCES / 'cra-product-categories.generated.json').write_text(json.dumps(cats, indent=2) + '\n', encoding='utf-8')
    # verbatim article/annex text for agents to quote without opening 700 KB of XHTML
    key_articles = [2, 3, 4, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 30, 31, 32, 64, 69, 71]
    text_dump = {**base, 'articles': {str(n): articles[n] for n in key_articles if n in articles}}
    (REFERENCES / 'cra-key-articles.generated.json').write_text(json.dumps(text_dump, indent=2) + '\n', encoding='utf-8')
    return {'articles': len(articles), 'requirements': len(reqs), 'categories': {k: len(v) for k, v in categories.items()}}


def write_review(old: dict, new: dict):
    lines = ['# Upstream CRA source change review', '', f'Generated: {datetime.now(timezone.utc).isoformat()}', '',
             '| Source | Previous SHA-256 | New SHA-256 |', '|---|---|---|']
    for key, src in SOURCES.items():
        o = (old.get('sources') or {}).get(key, {}).get('sha256', 'n/a'); n = (new.get('sources') or {}).get(key, {}).get('sha256', 'n/a')
        lines.append(f'| {src["celex"]} | `{o}` | `{n}` |')
    lines += ['', '## Required maintainer review', '',
              '- Confirm the change is a genuine Official Journal change (corrigendum, consolidated text, amending act) and not a converter artefact.',
              '- Re-run `python scripts/validate_repo.py` and the test suite; the catalogue counts are asserted against the published act.',
              '- Review `references/requirement-assessment-guide.json` for provisions whose wording changed.',
              '- Update `references/legal-status-and-dates.md` and the CHANGELOG. Merge only after a human confirms the generated baseline.', '']
    (ROOT / 'official' / 'UPSTREAM_CHANGE_REVIEW.md').write_text('\n'.join(lines), encoding='utf-8')

# ----------------------------------------------------------------------------- main

def load_manifest():
    return json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}


def rebuild_local():
    manifest = load_manifest()
    reg = (CURRENT / SOURCES['regulation']['local_file']).read_text(encoding='utf-8')
    ir_path = CURRENT / SOURCES['implementing_regulation_2025_2392']['local_file']
    ir = ir_path.read_text(encoding='utf-8') if ir_path.exists() else None
    stats = write_catalogues(reg, ir, manifest.get('sources', {}))
    return {'rebuilt_from': 'official/current', **stats}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--sync', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--rebuild-local', action='store_true')
    ap.add_argument('--summary-json', default='')
    args = ap.parse_args()

    def finish(summary, code=0):
        print(json.dumps(summary, indent=2))
        if args.summary_json:
            Path(args.summary_json).write_text(json.dumps(summary) + '\n', encoding='utf-8')
        return code

    if args.rebuild_local:
        return finish(rebuild_local())
    if not (args.sync or args.check):
        print('Use --sync, --check or --rebuild-local', file=sys.stderr); return 64

    old = load_manifest()
    fetched = {}; errors = {}
    for key, src in SOURCES.items():
        try:
            fetched[key] = fetch_cellar(src['celex'])
        except Exception as e:  # noqa: BLE001
            errors[key] = str(e)
            if src['required']:
                raise
    new_sources = {}
    for key, src in SOURCES.items():
        if key in fetched:
            b = fetched[key]
            new_sources[key] = {'celex': src['celex'], 'title': src['title'], 'eli': src['eli'], 'oj': src['oj'],
                                'cellar_url': f'http://publications.europa.eu/resource/celex/{src["celex"]}',
                                'local_file': src['local_file'], 'sha256': sha256(b), 'size': len(b),
                                'fetched_at_utc': datetime.now(timezone.utc).isoformat()}
        elif key in (old.get('sources') or {}):
            new_sources[key] = {**old['sources'][key], 'fetch_warning': errors.get(key)}
    changed = {k for k, v in new_sources.items() if (old.get('sources') or {}).get(k, {}).get('sha256') != v.get('sha256')}
    summary = {'changed': sorted(changed), 'fetch_errors': errors}
    if args.check:
        return finish(summary, 2 if changed else 0)

    CURRENT.mkdir(parents=True, exist_ok=True)
    for key, b in fetched.items():
        (CURRENT / SOURCES[key]['local_file']).write_bytes(b)
    new_manifest = {**{k: v for k, v in old.items() if k not in {'sources', 'last_checked_utc'}},
                    'last_checked_utc': datetime.now(timezone.utc).isoformat(), 'sources': new_sources}
    MANIFEST.write_text(json.dumps(new_manifest, indent=2) + '\n', encoding='utf-8')
    if changed:
        write_review(old, new_manifest)
    stats = rebuild_local()
    return finish({**summary, **stats})


if __name__ == '__main__':
    try:
        sys.exit(main() or 0)
    except Exception as e:  # noqa: BLE001
        print(f'ERROR: {type(e).__name__}: {e}', file=sys.stderr)
        sys.exit(1)
