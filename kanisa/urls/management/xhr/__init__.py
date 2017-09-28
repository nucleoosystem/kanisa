from django.conf.urls import include, url


urlpatterns = [
    url(r'^diary/', include('kanisa.urls.management.xhr.diary')),
    url(r'^media/', include('kanisa.urls.management.xhr.media')),
    url(r'^navigation/', include('kanisa.urls.management.xhr.navigation')),
    url(r'^pages/', include('kanisa.urls.management.xhr.pages')),
    url(r'^sermons/', include('kanisa.urls.management.xhr.sermons')),
]
