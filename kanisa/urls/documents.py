from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required as smr
from kanisa.views.documents import (DocumentIndexView,
                                    DocumentCreateView,
                                    DocumentUpdateView)

urlpatterns = patterns('',
                       url(r'^$',
                           smr(DocumentIndexView.as_view()),
                           {},
                           'kanisa_manage_documents'),
                       url(r'^create/$',
                           smr(DocumentCreateView.as_view()),
                           {},
                           'kanisa_manage_documents_create'),
                       url(r'^edit/(?P<pk>\d+)$',
                           smr(DocumentUpdateView.as_view()),
                           {},
                           'kanisa_manage_documents_update'),
                       )
