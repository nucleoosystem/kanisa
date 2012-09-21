from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from kanisa.forms.navigation import NavigationElementForm
from kanisa.models import NavigationElement
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaListView,
                                  KanisaCreateView,
                                  KanisaUpdateView)


class NavigationElementBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Navigation elements appear in the navigation bar at the '
                   'top of every page.')
    kanisa_root_crumb = {'text': 'Navigation',
                         'url': reverse_lazy('kanisa_manage_navigation')}
    permission = 'kanisa.manage_navigation'
    kanisa_nav_component = 'navigation'


class NavigationElementIndexView(NavigationElementBaseView,
                                 KanisaListView):
    model = NavigationElement

    template_name = 'kanisa/management/navigation/index.html'
    kanisa_title = 'Manage Navigation'
    kanisa_is_root_view = True


class NavigationElementCreateView(NavigationElementBaseView,
                                  KanisaCreateView):
    form_class = NavigationElementForm
    kanisa_title = 'Create Navigation Element'
    success_url = reverse_lazy('kanisa_manage_navigation')


class NavigationElementUpdateView(NavigationElementBaseView,
                                  KanisaUpdateView):
    form_class = NavigationElementForm
    model = NavigationElement
    success_url = reverse_lazy('kanisa_manage_navigation')
