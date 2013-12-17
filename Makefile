cleandist:
	rm -rf kanisa.egg-info/
	rm -rf build/
	rm -rf dist/
	python setup.py bdist_wheel

git-check:
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
