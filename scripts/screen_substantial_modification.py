#!/usr/bin/env python3
"""Screen a change set for substantial modification (Article 3(30); guidance C(2026) 5252 section 4.3).

Input: a JSON file with the change description and the four-factor answers:
{
  "change_set": {"description": "...", "from_version": "1.2.0", "to_version": "1.3.0", "commits_or_release_notes": ["..."]},
  "security_update_only": false,
  "changes_intended_purpose": false,
  "answers": {
    "new_threat_vectors":  {"answer": "yes|no|unknown", "reasoning": "...", "evidence_ids": []},
    "new_attack_scenarios": {...}, "changed_likelihood": {...}, "changed_impact": {...}
  },
  "risk_assessment_assumptions_still_valid": true
}
Output: 25-substantial-modification-screening.json and .md in --output.
"""
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

QUESTIONS = {
    'new_threat_vectors': ('a. Does the update introduce new threat vectors (interfaces, communication channels, execution environments, external dependencies)?', ['AI.P1.2j', 'AI.P1.2d', 'AI.P1.2e', 'AI.P1.2f', 'AI.P1.2h', 'AI.P1.2i', 'A13.5']),
    'new_attack_scenarios': ('b. Does it enable new attack scenarios (unauthorised access, manipulation, interference, misuse)?', ['AI.P1.2a', 'AI.P1.2d', 'AI.P1.2k', 'AI.P1.2l']),
    'changed_likelihood': ('c. Does it change the likelihood of previously identified attack scenarios (lower effort, more exposure, weaker safeguards)?', ['AI.P1.2b', 'AI.P1.2c', 'AI.P1.2k']),
    'changed_impact': ('d. Does it change the potential impact of previously identified scenarios (scope of data or functions, severity, detect, contain, recover)?', ['AI.P1.2g', 'AI.P1.2h', 'AI.P1.2l', 'AI.P1.2m']),
}
ALWAYS = ['A13.2', 'A13.3', 'A13.4', 'AVII.3']


def screen(a: dict) -> dict:
    answers = a['answers']
    yes = [k for k, v in answers.items() if v.get('answer') == 'yes']
    unknown = [k for k, v in answers.items() if v.get('answer') == 'unknown']
    assumptions = a.get('risk_assessment_assumptions_still_valid')
    purpose = bool(a.get('changes_intended_purpose'))
    sec_only = bool(a.get('security_update_only'))
    consequences = []
    if purpose:
        conclusion = 'substantial'; conf = 'High'
        consequences.append('Change to the intended purpose: substantial modification (Article 3(30); guidance point 105).')
    elif yes:
        conclusion = 'substantial'; conf = 'Medium' if len(yes) == 1 else 'High'
        consequences.append(f'Affirmative four-factor answers ({", ".join(yes)}): new or increased cybersecurity risk not covered by the risk assessment (guidance points 107, 109, 110).')
        if sec_only:
            consequences.append('Security update that nonetheless introduces new risks or dependencies is not covered by the security-update carve-out (guidance point 109, examples 49 and 50).')
    elif unknown or assumptions is None:
        conclusion = 'undetermined_pending_risk_assessment_update'; conf = 'Low'
        consequences.append('One or more answers unknown, or validity of risk-assessment assumptions not confirmed: update the risk assessment before concluding (guidance points 104, 111).')
    elif assumptions is False:
        conclusion = 'substantial'; conf = 'Medium'
        consequences.append('Risk-assessment assumptions or mitigations no longer valid (guidance point 111).')
    else:
        conclusion = 'not_substantial'; conf = 'High' if sec_only else 'Medium'
        consequences.append('No new threat vectors, attack scenarios, likelihood or impact changes; assumptions remain valid: likely not a substantial modification (guidance point 111).' + (' Security update within the carve-out (guidance point 108).' if sec_only else ''))
    if conclusion == 'substantial':
        consequences += ['The modified product is treated as a new product: new placing on the market, new conformity assessment, updated technical documentation and declaration (guidance section 4.4).',
                         'Declare a support period for the modified version after reassessing the Article 13(8) criteria (guidance section 5.1).',
                         'If the modifier is not the original manufacturer, it becomes the manufacturer for the affected part or the whole product (Articles 21 and 22).',
                         'For a product first placed on the market before 11 December 2027 this brings it into the full regime (Article 69(2)).']
    provisions = sorted(set(ALWAYS + [p for k in yes for p in QUESTIONS[k][1]]))
    legal = conclusion != 'not_substantial' or purpose or bool(a.get('touches_product_boundary'))
    return {
        'change_set': a.get('change_set', {}), 'security_update_only': sec_only, 'changes_intended_purpose': purpose,
        'answers': {k: {'question': QUESTIONS[k][0], **v} for k, v in answers.items()},
        'risk_assessment_assumptions_still_valid': assumptions, 'conclusion': conclusion,
        'provisions_requiring_reassessment': provisions, 'consequences': consequences, 'confidence': conf,
        'legal_confirmation_recommended': legal, 'screened_at_utc': datetime.now(timezone.utc).isoformat(),
    }


def markdown(d: dict) -> str:
    cs = d['change_set']
    lines = ['# Substantial modification screening', '', f"**Change set:** {cs.get('description', '')} ({cs.get('from_version', '?')} to {cs.get('to_version', '?')})  ",
             f"**Conclusion:** {d['conclusion']} (confidence {d['confidence']}; legal confirmation recommended: {'yes' if d['legal_confirmation_recommended'] else 'no'})", '',
             '| Factor | Answer | Reasoning |', '|---|---|---|']
    for k, v in d['answers'].items():
        lines.append(f"| {v['question']} | {v['answer']} | {v.get('reasoning', '')} |")
    lines += ['', '## Consequences', ''] + [f'- {c}' for c in d['consequences']]
    lines += ['', '## Provisions requiring re-assessment', '', ', '.join(d['provisions_requiring_reassessment']), '',
              '> Based on Article 3(30) of Regulation (EU) 2024/2847 and the Commission\'s non-binding guidance C(2026) 5252 section 4.3. Not legal advice.', '']
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--answers', required=True); ap.add_argument('--output', default='.')
    args = ap.parse_args()
    d = screen(json.loads(Path(args.answers).read_text(encoding='utf-8')))
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    (out / '25-substantial-modification-screening.json').write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
    (out / '25-substantial-modification-screening.md').write_text(markdown(d), encoding='utf-8')
    print(json.dumps({'conclusion': d['conclusion'], 'confidence': d['confidence'], 'provisions': len(d['provisions_requiring_reassessment'])}))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f'ERROR: {type(e).__name__}: {e}', file=sys.stderr); sys.exit(1)
