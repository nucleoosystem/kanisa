from django.conf.urls import url
import kanisa.views.members.documents as views


urlpatterns = [
    url(r'^$', views.index, {}, 'kanisa_members_documents'),
    url(r'^(?P<document_pk>\d+)$', views.download, {},
        'kanisa_members_documents_download'),
]
