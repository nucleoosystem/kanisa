cleandist:
	rm -rf kanisa.egg-info/
	rm -rf build/
	rm -rf dist/
	python setup.py bdist_wheel

reminify:
	rm -f kanisa/static/kanisa/js/minified/*.js
	rm -f kanisa/static/kanisa/css/minified/*.css
	python setup.py minify_management_js
	python setup.py minify_public_js
	python setup.py minify_css

# We reminify the JavaScript to ensure that no changes have been made
# which haven't been propagated to the minified JavaScript.
git-check: reminify
	git status
	git diff-files --quiet

test:
	tox

flake8:
	tox -e flake8

push: git-check test
	git push -u origin master

wheel: push cleandist

# We probably want the hostname (kanisa, which is an SSH alias I have
# locally) to be in a config file somewhere.
deploy: wheel
	scp dist/kanisa-*.whl kanisa:/home/deploy/
	scp deploy.sh kanisa:/home/deploy/
	ssh kanisa bash /home/deploy/deploy.sh
