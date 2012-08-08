from django.http import HttpResponse
from kanisa.models import SermonSeries
from kanisa.views.xhr import XHRBasePostView, BadArgument


class MarkSermonSeriesCompleteView(XHRBasePostView):
    required_arguments = ['series', ]
    permission = 'kanisa.manage_sermons'

    def get_series(self):
        try:
            series_pk = int(self.arguments['series'])
            return SermonSeries.objects.get(pk=series_pk)
        except (SermonSeries.DoesNotExist, ValueError):
            raise BadArgument("No sermon series found with ID '%s'."
                              % self.arguments['series'])

    def render(self, request, *args, **kwargs):
        series = self.get_series()
        series.active = False
        series.save()
        return HttpResponse("Series marked complete.")
