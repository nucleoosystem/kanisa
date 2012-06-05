from django.shortcuts import render_to_response
from django.template import RequestContext

from kanisa.models.banners import Banner


def index(request):
    banners = Banner.objects.all()

    return render_to_response('kanisa/index.html',
                              {'banners': banners},
                              context_instance=RequestContext(request))
