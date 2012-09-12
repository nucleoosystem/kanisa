from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from kanisa.models.pages import Page, get_page_from_path


def public_page_view(request):
    try:
        page = get_page_from_path(request.path)

        return render_to_response('kanisa/public/pages/page.html',
                                  {'page': page},
                                  context_instance=RequestContext(request))
    except Page.DoesNotExist:
        if not request.path.endswith('/') and settings.APPEND_SLASH:
            try:
                page = get_page_from_path(request.path + '/')
            except Page.DoesNotExist:
                raise Http404
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise Http404
