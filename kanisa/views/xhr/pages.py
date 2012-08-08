import json
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string

from kanisa.models import Page
from kanisa.views.xhr.base import XHRBasePostView, XHRBaseGetView, BadArgument


class CreatePageView(XHRBasePostView):
    permission = 'kanisa.manage_pages'
    required_arguments = ['title', 'parent', ]

    def get_title(self):
        title = self.arguments['title']

        if not title:
            raise BadArgument("Title must not be empty.")

        return title

    def get_parent(self):
        parent = self.arguments['parent']

        if not parent:
            return None

        try:
            return Page.objects.get(pk=parent)
        except (Page.DoesNotExist, ValueError):
            raise BadArgument("Page with ID '%s' not found."
                              % parent)

    def render(self, request, *args, **kwargs):
        title = self.get_title()
        parent = self.get_parent()

        Page.objects.create(title=title,
                            parent=parent,
                            draft=True)

        return HttpResponse("Page created.")


class ListPagesView(XHRBaseGetView):
    permission = 'kanisa.manage_pages'

    def render(self, request, *args, **kwargs):
        pages = Page.objects.all()
        tmpl = 'kanisa/management/pages/_page_table.html'
        page_table = render_to_string(tmpl,
                                      {'page_list': pages},
                                      context_instance=RequestContext(request))

        tmpl = 'kanisa/management/pages/_parent_select_options.html'
        options = render_to_string(tmpl,
                                   {'page_list': pages},
                                   context_instance=RequestContext(request))

        response = {'page_table': page_table,
                    'options': options}
        return HttpResponse(json.dumps(response))
