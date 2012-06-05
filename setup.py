from setuptools import setup, find_packages

import kanisa

setup(
    name='kanisa',
    version=kanisa.__version__,
    description="A Django app for managing Church websites."
    long_description=open('README.md').read(),
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='http://github.com/dominicrodger/kanisa',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django",
    ],
)
