from datetime import datetime
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
import json
from kanisa.models import Band, ScheduledEvent
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


class EventsView(XHRBaseGetView):
    required_arguments = ['date', ]
    permission = None

    def render(self, request, *args, **kwargs):
        raw_date = self.request.GET['date']

        try:
            parsed_date = datetime.strptime(raw_date,
                                            '%d/%m/%Y')
        except ValueError:
            return HttpResponseBadRequest(
                "Invalid date - should be dd/mm/yyyy"
            )

        qs = ScheduledEvent.objects.filter(date=parsed_date)
        return HttpResponse(
            json.dumps({"events": [(e.id, unicode(e)) for e in qs]})
        )
