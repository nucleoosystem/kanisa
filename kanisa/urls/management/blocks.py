from django.conf.urls import patterns, url
import kanisa.views.blocks as views


urlpatterns = patterns(
    '',
    url(r'^$', views.block_management, {}, 'kanisa_manage_blocks'),
    url(r'^edit/(?P<slug>[a-z0-9-_]+)/$', views.block_update, {},
        'kanisa_manage_blocks_update'),
)
