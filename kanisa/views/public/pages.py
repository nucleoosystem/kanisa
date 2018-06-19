from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render
from kanisa.models.pages import (
    Page,
    get_page_from_path,
    get_page_from_path_including_drafts
)


def public_page_view(request):
    if request.user.has_perm('kanisa.manage_pages'):
        func = get_page_from_path_including_drafts
    else:
        func = get_page_from_path

    try:
        page = func(request.path)

        parent_path = None
        if page.parent:
            parent_path = page.parent.get_path()

        return render(
            request,
            'kanisa/public/pages/page.html',
            {'page': page,
             'parent': page.parent,
             'parent_path': parent_path,
             'page_path': page.get_path(),
             'siblings': page.get_published_siblings(),
             'children': page.get_published_children(),
             'kanisa_title': unicode(page)})
    except Page.DoesNotExist:
        if not request.path.endswith('/') and settings.APPEND_SLASH:
            try:
                page = func(request.path + '/')
            except Page.DoesNotExist:
                raise Http404
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise Http404
