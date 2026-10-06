.PHONY: validate sync check rebuild init

validate:
	python scripts/validate_repo.py
	python -m unittest discover -s tests -p 'test_*.py'

# Fetch the official texts from the Publications Office and rebuild the catalogues (network).
sync:
	python scripts/sync_official_text.py --sync
	python scripts/validate_repo.py

# Report whether any pinned official text changed (network); exit code 2 means changed.
check:
	python scripts/sync_official_text.py --check

# Rebuild the generated catalogues from official/current without network.
rebuild:
	python scripts/sync_official_text.py --rebuild-local
	python scripts/validate_repo.py

init:
	@test -n "$(PRODUCT)" || (echo "PRODUCT is required" && exit 2)
	@test -n "$(VERSION)" || (echo "VERSION is required" && exit 2)
	python scripts/init_assessment.py --product "$(PRODUCT)" --version "$(VERSION)" $(ARGS)
