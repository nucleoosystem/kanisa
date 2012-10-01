from django.conf.urls import patterns, url
from kanisa.views.documents import (DocumentIndexView,
                                    DocumentCreateView,
                                    DocumentUpdateView,
                                    DocumentDeleteView)

urlpatterns = patterns('',
                       url(r'^$',
                           DocumentIndexView.as_view(),
                           {},
                           'kanisa_manage_documents'),
                       url(r'^create/$',
                           DocumentCreateView.as_view(),
                           {},
                           'kanisa_manage_documents_create'),
                       url(r'^edit/(?P<pk>\d+)$',
                           DocumentUpdateView.as_view(),
                           {},
                           'kanisa_manage_documents_update'),
                       url(r'^delete/(?P<pk>\d+)$',
                           DocumentDeleteView.as_view(),
                           {},
                           'kanisa_manage_documents_delete'),
                       )
