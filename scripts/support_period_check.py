#!/usr/bin/env python3
"""Check a declared support period against Article 13(8), (9), (13) and (18) and compute retention dates.

Usage:
  python scripts/support_period_check.py --placed 2028-01-15 --support-end 2033-01-31 --expected-use-years 5 \
      [--shorter-justification "subscription-only software"] [--update-issued 2028-06-01 --update-issued 2029-03-01] [--output check.json]

Rules encoded:
  * support period at least five years, unless expected use is shorter, in which case it equals expected use (Article 13(8));
  * five years is a floor, not a default: a period shorter than the expected use time is flagged (guidance point 126);
  * each security update issued during the support period stays available for at least 10 years after issue or the
    remainder of the support period, whichever is longer (Article 13(9));
  * technical documentation, declaration and user information are kept for 10 years after placing on the market or the
    support period, whichever is longer (Article 13(13), (18)).
"""
import argparse, json, sys
from datetime import date, timedelta
from pathlib import Path


def years_between(a: date, b: date) -> float:
    return (b - a).days / 365.25


def add_years(d: date, n: int) -> date:
    try:
        return d.replace(year=d.year + n)
    except ValueError:  # 29 February
        return d.replace(year=d.year + n, day=28)


def check(placed: date, end: date, expected: float, shorter_justification: str | None, updates: list[date]) -> dict:
    checks = []; sp_years = years_between(placed, end)

    def add(cid, status, msg, basis):
        checks.append({'id': cid, 'status': status, 'message': msg, 'legal_basis': basis})
    if end <= placed:
        add('end_after_placing', 'fail', 'Support period end must be after the placing-on-market date', 'Article 13(8)')
    if expected < 5:
        if abs(sp_years - expected) <= 0.1:
            add('minimum_five_years', 'pass' if shorter_justification else 'warn', f'Support period {sp_years:.2f} years equals the expected use time {expected} years (< 5), ' + ('justified: ' + shorter_justification if shorter_justification else 'but no justification for a shorter expected use time was given'), 'Article 13(8) third subparagraph; Recital 60')
        elif sp_years < expected:
            add('minimum_five_years', 'fail', f'Support period {sp_years:.2f} years is shorter than the expected use time {expected} years', 'Article 13(8)')
        else:
            add('minimum_five_years', 'pass', f'Support period {sp_years:.2f} years covers the expected use time {expected} years', 'Article 13(8)')
    else:
        if sp_years + 0.01 < 5:
            add('minimum_five_years', 'fail', f'Support period {sp_years:.2f} years is below the five-year minimum and the expected use time is not shorter than five years', 'Article 13(8) third subparagraph')
        else:
            add('minimum_five_years', 'pass', f'Support period {sp_years:.2f} years meets the five-year minimum', 'Article 13(8) third subparagraph')
        if sp_years + 0.01 < expected:
            add('reflects_expected_use', 'warn', f'Support period {sp_years:.2f} years is shorter than the expected use time {expected} years; five years is a safeguard, not a default', 'Article 13(8) second subparagraph; guidance point 126; Recital 60')
        else:
            add('reflects_expected_use', 'pass', 'Support period reflects the expected use time', 'Article 13(8) second subparagraph')
    docs_until = max(add_years(placed, 10), end)
    add('documentation_retention', 'info', f'Keep technical documentation and the EU declaration of conformity until at least {docs_until.isoformat()}', 'Article 13(13)')
    add('user_information_availability', 'info', f'Keep Annex II user information available (online if provided online) until at least {docs_until.isoformat()}', 'Article 13(18)')
    computed = {'documentation_retained_until': docs_until.isoformat(), 'user_information_available_until': docs_until.isoformat()}
    for i, u in enumerate(updates, 1):
        until = max(add_years(u, 10), end)
        computed[f'update_{i}_issued_{u.isoformat()}_available_until'] = until.isoformat()
        if u > end:
            add(f'update_{i}_within_support', 'warn', f'Update issued {u.isoformat()} is after the support period end; Article 13(9) covers updates made available during the support period', 'Article 13(9)')
    if updates:
        add('update_availability', 'info', f'Each security update issued during the support period must remain available for 10 years after issue or until {end.isoformat()}, whichever is later', 'Article 13(9)')
    add('end_date_communication', 'info', 'The end date (at least month and year) must be clearly specified at the time of purchase, and on the product, packaging or digitally where applicable; display an end-of-support notification where technically feasible', 'Article 13(19); Annex II point 7')
    result = 'FAIL' if any(c['status'] == 'fail' for c in checks) else ('PASS_WITH_WARNINGS' if any(c['status'] == 'warn' for c in checks) else 'PASS')
    return {'placed_on_market': placed.isoformat(), 'declared_support_period_end': end.isoformat(), 'declared_support_period_years': round(sp_years, 2), 'expected_use_years': expected, 'checks': checks, 'computed_dates': computed, 'result': result}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--placed', required=True); ap.add_argument('--support-end', required=True); ap.add_argument('--expected-use-years', type=float, required=True)
    ap.add_argument('--shorter-justification'); ap.add_argument('--update-issued', action='append', default=[]); ap.add_argument('--output')
    args = ap.parse_args()
    out = check(date.fromisoformat(args.placed), date.fromisoformat(args.support_end), args.expected_use_years, args.shorter_justification, [date.fromisoformat(u) for u in args.update_issued])
    if args.output:
        Path(args.output).write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(out, indent=2))
    return 2 if out['result'] == 'FAIL' else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f'ERROR: {type(e).__name__}: {e}', file=sys.stderr); sys.exit(1)
