# Sample assessment fixture

A **fictional**, minimal evidence pack showing the machine-readable files the scripts consume:

- `00-assessment-manifest.json` - pinned product, mode, role and legal baseline;
- `07-requirement-matrix.csv` - one row per provision in the generated catalogue (96 for the pinned text), with gaps, one justified not-applicable, one blocked and one not-assessed row;
- `10-adjudication-log.jsonl` - the adjudication record behind the not-applicable decision;
- `11-gaps-register.jsonl` - the two gaps behind the GAP rows, one of which is a live Article 14 obligation.

Used by the test suite and usable as a trial baseline:

```bash
python scripts/export_ticket_queue.py --assessment-dir examples/sample-assessment --output /tmp/queue
python scripts/compare_assessments.py --baseline examples/sample-assessment --current examples/sample-assessment --output /tmp/regression
```

Nothing here represents a real product, manufacturer or assessment outcome.
