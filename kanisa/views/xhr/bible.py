from django.http import HttpResponse, HttpResponseBadRequest
from kanisa.models.bible.bible import to_passage, InvalidPassage
from kanisa.views.xhr import XHRBasePostView


class CheckBiblePassageView(XHRBasePostView):
    required_arguments = ['passage', ]
    permission = None

    def render(self, request, *args, **kwargs):
        try:
            passage = to_passage(request.POST['passage'])
            return HttpResponse(unicode(passage))
        except InvalidPassage, e:
            return HttpResponseBadRequest(unicode(e))
