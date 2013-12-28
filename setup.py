from setuptools import setup, find_packages

import kanisa

setup(
    name='kanisa',
    version=kanisa.__version__,
    description="A Django app for managing Church websites.",
    long_description=open('README.md').read(),
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='http://github.com/dominicrodger/kanisa',
    license='BSD',
    packages=find_packages(exclude=["kanisa.tests", "kanisa.tests.*"]),
    include_package_data=True,
    install_requires=[
        "BeautifulSoup==3.2.1",
        "Django>=1.4",
        "PIL==1.1.7",
        "django-autoslug==1.7.1",
        "django-compressor==1.1.2",
        "django-crispy-forms==1.4.0",
        "django-haystack==1.2.7",
        "django-mptt==0.6.0",
        "django-password-reset==0.5.1",
        "django-recurrence==1.0.1",
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
        "django-setuptest==0.1.4",
        "factory-boy==2.2.1",
        "mock==1.0.1",
    ),
    test_suite='setuptest.setuptest.SetupTestSuite',
)
