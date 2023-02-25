# adapted from qqiime2, freyja
.PHONY: all lint test test-cov install dev clean distclean

PYTHON ?= python

all: ;

lint:
	flake8 Python-outbreak-info

test: all
	py.test

test-install: all
	# ensure the package is installed and the app is buildable. this test
	# is a passive verification that non-py essential files are part of the
	# installed entity.
	cd /  # go somewhere to avoid relative imports
	python -c "import outbreak_data"
	python -c "import outbreak_tools"

# test-cov: all
# 	py.test --cov=outbreakpy
# 	coveralls

install: all
	$(PYTHON) setup.py install

dev: all
	pip install -e .

clean: distclean

distclean: ;
