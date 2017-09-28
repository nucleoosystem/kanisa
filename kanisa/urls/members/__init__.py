from django.conf.urls import include, url
import kanisa.views.members as base


urlpatterns = [
    url(r'^$', base.index, {}, 'kanisa_members_index'),
    url(r'^account/', include('kanisa.urls.members.account')),
    url(r'^documents/', include('kanisa.urls.members.documents')),
    url(r'^services/', include('kanisa.urls.members.services')),
]
