cleandist:
	rm -rf kanisa.egg-info/
	rm -rf build/
	rm -rf dist/
	python setup.py bdist_wheel

git-check:
	git status
	git diff-files --quiet

test:
	tox

jshint:
	jshint kanisa/static/kanisa/js/management/* --show-non-errors
	jshint kanisa/static/kanisa/js/public/* --show-non-errors

coverage:
	py.test --cov-report term-missing --cov kanisa

flake8:
	tox -e flake8

push: git-check flake8 test
	git push -u origin master

wheel: push cleandist
