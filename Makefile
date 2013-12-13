wheel:
	rm -rf build/
	rm -rf dist/
	python setup.py bdist_wheel

deploy: wheel
	# We probably want the hostname (kanisa, which is an SSH alias
	# I have locally) to be in a config file somewhere.
	scp dist/kanisa-*.whl kanisa:/home/deploy/
	scp deploy.sh kanisa:/home/deploy/
	ssh kanisa bash /home/deploy/deploy.sh
