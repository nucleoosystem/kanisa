from django.conf.urls import url
import kanisa.views.management.blocks as views


urlpatterns = [
    url(r'^$', views.block_management, {}, 'kanisa_manage_blocks'),
    url(r'^edit/(?P<slug>[a-z0-9-_]+)/$', views.block_update, {},
        'kanisa_manage_blocks_update'),
]
