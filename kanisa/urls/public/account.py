from django.conf.urls import patterns, url
from kanisa.views import KanisaLoginView


urlpatterns = patterns('',
                       url(r'^login/$',
                           KanisaLoginView.as_view(),
                           {},
                           'kanisa_public_login'),
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           {'template_name': 'kanisa/logout.html', },
                           'kanisa_public_logout'),
                       )
