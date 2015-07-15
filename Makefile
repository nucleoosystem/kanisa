clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

cleandist: clean
	python setup.py bdist_wheel

git-check:
	git status
	git diff-files --quiet

test:
	tox

flake8:
	tox -e flake8

jslint:
	jshint kanisa/static/kanisa/js/management/* --show-non-errors
	jshint kanisa/static/kanisa/js/public/* --show-non-errors

lint: flake8 jslint

coverage:
	py.test --cov-report term-missing --cov kanisa

push: git-check flake8 test
	git push -u origin master

wheel: push cleandist
