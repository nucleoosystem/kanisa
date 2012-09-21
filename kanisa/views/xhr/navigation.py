from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from kanisa.models import NavigationElement
from kanisa.views.xhr.base import (XHRBaseGetView,
                                   XHRBasePostView,
                                   BadArgument)


class ListNavigationView(XHRBaseGetView):
    permission = 'kanisa.manage_navigation'

    def render(self, request, *args, **kwargs):
        elements = NavigationElement.objects.all()
        tmpl = 'kanisa/management/navigation/_item_list.html'
        return render_to_response(tmpl,
                                  {'object_list': elements},
                                  context_instance=RequestContext(request))


class MoveNavigationElementBase(XHRBasePostView):
    required_arguments = ['navigation_element', ]
    permission = 'kanisa.manage_navigation'

    def get_element(self):
        try:
            element_pk = int(self.arguments['navigation_element'])
            return NavigationElement.objects.get(pk=element_pk)
        except (NavigationElement.DoesNotExist, ValueError):
            raise BadArgument("No navigation element found with ID '%s'."
                              % self.arguments['navigation_element'])

    def render(self, request, *args, **kwargs):
        element = self.get_element()
        try:
            self.move(element)
        except NavigationElement.DoesNotExist:
            raise BadArgument("Cannot move element.")

        return HttpResponse("Element moved.")


class MoveNavigationElementDownView(MoveNavigationElementBase):
    def move(self, element):
        element.move_down()


class MoveNavigationElementUpView(MoveNavigationElementBase):
    def move(self, element):
        element.move_up()
