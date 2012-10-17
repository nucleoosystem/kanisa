from django.conf.urls import patterns, url
from kanisa.views.public.search import KanisaSearchView


urlpatterns = patterns('',
                       url(r'^$',
                           KanisaSearchView.as_view(),
                           {},
                           'kanisa_public_search'),
                       )
