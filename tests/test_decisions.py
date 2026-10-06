import importlib.util, json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


classify = load('classify_product'); screen = load('screen_substantial_modification')
EX = json.loads((ROOT / 'examples/scope-answers.example.json').read_text(encoding='utf-8'))
CL = json.loads((ROOT / 'examples/classification-answers.example.json').read_text(encoding='utf-8'))


class ScopeTests(unittest.TestCase):
    def test_example_is_in_scope_with_rdps(self):
        d = classify.scope_decision(EX)
        self.assertEqual(d['decision'], 'in_scope')
        self.assertEqual(d['product_boundary']['remote_data_processing_solutions'], ['Example Cloud device management backend'])
        self.assertEqual(d['product_boundary']['third_party_components_outside_boundary'], ['Third-party SaaS analytics'])
        self.assertEqual(d['date_regime'], 'not_yet_placed')

    def test_web_application_is_out_of_scope(self):
        d = classify.scope_decision({**EX, 'product_kind': 'software', 'software_operated_on_user_side': False, 'remote_components': []})
        self.assertEqual(d['decision'], 'out_of_scope')

    def test_exclusion(self):
        d = classify.scope_decision({**EX, 'exclusion': 'medical_device_2017_745', 'remote_components': []})
        self.assertEqual(d['decision'], 'out_of_scope')
        self.assertIn('2017/745', d['questions'][3]['answer'])

    def test_pre_2027_product_reporting_only(self):
        d = classify.scope_decision({**EX, 'placed_on_market_date': '2026-05-01', 'substantially_modified_from_2027_12_11': False, 'remote_components': []})
        self.assertEqual(d['decision'], 'in_scope_article_14_only')
        self.assertEqual(d['date_regime'], 'placed_before_2027-12-11_not_modified')

    def test_pre_2027_substantially_modified(self):
        d = classify.scope_decision({**EX, 'placed_on_market_date': '2026-05-01', 'substantially_modified_from_2027_12_11': True, 'remote_components': []})
        self.assertEqual(d['decision'], 'in_scope')
        self.assertEqual(d['date_regime'], 'placed_before_2027-12-11_substantially_modified')

    def test_foss_steward(self):
        d = classify.scope_decision({**EX, 'commercial_model': 'free_non_commercial', 'is_foss': True, 'is_legal_person': True, 'provides_sustained_support': True, 'remote_components': []})
        self.assertEqual(d['economic_operator_role'], 'open_source_steward')
        self.assertTrue(d['legal_confirmation_recommended'])

    def test_foss_non_commercial_natural_person_out_of_scope(self):
        d = classify.scope_decision({**EX, 'commercial_model': 'donations_unconditional', 'is_foss': True, 'is_legal_person': False, 'remote_components': []})
        self.assertEqual(d['decision'], 'out_of_scope')


class ClassificationTests(unittest.TestCase):
    def test_example_default(self):
        d = classify.classification_decision(CL)
        self.assertEqual(d['class'], 'default')
        self.assertIn('module_A', d['available_routes'])

    def test_class_i_without_standards_has_no_module_a(self):
        d = classify.classification_decision({**CL, 'category_matches': [{'category_ref': 'AIII.I.11', 'relationship': 'matches_core_functionality', 'reasoning': 'OS'}]})
        self.assertEqual(d['class'], 'important_class_I')
        self.assertNotIn('module_A', d['available_routes'])
        self.assertIn('module_B_plus_C', d['available_routes'])

    def test_class_i_with_cited_standards_has_module_a(self):
        d = classify.classification_decision({**CL, 'harmonised_standards_cited_and_applied_in_full': True, 'category_matches': [{'category_ref': 'AIII.I.3', 'relationship': 'matches_core_functionality', 'reasoning': 'password manager'}]})
        self.assertIn('module_A', d['available_routes'])

    def test_foss_class_ii_article_32_5(self):
        d = classify.classification_decision({**CL, 'foss_product_with_public_technical_documentation': True, 'category_matches': [{'category_ref': 'AIII.II.1', 'relationship': 'matches_core_functionality', 'reasoning': 'hypervisor'}]})
        self.assertEqual(d['class'], 'important_class_II'); self.assertIn('module_A', d['available_routes'])

    def test_critical_without_delegated_act(self):
        d = classify.classification_decision({**CL, 'category_matches': [{'category_ref': 'AIV.3', 'relationship': 'matches_core_functionality', 'reasoning': 'secure element'}]})
        self.assertEqual(d['class'], 'critical'); self.assertEqual(d['available_routes'][0], 'module_B_plus_C')

    def test_integration_does_not_classify(self):
        d = classify.classification_decision({**CL, 'category_matches': [{'category_ref': 'AIII.I.11', 'relationship': 'integrated_or_ancillary_only', 'reasoning': 'embeds an OS'}]})
        self.assertEqual(d['class'], 'default')

    def test_unknown_category_rejected(self):
        with self.assertRaises(SystemExit):
            classify.classification_decision({**CL, 'category_matches': [{'category_ref': 'AIII.I.99', 'relationship': 'matches_core_functionality'}]})


class ScreeningTests(unittest.TestCase):
    def test_example_is_substantial(self):
        d = screen.screen(json.loads((ROOT / 'examples/substantial-modification-answers.example.json').read_text(encoding='utf-8')))
        self.assertEqual(d['conclusion'], 'substantial'); self.assertIn('A13.2', d['provisions_requiring_reassessment']); self.assertIn('AI.P1.2j', d['provisions_requiring_reassessment'])

    def test_security_fix_not_substantial(self):
        no = {'answer': 'no', 'reasoning': 'n'}
        d = screen.screen({'change_set': {}, 'security_update_only': True, 'changes_intended_purpose': False, 'answers': {'new_threat_vectors': no, 'new_attack_scenarios': no, 'changed_likelihood': no, 'changed_impact': no}, 'risk_assessment_assumptions_still_valid': True})
        self.assertEqual(d['conclusion'], 'not_substantial'); self.assertEqual(d['confidence'], 'High')

    def test_unknown_is_undetermined(self):
        no = {'answer': 'no', 'reasoning': 'n'}
        d = screen.screen({'change_set': {}, 'answers': {'new_threat_vectors': {'answer': 'unknown', 'reasoning': ''}, 'new_attack_scenarios': no, 'changed_likelihood': no, 'changed_impact': no}, 'risk_assessment_assumptions_still_valid': True})
        self.assertEqual(d['conclusion'], 'undetermined_pending_risk_assessment_update')


if __name__ == '__main__':
    unittest.main()
