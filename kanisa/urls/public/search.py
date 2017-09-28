from django.conf.urls import url
from kanisa.views.public.search import KanisaSearchView


urlpatterns = [
    url(r'^$', KanisaSearchView.as_view(), {}, 'kanisa_public_search'),
]
