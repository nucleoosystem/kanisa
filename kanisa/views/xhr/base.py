from django.http import (HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.views.generic import View


class MissingArgument(Exception):
    pass


class BadArgument(Exception):
    pass


class XHRBaseView(View):
    required_arguments = []

    def check_permissions(self, request):
        if not request.is_ajax():
            return HttpResponseForbidden("This page is not directly "
                                         "accessible.")

        if self.permission:
            if not request.user.has_perm(self.permission):
                return HttpResponseForbidden("You do not have permission "
                                             "to view this page.")

    def check_required_arguments(self):
        for arg in self.required_arguments:
            if arg not in self.arguments:
                raise MissingArgument(arg)

    def handle(self, request, *args, **kwargs):
        response = self.check_permissions(request)

        if response:
            return response

        try:
            self.check_required_arguments()
        except MissingArgument, e:
            message = "Required argument '%s' not found." % str(e)
            return HttpResponseBadRequest(message)

        try:
            return self.render(request, *args, **kwargs)
        except BadArgument, e:
            return HttpResponseBadRequest(e)


class XHRBasePostView(XHRBaseView):
    def post(self, request, *args, **kwargs):
        self.arguments = request.POST

        return self.handle(request, *args, **kwargs)


class XHRBaseGetView(XHRBaseView):
    def get(self, request, *args, **kwargs):
        self.arguments = request.GET

        return self.handle(request, *args, **kwargs)
