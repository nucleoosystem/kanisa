from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^speedbar/', include('speedbar.urls')),
    url(r'^djohno/', include('djohno.urls')),
    url(r'^', include('kanisa.urls')),
)


handler500 = 'kanisa.views.server_error'
