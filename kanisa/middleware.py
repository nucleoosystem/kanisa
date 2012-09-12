from django.http import Http404
from django.conf import settings
from kanisa.views.public.pages import public_page_view


class KanisaPageFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            # No need to check for a page for non-404 responses.
            return response

        try:
            return public_page_view(request)
        except Http404:
            return response

        # Return the original response if any errors happened. Because
        # this is a middleware, we can't assume the errors will be
        # caught elsewhere.
        except:
            if settings.DEBUG:
                raise
            return response
