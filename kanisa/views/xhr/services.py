from django.http import HttpResponse, HttpResponseBadRequest
import json
from kanisa.models import Band
from kanisa.views.xhr.base import XHRBaseGetView


class BandInformationView(XHRBaseGetView):
    required_arguments = ['band_id', ]
    permission = None

    def render(self, request, *args, **kwargs):
        try:
            band = Band.objects.get(pk=request.GET['band_id'])
            musicians = [m.pk for m in band.musicians.only('pk')]
            band_leader = band.band_leader.pk
            return HttpResponse(
                json.dumps({'band_leader': band_leader,
                            'musicians': musicians})
            )
        except Band.DoesNotExist:
            return HttpResponseBadRequest("Invalid band_id")
