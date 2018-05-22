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
        "Django",
        "Pillow",
        "django-autoslug",
        "django-crispy-forms",
        "django-haystack",
        "django-mptt",
        "django-password-reset",
        "django-recaptcha",
        "django-recurrence",
        "markdown",
        "mutagen",
        "sorl-thumbnail",
        "Whoosh",
    ],
    tests_require=(
        "pytest",
        "pytest-cov",
        "pytest-django",
        "factory-boy",
        "mock",
    ),
    cmdclass = {'test': PyTest},
)
