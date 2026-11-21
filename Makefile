PYTHON ?= python3
RUBY ?= ruby

.PHONY: check team-check
check:
	LC_ALL=C $(RUBY) scripts/check.rb
	$(PYTHON) examples/verify/demo.py --check
	$(MAKE) team-check
	$(PYTHON) -B -m unittest discover -s tests -v
	git diff --check "$$(git hash-object -t tree /dev/null)" --

team-check:
	$(PYTHON) -B examples/team-change/demo.py --check
