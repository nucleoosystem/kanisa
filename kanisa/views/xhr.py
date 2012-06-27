from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from kanisa.models.bible.bible import to_passage, InvalidPassage


@csrf_exempt
def check_bible_passage(request):
    if not 'passage' in request.POST:
        return HttpResponseBadRequest("Passage not found.")

    try:
        passage = to_passage(request.POST['passage'])
        return HttpResponse(unicode(passage))
    except InvalidPassage, e:
        if e.message:
            return HttpResponseBadRequest(e.message)
        msg = '"%s" is not a valid Bible passage.' % request.POST['passage']
        return HttpResponseBadRequest(msg)
