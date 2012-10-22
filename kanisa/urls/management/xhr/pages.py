from django.conf.urls import patterns, url
from kanisa.views.xhr.pages import (CreatePageView,
                                    ListPagesView)


urlpatterns = patterns('',
                       url(r'^create/$',
                           CreatePageView.as_view(),
                           {},
                           'kanisa_manage_xhr_create_page'),
                       url(r'^list/$',
                           ListPagesView.as_view(),
                           {},
                           'kanisa_manage_xhr_list_pages'),
                       )
