from django.http import Http404
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from kanisa.models.pages import get_page_for_request


class KanisaPageFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            # No need to check for a page for non-404 responses.
            return response
        try:
            page = get_page_for_request(request.path)
            return render_to_response('kanisa/public/pages/page.html',
                                      {'page': page},
                                      context_instance=RequestContext(request))

        # Return the original response if any errors happened. Because
        # this is a middleware, we can't assume the errors will be
        # caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
