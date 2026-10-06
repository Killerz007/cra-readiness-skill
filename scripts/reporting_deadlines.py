#!/usr/bin/env python3
"""Compute Article 14 reporting deadlines from the awareness timestamp.

Article 14(2) (actively exploited vulnerability): early warning within 24 hours of awareness;
vulnerability notification within 72 hours of awareness; final report no later than 14 days after a
corrective or mitigating measure is available.

Article 14(4) (severe incident): early warning within 24 hours; incident notification within 72
hours; final report within one month after the submission of the incident notification.

"Without undue delay and in any event within" means the stated limits are outer bounds, not targets.

Usage:
  python scripts/reporting_deadlines.py --type vulnerability --awareness 2026-10-06T14:30:00+02:00 [--mitigation-available 2026-10-09T10:00:00+02:00]
  python scripts/reporting_deadlines.py --type incident --awareness 2026-10-06T14:30:00+02:00 [--notification-submitted 2026-10-08T09:00:00+02:00]

Timestamps must carry a UTC offset. Output is JSON.
"""
import argparse, calendar, json, sys
from datetime import datetime, timedelta


def parse(ts: str) -> datetime:
    d = datetime.fromisoformat(ts.replace('Z', '+00:00'))
    if d.tzinfo is None:
        raise ValueError(f'timestamp {ts!r} has no UTC offset; the clock must be unambiguous')
    return d


def add_one_month(d: datetime) -> datetime:
    year, month = (d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1)
    day = min(d.day, calendar.monthrange(year, month)[1])
    return d.replace(year=year, month=month, day=day)


def compute(kind: str, awareness: datetime, mitigation: datetime | None, notification_submitted: datetime | None) -> dict:
    out = {
        'type': kind, 'awareness': awareness.isoformat(),
        'early_warning_due': (awareness + timedelta(hours=24)).isoformat(),
        'notification_due': (awareness + timedelta(hours=72)).isoformat(),
        'note': 'Deadlines are outer limits ("without undue delay and in any event within"). Submit via the ENISA single reporting platform to the CSIRT designated as coordinator (Article 14(7)).',
    }
    if kind == 'vulnerability':
        out['final_report_rule'] = 'No later than 14 days after a corrective or mitigating measure is available (Article 14(2)(c)).'
        out['final_report_due'] = (mitigation + timedelta(days=14)).isoformat() if mitigation else None
        if not mitigation:
            out['final_report_note'] = 'Provide --mitigation-available to compute the final report deadline.'
    else:
        out['final_report_rule'] = 'Within one month after the submission of the incident notification (Article 14(4)(c)).'
        if notification_submitted:
            out['final_report_due'] = add_one_month(notification_submitted).isoformat()
        else:
            out['final_report_due'] = None
            out['final_report_planning_estimate'] = add_one_month(awareness + timedelta(hours=72)).isoformat()
            out['final_report_note'] = 'Estimate assumes the notification is submitted at the 72-hour limit; provide --notification-submitted for the actual deadline.'
    out['user_information'] = 'Inform impacted users, and where appropriate all users, after becoming aware (Article 14(8)); no fixed deadline, act without undue delay and proportionately.'
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--type', choices=['vulnerability', 'incident'], required=True)
    ap.add_argument('--awareness', required=True); ap.add_argument('--mitigation-available'); ap.add_argument('--notification-submitted')
    args = ap.parse_args()
    out = compute(args.type, parse(args.awareness), parse(args.mitigation_available) if args.mitigation_available else None, parse(args.notification_submitted) if args.notification_submitted else None)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f'ERROR: {type(e).__name__}: {e}', file=sys.stderr); sys.exit(1)
