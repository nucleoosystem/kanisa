from django.conf.urls import patterns, url
import kanisa.views.members.documents as views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, {}, 'kanisa_members_documents'),
)
