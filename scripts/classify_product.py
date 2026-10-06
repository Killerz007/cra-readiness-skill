#!/usr/bin/env python3
"""Turn structured answers into a CRA scope decision or classification decision.

The logic encodes the text of Regulation (EU) 2024/2847 and the Commission's non-binding
guidance C(2026) 5252. It is a decision aid: every output carries a confidence level and a
``legal_confirmation_recommended`` flag, and borderline inputs always set that flag.

Usage:
  python scripts/classify_product.py --answers answers.json --stage scope    --output <dir>
  python scripts/classify_product.py --answers answers.json --stage classify --output <dir>

See examples/scope-answers.example.json and examples/classification-answers.example.json
for the expected input shape; schemas/scope-decision.schema.json and
schemas/classification-decision.schema.json describe the outputs.
"""
import argparse, json, sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERAL_APPLICATION = date(2027, 12, 11)
EXCLUSIONS = {
    'none': None,
    'medical_device_2017_745': 'Article 2(2)(a): Regulation (EU) 2017/745 applies',
    'ivd_2017_746': 'Article 2(2)(b): Regulation (EU) 2017/746 applies',
    'vehicle_2019_2144': 'Article 2(2)(c): Regulation (EU) 2019/2144 applies',
    'aviation_2018_1139_certified': 'Article 2(3): product certified under Regulation (EU) 2018/1139',
    'marine_2014_90': 'Article 2(4): Directive 2014/90/EU applies',
    'spare_part_identical': 'Article 2(6): spare part replacing an identical component to the same specifications',
    'national_security_defence': 'Article 2(7): developed or modified exclusively for national security or defence, or designed to process classified information',
}
COMMERCIAL = {
    'price': ('commercial', 'A price is charged for the product (guidance 3.2.1).'),
    'monetises_other_products_or_services': ('commercial', 'The product monetises other products or services through it (guidance 3.2.2).'),
    'personal_data_processing_condition': ('commercial', 'Use is conditional on processing personal data for purposes other than security, compatibility or interoperability (guidance 3.2.2).'),
    'paid_access_updates_or_support_conditioned': ('commercial', 'Access to the product, binaries, updates or fixes is conditioned on payment or de facto payment (guidance 3.2.3, 3.2.4).'),
    'internal_use_only': ('not_commercial', 'Manufactured for own use; not placed on the market (Blue Guide 2.3; FAQ).'),
    'free_non_commercial': ('not_commercial', 'Supplied free of charge without monetisation; not a commercial activity (Recital 18; guidance 3.2).'),
    'donations_unconditional': ('not_commercial', 'Voluntary unconditional donations are not a commercial activity (Recital 15; guidance 3.2.4).'),
    'not_for_profit_entity': ('not_commercial', 'Not-for-profit entity using all earnings after costs for not-for-profit objectives (Recital 18; guidance 3.2.6).'),
    'unknown': ('unknown', 'Commercial model not established.'),
}


def now():
    return datetime.now(timezone.utc).isoformat()


def load_categories():
    path = ROOT / 'references' / 'cra-product-categories.generated.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    lookup = {}
    for n in data['annex_iii_iv_categories']['important_class_I']:
        lookup[f'AIII.I.{n["number"]}'] = ('important_class_I', n['category'], 'III')
    for n in data['annex_iii_iv_categories']['important_class_II']:
        lookup[f'AIII.II.{n["number"]}'] = ('important_class_II', n['category'], 'III')
    for n in data['annex_iii_iv_categories']['critical']:
        lookup[f'AIV.{n["number"]}'] = ('critical', n['category'], 'IV')
    return lookup

# ----------------------------------------------------------------------------- scope

def scope_decision(a: dict) -> dict:
    qs = []; reasons_legal = []; conf = 'High'

    def q(qid, question, answer, basis, c='High'):
        nonlocal conf
        qs.append({'id': qid, 'question': question, 'answer': answer, 'basis': basis, 'confidence': c})
        if c == 'Low' or (c == 'Medium' and conf == 'High'):
            conf = c

    decision = 'in_scope'
    role = a.get('economic_operator_role', 'undetermined')

    # Q1 product with digital elements
    kind = a.get('product_kind', 'unknown')  # software | hardware | hardware_with_software | combination | remote_service_only
    operated_user_side = a.get('software_operated_on_user_side')
    if kind == 'remote_service_only' or (kind == 'software' and operated_user_side is False):
        q('Q1', 'Is it a product with digital elements?', 'No: software that executes remotely and is merely accessed by the user is not, on that basis, a product with digital elements.', 'Article 3(1); guidance points 20 to 21')
        decision = 'out_of_scope'
    elif kind in ('software', 'hardware', 'hardware_with_software', 'combination'):
        q('Q1', 'Is it a product with digital elements?', f'Yes ({kind}).', 'Article 3(1); guidance point 18')
    else:
        q('Q1', 'Is it a product with digital elements?', 'Undetermined.', 'Article 3(1)', 'Low'); decision = 'undetermined'
    if a.get('has_data_connection') is False:
        q('Q1b', 'Direct or indirect logical or physical data connection?', 'No; outside Article 2(1).', 'Article 2(1)')
        if decision == 'in_scope':
            decision = 'out_of_scope'
    else:
        q('Q1b', 'Direct or indirect logical or physical data connection?', 'Yes.' if a.get('has_data_connection') else 'Assumed yes (not answered).', 'Article 2(1)', 'High' if a.get('has_data_connection') else 'Medium')

    # Q2 commercial activity
    model = a.get('commercial_model', 'unknown')
    kind_c, basis_c = COMMERCIAL.get(model, COMMERCIAL['unknown'])
    foss = bool(a.get('is_foss'))
    if kind_c == 'commercial':
        q('Q2', 'Made available on the EU market in the course of a commercial activity?', f'Yes. {basis_c}', 'Article 3(21), (22)')
    elif kind_c == 'not_commercial':
        q('Q2', 'Made available on the EU market in the course of a commercial activity?', f'No. {basis_c}', 'Article 3(22); Recital 18')
        if foss and a.get('is_legal_person') and a.get('provides_sustained_support'):
            role = 'open_source_steward'
            q('Q2b', 'Open-source software steward?', 'Yes: legal person systematically providing sustained support for FOSS intended for commercial activities. Article 24 obligations apply from 11 December 2027; Article 14 to the extent of Article 24(3).', 'Article 3(14), Article 24; guidance 3.3', 'Medium')
            reasons_legal.append('Steward status depends on facts about sustained support and commercial intent.')
        elif decision == 'in_scope':
            decision = 'out_of_scope'
    else:
        q('Q2', 'Made available on the EU market in the course of a commercial activity?', 'Undetermined.', 'Article 3(22)', 'Low')
        if decision == 'in_scope':
            decision = 'undetermined'
    if model in ('monetises_other_products_or_services', 'personal_data_processing_condition', 'paid_access_updates_or_support_conditioned', 'donations_unconditional', 'not_for_profit_entity') or foss:
        reasons_legal.append('Commercial-activity test for free or open-source software rests on the Commission\'s non-binding guidance; confirm with counsel.')
    if a.get('made_available_in_eu') is False:
        q('Q2c', 'Made available in the EU?', 'No; the CRA applies to the Union market only.', 'Article 2(1)')
        if decision == 'in_scope':
            decision = 'out_of_scope'

    # Q3 exclusions
    exc = a.get('exclusion', 'none')
    if exc not in EXCLUSIONS:
        q('Q3', 'Does an exclusion apply?', f'Unknown exclusion code {exc!r}.', 'Article 2', 'Low')
    elif EXCLUSIONS[exc]:
        q('Q3', 'Does an exclusion apply?', f'Yes. {EXCLUSIONS[exc]}', 'Article 2')
        if decision == 'in_scope':
            decision = 'out_of_scope'
    else:
        q('Q3', 'Does an exclusion apply?', 'No exclusion identified.', 'Article 2(2) to (7)')
    if a.get('exclusion_borderline'):
        reasons_legal.append('Product is near an Article 2 exclusion boundary.'); conf = 'Medium' if conf == 'High' else conf

    # Q4 remote data processing
    rdps = []; third_party = []
    for rc in a.get('remote_components', []):
        tests = (bool(rc.get('at_a_distance')), bool(rc.get('absence_prevents_function')), bool(rc.get('developed_by_or_for_manufacturer')))
        if all(tests):
            rdps.append(rc['name'])
        elif rc.get('affects_product_security'):
            third_party.append(rc['name'])
    q('Q4', 'Remote data processing solutions inside the product boundary?', f'{len(rdps)} qualifying: {rdps}; treated as third-party components: {third_party}.', 'Article 3(1), (2); guidance section 8', 'High' if not a.get('remote_components') else 'Medium')
    if rdps or third_party:
        reasons_legal.append('Remote data processing boundary decisions are fact-sensitive.')

    # Q5 date regime
    placed = a.get('placed_on_market_date')
    if placed:
        try:
            pd = date.fromisoformat(placed)
        except ValueError:
            pd = None
        if pd and pd < GENERAL_APPLICATION:
            if a.get('substantially_modified_from_2027_12_11'):
                regime = 'placed_before_2027-12-11_substantially_modified'
                q('Q5', 'Date regime?', 'Placed on the market before 11 December 2027 and substantially modified from that date: full obligations apply to the modified product.', 'Article 69(2)')
            else:
                regime = 'placed_before_2027-12-11_not_modified'
                q('Q5', 'Date regime?', 'Placed on the market before 11 December 2027 and not substantially modified: Article 14 reporting applies; other obligations do not unless substantially modified.', 'Article 69(2), (3)')
                if decision == 'in_scope':
                    decision = 'in_scope_article_14_only'
        else:
            regime = 'placed_on_or_after_2027-12-11' if pd else 'undetermined'
            q('Q5', 'Date regime?', 'Placed on or after 11 December 2027: all obligations apply (Article 14 since 11 September 2026).', 'Article 71(2)')
    else:
        regime = 'not_yet_placed'
        q('Q5', 'Date regime?', 'Not yet placed on the market: all obligations will apply at placing on the market; Article 14 applies once the product is in scope.', 'Article 71(2); Article 69')

    # Q6 separately supplied components
    sep = a.get('separately_supplied_components', [])
    q('Q6', 'Components placed on the market separately?', f'{sep}' if sep else 'None identified.', 'Article 3(1); guidance point 145')

    if a.get('user_disputes_outcome'):
        reasons_legal.append('The user disagrees with the assessed outcome.')
    if decision == 'undetermined':
        reasons_legal.append('Scope could not be determined from the facts provided.')
    legal = bool(reasons_legal) or conf == 'Low'
    return {
        'decision': decision, 'economic_operator_role': role,
        'product_boundary': {'product': a.get('product_name', ''), 'remote_data_processing_solutions': rdps, 'third_party_components_outside_boundary': third_party, 'separately_supplied_components': sep},
        'date_regime': regime, 'confidence': conf, 'legal_confirmation_recommended': legal, 'reasons_for_legal_confirmation': reasons_legal,
        'questions': qs, 'adjudication_ids': [], 'decided_at_utc': now(),
    }


def scope_markdown(d: dict) -> str:
    lines = ['# Scope determination', '', f"**Decision:** {d['decision']}  ", f"**Economic operator role:** {d['economic_operator_role']}  ", f"**Date regime:** {d['date_regime']}  ",
             f"**Confidence:** {d['confidence']} | **Legal confirmation recommended:** {'yes' if d['legal_confirmation_recommended'] else 'no'}", '']
    if d['reasons_for_legal_confirmation']:
        lines += ['Reasons for legal confirmation:', ''] + [f'- {r}' for r in d['reasons_for_legal_confirmation']] + ['']
    lines += ['| # | Question | Answer | Basis | Confidence |', '|---|---|---|---|---|']
    for q in d['questions']:
        lines.append(f"| {q['id']} | {q['question']} | {q['answer']} | {q['basis']} | {q['confidence']} |")
    b = d['product_boundary']
    lines += ['', '## Product boundary', '', f"- Remote data processing solutions: {b['remote_data_processing_solutions'] or 'none'}", f"- Third-party components outside the boundary: {b['third_party_components_outside_boundary'] or 'none'}", f"- Separately supplied components: {b['separately_supplied_components'] or 'none'}", '',
              '> Technical assessment of the facts against Regulation (EU) 2024/2847 and the Commission\'s non-binding guidance C(2026) 5252. Not legal advice.', '']
    return '\n'.join(lines)

# ----------------------------------------------------------------------------- classification

CLASS_ORDER = ['default', 'important_class_I', 'important_class_II', 'critical']


def classification_decision(a: dict) -> dict:
    lookup = load_categories()
    considered = []; matched = None; cls = 'default'
    for m in a.get('category_matches', []):
        ref = m.get('category_ref'); rel = m.get('relationship', 'no_overlap')
        if ref not in lookup:
            raise SystemExit(f'unknown category_ref {ref!r}; use AIII.I.<n>, AIII.II.<n> or AIV.<n>')
        c, name, annex = lookup[ref]
        considered.append({'category': name, 'category_ref': ref, 'relationship': rel, 'reasoning': m.get('reasoning', '')})
        if rel == 'matches_core_functionality' and CLASS_ORDER.index(c) > CLASS_ORDER.index(cls):
            cls = c; matched = {'annex': annex, 'class': c, 'number': int(ref.split('.')[-1]), 'category': name}
    modules = []
    for mod in a.get('modules_sold_separately', []):
        ref = mod.get('category_ref')
        modules.append({'module': mod.get('module'), 'class': lookup[ref][0] if ref in lookup else 'default'})

    hs = bool(a.get('harmonised_standards_cited_and_applied_in_full'))
    scheme = bool(a.get('certification_scheme_available_substantial'))
    da8 = bool(a.get('article_8_delegated_act_requires_certification'))
    foss_public = bool(a.get('foss_product_with_public_technical_documentation'))
    notes = []
    if cls == 'default':
        routes = ['module_A', 'module_B_plus_C', 'module_H'] + (['european_certification_scheme'] if scheme else [])
        notes.append('Default category: any Article 32(1) procedure.')
    elif cls == 'important_class_I':
        routes = ['module_B_plus_C', 'module_H'] + (['european_certification_scheme'] if scheme else [])
        if hs or foss_public:
            routes = ['module_A'] + routes
            notes.append('Module A available because harmonised standards, common specifications or a scheme are applied in full (Article 32(2))' if hs else 'Module A available under Article 32(5): free and open-source product with public technical documentation.')
        else:
            notes.append('Module A NOT available: no cited harmonised standard, common specification or applicable scheme applied in full (Article 32(2)).')
    elif cls == 'important_class_II':
        routes = ['module_B_plus_C', 'module_H'] + (['european_certification_scheme'] if scheme else [])
        if foss_public:
            routes = ['module_A'] + routes; notes.append('Article 32(5): FOSS product with public technical documentation may use any Article 32(1) procedure.')
        notes.append('Class II: third-party assessment or certification scheme at least "substantial" (Article 32(3)).')
    else:
        routes = (['european_certification_scheme'] if da8 else []) + ['module_B_plus_C', 'module_H'] + (['european_certification_scheme'] if scheme and not da8 else [])
        notes.append('Critical: certification scheme where an Article 8(1) delegated act requires it; otherwise the class II procedures (Article 32(4)).' + (' An Article 8(1) delegated act is reported as applicable.' if da8 else ' No Article 8(1) delegated act reported.'))
    conf = a.get('confidence', 'Medium')
    legal = bool(a.get('borderline') or a.get('user_disputes_outcome') or any(c['relationship'] in ('substantially_exceeds', 'substantially_falls_short') for c in considered) or modules)
    return {
        'core_functionality': a.get('core_functionality', ''), 'class': cls, 'matched_category': matched, 'categories_considered': considered,
        'modules_classified_separately': modules, 'available_routes': routes, 'route_notes': ' '.join(notes), 'harmonised_standards_cited': hs,
        'foss_article_32_5': foss_public, 'confidence': conf, 'legal_confirmation_recommended': legal,
        'strongest_counter_argument': a.get('strongest_counter_argument', ''), 'adjudication_ids': [], 'decided_at_utc': now(),
    }


def classification_markdown(d: dict) -> str:
    lines = ['# Classification and conformity assessment route', '', f"**Core functionality:** {d['core_functionality']}  ", f"**Class:** {d['class']}  ",
             f"**Matched category:** {d['matched_category']['category'] if d['matched_category'] else 'none (default category)'}  ",
             f"**Available routes (Article 32):** {', '.join(d['available_routes'])}  ", f"**Route notes:** {d['route_notes']}  ",
             f"**Confidence:** {d['confidence']} | **Legal confirmation recommended:** {'yes' if d['legal_confirmation_recommended'] else 'no'}", '',
             '| Category considered | Relationship to core functionality | Reasoning |', '|---|---|---|']
    for c in d['categories_considered']:
        lines.append(f"| {c['category']} ({c['category_ref']}) | {c['relationship']} | {c['reasoning']} |")
    if d['modules_classified_separately']:
        lines += ['', '## Modules sold separately', ''] + [f"- {m['module']}: {m['class']}" for m in d['modules_classified_separately']]
    if d['strongest_counter_argument']:
        lines += ['', f"**Strongest counter-argument:** {d['strongest_counter_argument']}"]
    lines += ['', '> Classification follows Article 7, Article 8, Annex III and IV of Regulation (EU) 2024/2847 and the technical descriptions in Implementing Regulation (EU) 2025/2392, read with the Commission\'s non-binding guidance C(2026) 5252 section 6. Not legal advice.', '']
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--answers', required=True); ap.add_argument('--stage', choices=['scope', 'classify'], required=True); ap.add_argument('--output', default='.')
    args = ap.parse_args()
    a = json.loads(Path(args.answers).read_text(encoding='utf-8'))
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    if args.stage == 'scope':
        d = scope_decision(a)
        (out / '02-scope-decision.json').write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
        (out / '02-scope-determination.md').write_text(scope_markdown(d), encoding='utf-8')
        print(json.dumps({'decision': d['decision'], 'role': d['economic_operator_role'], 'date_regime': d['date_regime'], 'confidence': d['confidence'], 'legal_confirmation_recommended': d['legal_confirmation_recommended']}))
    else:
        d = classification_decision(a)
        (out / '03-classification-decision.json').write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
        (out / '03-classification-and-route.md').write_text(classification_markdown(d), encoding='utf-8')
        print(json.dumps({'class': d['class'], 'routes': d['available_routes'], 'confidence': d['confidence'], 'legal_confirmation_recommended': d['legal_confirmation_recommended']}))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f'ERROR: {type(e).__name__}: {e}', file=sys.stderr); sys.exit(1)
