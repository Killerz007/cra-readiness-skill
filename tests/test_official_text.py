import hashlib, importlib.util, json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sync', ROOT / 'scripts/sync_official_text.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


class PinnedTextTests(unittest.TestCase):
    """The parser is run against the pinned Official Journal text on every test run."""

    @classmethod
    def setUpClass(cls):
        cls.reg = (ROOT / 'official/current/CRA-2024-2847.xhtml').read_text(encoding='utf-8')
        cls.ir = (ROOT / 'official/current/IR-2025-2392.xhtml').read_text(encoding='utf-8')
        cls.manifest = json.loads((ROOT / 'official/upstream-manifest.json').read_text(encoding='utf-8'))

    def test_manifest_hashes_match_pinned_files(self):
        for key, src in self.manifest['sources'].items():
            p = ROOT / 'official/current' / src['local_file']
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), src['sha256'], key)

    def test_article_count_and_titles(self):
        arts = mod.parse_articles(self.reg)
        self.assertEqual(len(arts), 71)
        self.assertEqual(arts[13]['title'], 'Obligations of manufacturers')
        self.assertEqual(arts[14]['title'], 'Reporting obligations of manufacturers')
        self.assertEqual(arts[71]['title'], 'Entry into force and application')
        self.assertIn('11 December 2027', arts[71]['paragraphs'][2]['text'])
        self.assertIn('11 September 2026', arts[71]['paragraphs'][2]['text'])

    def test_requirement_catalogue_counts(self):
        _, reqs, cats = mod.build_requirements(self.reg)
        ids = [r['id'] for r in reqs]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(sum(1 for i in ids if i.startswith('AI.P1.')), 15)
        self.assertEqual(sum(1 for i in ids if i.startswith('AI.P2.')), 8)
        self.assertEqual([i for i in ids if i.startswith('AI.P1.2') and len(i) == 8], ['AI.P1.2' + c for c in 'abcdefghijklm'])
        self.assertEqual(len(cats['important_class_I']), 19); self.assertEqual(len(cats['important_class_II']), 4); self.assertEqual(len(cats['critical']), 3)

    def test_key_wording_extracted_verbatim(self):
        _, reqs, _ = mod.build_requirements(self.reg)
        by = {r['id']: r for r in reqs}
        self.assertIn('software bill of materials in a commonly used and machine-readable format covering at the very least the top-level dependencies', by['AI.P2.1']['text'])
        self.assertIn('secure by default configuration', by['AI.P1.2b']['text'])
        self.assertIn('within 24 hours', by['A14.2']['points'][0]['text'])
        self.assertIn('at least five years', by['A13.8']['text'])
        self.assertIn('minimum of 10 years', by['A13.9']['text'])

    def test_technical_descriptions(self):
        td = mod.parse_technical_descriptions(self.ir)
        self.assertEqual(td['important_class_I'][10]['category'], 'Operating systems')
        self.assertIn('AVA_VAN', td['critical'][2]['technical_description'])
        self.assertTrue(all(x['technical_description'] for v in td.values() for x in v))

    def test_generated_files_are_current(self):
        _, reqs, cats = mod.build_requirements(self.reg)
        gen = json.loads((ROOT / 'references/cra-requirements-catalog.generated.json').read_text(encoding='utf-8'))
        self.assertEqual(gen['requirements'], reqs, 'generated catalogue is stale; run scripts/sync_official_text.py --rebuild-local')
        self.assertEqual(gen['pinned_sha256'], self.manifest['sources']['regulation']['sha256'])
        pc = json.loads((ROOT / 'references/cra-product-categories.generated.json').read_text(encoding='utf-8'))
        self.assertEqual(pc['annex_iii_iv_categories'], cats)
        self.assertEqual(pc['technical_descriptions'], mod.parse_technical_descriptions(self.ir))

    def test_guide_covers_every_provision(self):
        gen = json.loads((ROOT / 'references/cra-requirements-catalog.generated.json').read_text(encoding='utf-8'))
        guide = json.loads((ROOT / 'references/requirement-assessment-guide.json').read_text(encoding='utf-8'))['entries']
        self.assertEqual(set(guide), {r['id'] for r in gen['requirements']})


if __name__ == '__main__':
    unittest.main()
