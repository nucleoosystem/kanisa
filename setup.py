from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

import kanisa


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='kanisa',
    version=kanisa.__version__,
    description="A Django app for managing Church websites.",
    long_description=open('README.md').read(),
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='http://github.com/dominicrodger/kanisa',
    license='BSD',
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=[
        "BeautifulSoup==3.2.1",
        "Django>=1.4",
        "Pillow==1.7.8",
        "django-autoslug==1.7.1",
        "django-compressor==1.1.2",
        "django-constance==0.6",
        "django-crispy-forms==1.4.0",
        "django-haystack==1.2.7",
        "django-mptt==0.6.0",
        "django-password-reset==0.5.1",
        "django-picklefield==0.3.0",
        "django-recurrence==1.1.0",
        "lxml==3.2.4",
        "markdown==2.3.1",
        "minify==0.1.4",
        "mutagen==1.22",
        "sorl-thumbnail==11.12",
        "south==0.8.4",
        "tweepy==1.11",
        "Whoosh==2.4.1",
        "wsgiref==0.1.2",
    ],
    tests_require=(
        "pytest==2.6.4",
        "pytest-cov==1.7.0",
        "pytest-django==2.8.0",
        "factory-boy==2.2.1",
        "mock==1.0.1",
    ),
    cmdclass = {'test': PyTest},
)
