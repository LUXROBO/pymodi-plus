.PHONY: clean clean-test clean-pyc clean-build docs
.DEFAULT_GOAL := install

ifeq ($(shell which python3),)
	MODI_PYTHON = python
else
	MODI_PYTHON = python3
endif

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := $(MODI_PYTHON) -c "$$BROWSER_PYSCRIPT"


# remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test

# remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

# remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

# check style with flake8
lint:
	flake8 modi_plus examples tests

# run tests quickly with the default Python
test:
	$(MODI_PYTHON) setup.py test

# generate Sphinx HTML documentation, including API docs
docs:
	rm -f docs/modi_plus.*
	rm -f docs/modules.md
	sphinx-apidoc -o docs/ modi_plus
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

# package and upload a release
release: dist
	twine upload dist/*

# builds source and wheel package
dist: clean
	$(MODI_PYTHON) setup.py sdist
	$(MODI_PYTHON) setup.py bdist_wheel
	ls -l dist

# install the package to the active Python's site-packages
install: clean
	$(MODI_PYTHON) setup.py install
