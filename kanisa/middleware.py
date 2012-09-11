from django.http import Http404, HttpResponsePermanentRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from kanisa.models.pages import Page, get_page_from_path


class KanisaPageFallbackMiddleware(object):
    def get_page_response(self, request):
        try:
            page = get_page_from_path(request.path)
            return render_to_response('kanisa/public/pages/page.html',
                                      {'page': page},
                                      context_instance=RequestContext(request))
        except Page.DoesNotExist:
            if not request.path.endswith('/') and settings.APPEND_SLASH:
                page = get_page_from_path(request.path + '/')
                return HttpResponsePermanentRedirect('%s/' % request.path)
            else:
                raise

    def process_response(self, request, response):
        if response.status_code != 404:
            # No need to check for a page for non-404 responses.
            return response
        try:
            return self.get_page_response(request)
        except Page.DoesNotExist:
            return response

        # Return the original response if any errors happened. Because
        # this is a middleware, we can't assume the errors will be
        # caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
