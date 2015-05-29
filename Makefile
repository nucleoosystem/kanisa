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

# We probably want the hostname (kanisa, which is an SSH alias I have
# locally), and the directories to be in a config file somewhere. This
# task just deploys the wheel that's already built, use "make deploy"
# to ensure you're deploying the latest version.
redeploy:
	scp dist/kanisa-*.whl kanisa:/home/deploy/
	scp deploy.sh kanisa:/home/deploy/
	scp single_deploy.sh kanisa:/home/deploy/
	ssh kanisa bash /home/deploy/deploy.sh

deploy: wheel redeploy
	echo "Deployment complete."
