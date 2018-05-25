from django.conf.urls import url
import kanisa.views.management.documents as views


urlpatterns = [
    url(r'^$', views.document_management, {}, 'kanisa_manage_documents'),
    url(r'^create/$', views.document_create, {},
        'kanisa_manage_documents_create'),
    url(r'^edit/(?P<pk>\d+)/$', views.document_update, {},
        'kanisa_manage_documents_update'),
    url(r'^delete/(?P<pk>\d+)/$', views.document_delete, {},
        'kanisa_manage_documents_delete'),
    url(r'^expire/(?P<pk>\d+)/$', views.document_expire, {},
        'kanisa_manage_documents_expire'),
]
