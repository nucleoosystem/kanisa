from django.conf.urls import patterns, include, url
from kanisa.views.management import KanisaManagementIndexView


urlpatterns = patterns(
    '',
    url(r'^$', KanisaManagementIndexView.as_view(), {}, 'kanisa_manage_index'),
    url(r'^banners/', include('kanisa.urls.management.banners')),
    url(r'^blocks/', include('kanisa.urls.management.blocks')),
    url(r'^blog/', include('kanisa.urls.management.blog')),
    url(r'^branding/', include('kanisa.urls.management.branding')),
    url(r'^diary/', include('kanisa.urls.management.diary')),
    url(r'^documents/', include('kanisa.urls.management.documents')),
    url(r'^media/', include('kanisa.urls.management.media')),
    url(r'^navigation/', include('kanisa.urls.management.navigation')),
    url(r'^pages/', include('kanisa.urls.management.pages')),
    url(r'^sermons/', include('kanisa.urls.management.sermons')),
    url(r'^users/', include('kanisa.urls.management.users')),
    url(r'^xhr/', include('kanisa.urls.management.xhr')),
)
