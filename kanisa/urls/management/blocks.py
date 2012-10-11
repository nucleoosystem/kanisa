from django.conf.urls import patterns, url
from kanisa.views.blocks import (BlockIndexView,
                                 BlockUpdateView)

urlpatterns = patterns('',
                       url(r'^$',
                           BlockIndexView.as_view(),
                           {},
                           'kanisa_manage_blocks'),
                       url(r'^edit/(?P<slug>[a-z0-9-]+)/$',
                           BlockUpdateView.as_view(),
                           {},
                           'kanisa_manage_blocks_update'),
                       )
