# Gap ticket integration

## Default behaviour

Every `full` and `retest` assessment generates a structured ticket queue from open gaps (`scripts/export_ticket_queue.py`). Default mode `queue`: local files only. External GitHub Issues, Jira tickets or other work items are created only when the user explicitly authorises it for the run (`external_ticket_creation_authorized=true` in the manifest or an explicit instruction) and a writable connector exists.

Modes: `off`, `queue` (default), `github`, `jira`, `auto` (project-configured provider, with prior explicit authorisation).

## Ticket content

Gap ID and `regression_key`; rating and status; provisions affected (IDs and plain-language source such as "Annex I Part I (2)(b)"); legal exposure and applicable date; affected components; description; risk; remediation; implementation guidance; documentation change required; retest criterion; assessment version and commit; evidence references where safe. Never include secrets or exploit details.

## Deduplication

Search open items for the gap ID or regression key before creating; update or comment instead of duplicating.

## Priority mapping

Critical to highest; High to high; Medium to normal; Low to low; Observation to backlog. Ticket priority never changes provision status.

## Closure

Closing a ticket is not evidence of remediation. Only the retest process closes a gap.
