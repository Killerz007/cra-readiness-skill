import csv, importlib.util, json, subprocess, sys, tempfile, unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def run(script, *args):
    return subprocess.run([sys.executable, str(ROOT / 'scripts' / script), *map(str, args)], capture_output=True, text=True)


class SbomTests(unittest.TestCase):
    def test_sample_sbom_passes(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / 'r.json'
            p = run('check_sbom.py', ROOT / 'examples/sample-sbom.cdx.json', '--output', out, '--markdown', Path(td) / 'r.md')
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            r = json.loads(out.read_text())
            self.assertIn(r['result'], ('PASS', 'PASS_WITH_WARNINGS')); self.assertEqual(r['top_level_dependency_count'], 4)

    def test_missing_versions_fail(self):
        d = json.loads((ROOT / 'examples/sample-sbom.cdx.json').read_text())
        del d['components'][0]['version']
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 's.json'; p.write_text(json.dumps(d))
            r = run('check_sbom.py', p)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)

    def test_lockfile_reconciliation_detects_missing(self):
        d = {"bomFormat": "CycloneDX", "specVersion": "1.5", "metadata": {"component": {"name": "app", "version": "1.0", "bom-ref": "app"}}, "components": [{"name": "left-pad", "version": "1.3.0", "purl": "pkg:npm/left-pad@1.3.0"}], "dependencies": [{"ref": "app", "dependsOn": ["pkg:npm/left-pad@1.3.0"]}]}
        with tempfile.TemporaryDirectory() as td:
            s = Path(td) / 's.json'; s.write_text(json.dumps(d))
            pk = Path(td) / 'package.json'; pk.write_text(json.dumps({"dependencies": {"left-pad": "^1.3.0", "express": "^4"}}))
            out = Path(td) / 'r.json'
            r = run('check_sbom.py', s, '--lockfile', pk, '--output', out)
            self.assertEqual(r.returncode, 2)
            self.assertEqual(json.loads(out.read_text())['lockfile_reconciliation']['missing_from_sbom'], ['express'])

    def test_spdx_parses(self):
        d = {"spdxVersion": "SPDX-2.3", "SPDXID": "SPDXRef-DOCUMENT", "name": "doc", "creationInfo": {"created": "2026-01-01T00:00:00Z", "creators": ["Tool: x-1.0"]}, "documentDescribes": ["SPDXRef-root"],
             "packages": [{"SPDXID": "SPDXRef-root", "name": "app", "versionInfo": "1.0"}, {"SPDXID": "SPDXRef-a", "name": "liba", "versionInfo": "2.0", "supplier": "Organization: A", "externalRefs": [{"referenceCategory": "PACKAGE-MANAGER", "referenceType": "purl", "referenceLocator": "pkg:generic/liba@2.0"}]}],
             "relationships": [{"spdxElementId": "SPDXRef-root", "relationshipType": "DEPENDS_ON", "relatedSpdxElement": "SPDXRef-a"}]}
        with tempfile.TemporaryDirectory() as td:
            s = Path(td) / 's.spdx.json'; s.write_text(json.dumps(d)); out = Path(td) / 'r.json'
            r = run('check_sbom.py', s, '--output', out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(json.loads(out.read_text())['format'], 'SPDX')


class DeadlineTests(unittest.TestCase):
    def test_vulnerability_deadlines(self):
        m = load('reporting_deadlines')
        a = datetime(2026, 10, 6, 14, 30, tzinfo=timezone.utc)
        d = m.compute('vulnerability', a, datetime(2026, 10, 9, 10, 0, tzinfo=timezone.utc), None)
        self.assertEqual(d['early_warning_due'], '2026-10-07T14:30:00+00:00')
        self.assertEqual(d['notification_due'], '2026-10-09T14:30:00+00:00')
        self.assertEqual(d['final_report_due'], '2026-10-23T10:00:00+00:00')

    def test_incident_one_month_and_month_end(self):
        m = load('reporting_deadlines')
        d = m.compute('incident', datetime(2026, 1, 29, 9, 0, tzinfo=timezone.utc), None, datetime(2026, 1, 31, 9, 0, tzinfo=timezone.utc))
        self.assertEqual(d['final_report_due'], '2026-02-28T09:00:00+00:00')

    def test_naive_timestamp_rejected(self):
        m = load('reporting_deadlines')
        with self.assertRaises(ValueError):
            m.parse('2026-10-06T14:30:00')


class SupportPeriodTests(unittest.TestCase):
    def test_five_year_floor(self):
        m = load('support_period_check')
        from datetime import date
        r = m.check(date(2028, 1, 15), date(2031, 1, 15), 7, None, [])
        self.assertEqual(r['result'], 'FAIL')
        r = m.check(date(2028, 1, 15), date(2033, 1, 15), 7, None, [date(2028, 6, 1)])
        self.assertEqual(r['result'], 'PASS_WITH_WARNINGS')  # shorter than expected use
        self.assertEqual(r['computed_dates']['documentation_retained_until'], '2038-01-15')
        self.assertEqual(r['computed_dates']['update_1_issued_2028-06-01_available_until'], '2038-06-01')
        r = m.check(date(2028, 1, 15), date(2030, 1, 15), 2, 'subscription-only software', [])
        self.assertEqual(r['result'], 'PASS')


class RegressionAndTicketTests(unittest.TestCase):
    SAMPLE = ROOT / 'examples/sample-assessment'

    def test_sample_compares_cleanly_with_itself(self):
        with tempfile.TemporaryDirectory() as td:
            p = run('compare_assessments.py', '--baseline', self.SAMPLE, '--current', self.SAMPLE, '--output', td)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertEqual(json.loads((Path(td) / 'regression-summary.json').read_text())['result'], 'PASS')

    def test_conformant_to_gap_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            cur = Path(td) / 'current'; cur.mkdir()
            with (self.SAMPLE / '07-requirement-matrix.csv').open(newline='', encoding='utf-8') as f:
                rows = list(csv.DictReader(f))
            rows[0]['status'] = 'GAP'
            with (cur / '07-requirement-matrix.csv').open('w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
            (cur / '11-gaps-register.jsonl').write_text((self.SAMPLE / '11-gaps-register.jsonl').read_text())
            out = Path(td) / 'out'
            p = run('compare_assessments.py', '--baseline', self.SAMPLE, '--current', cur, '--output', out)
            self.assertEqual(p.returncode, 2)
            self.assertEqual(json.loads((out / 'regression-summary.json').read_text())['blocking_regressions'][0]['provision_id'], rows[0]['provision_id'])

    def test_ticket_queue(self):
        with tempfile.TemporaryDirectory() as td:
            p = run('export_ticket_queue.py', '--assessment-dir', self.SAMPLE, '--output', td)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            q = json.loads((Path(td) / '22-finding-ticket-queue.json').read_text())
            self.assertFalse(q['ticket_creation_authorized']); self.assertEqual([t['gap_id'] for t in q['tickets']], ['CRA-G-001', 'CRA-G-002'])

    def test_init_assessment(self):
        with tempfile.TemporaryDirectory() as td:
            p = run('init_assessment.py', '--product', 'Test Product', '--version', '1.0', '--output-root', td)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            out = Path(p.stdout.strip())
            m = json.loads((out / '00-assessment-manifest.json').read_text())
            self.assertEqual(m['product_name'], 'Test Product'); self.assertTrue((out / '07-requirement-matrix.csv').exists())


if __name__ == '__main__':
    unittest.main()
