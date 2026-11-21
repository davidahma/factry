PYTHON ?= python3
RUBY ?= ruby

.PHONY: check
check:
	$(RUBY) scripts/check.rb
	$(PYTHON) examples/verify/demo.py --check
	$(PYTHON) -B -m unittest discover -s tests -v
	git diff --check "$$(git hash-object -t tree /dev/null)" --
