Kanisa
======

A project for managing Church websites, built with Django.

Kanisa handles:

* Public pages;
* Sermons;
* A calendar;
* A members' area for documents and service planning;
* Social integration (primarily posting to Twitter currently);
* Search;
* Banners - for advertising upcoming events etc.

You can see it in action at https://www.centralbaptistchelmsford.org.

Requirements
------------

Kanisa expects to essentially be the only app you're running, and
requires Python 2.7. It is tested with Django 1.5 and 1.6.

Installation
------------

You can install Kanisa and its dependencies using:

    pip install -e git+git@github.com:dominicrodger/kanisa.git#egg=kanisa

You'll need to set at least the following settings:

    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    MIDDLEWARE_CLASSES += ['kanisa.middleware.KanisaPageFallbackMiddleware']
    TEMPLATE_CONTEXT_PROCESSORS += ['kanisa.context_processors.kanisa_settings']
    LOGIN_URL = '/members/account/login/'

You'll also need to set up Haystack for search functionality.

You'll need a root `urls.py` which looks a bit like this:

    from django.conf import settings
    from django.conf.urls import patterns, include, url

    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include('kanisa.urls')),
    )
