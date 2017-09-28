from django.conf.urls import url
import kanisa.views.xhr.sermons as views


urlpatterns = [
    url(r'^markcomplete/$', views.mark_complete, {},
        'kanisa_manage_xhr_sermon_series_complete'),
]
