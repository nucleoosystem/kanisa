from django.http import HttpResponse
from django.shortcuts import render

from kanisa.models import NavigationElement
from kanisa.views.xhr.base import (XHRBaseGetView,
                                   XHRBasePostView,
                                   BadArgument)


class ListNavigationView(XHRBaseGetView):
    permission = 'kanisa.manage_navigation'

    def render(self, request, *args, **kwargs):
        elements = NavigationElement.objects.all()
        tmpl = 'kanisa/management/navigation/_item_list.html'
        return render(request,
                      tmpl,
                      {'object_list': elements})
list_navigation = ListNavigationView.as_view()


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
move_navigation_down = MoveNavigationElementDownView.as_view()


class MoveNavigationElementUpView(MoveNavigationElementBase):
    def move(self, element):
        element.move_up()
move_navigation_up = MoveNavigationElementUpView.as_view()
