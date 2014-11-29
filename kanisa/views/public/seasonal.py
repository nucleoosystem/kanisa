from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView
from kanisa.models import SeasonalEvent


class SeasonalView(TemplateView):
    template_name = 'kanisa/public/seasonal/index.html'

    def get_season(self):
        return self.kwargs['season']

    def get_events(self):
        season = self.get_season()

        if season == 'christmas':
            letter = 'C'
        elif season == 'easter':
            letter = 'E'
        else:
            raise ImproperlyConfigured(
                'Unknown season: %s.' % season
            )

        return SeasonalEvent.objects.filter(season=letter)

    def get_context_data(self, **kwargs):
        context = super(SeasonalView,
                        self).get_context_data(**kwargs)

        context['season'] = self.get_season()
        context['content_block_intro'] = (
            'seasonal_intro_%s' % self.get_season()
        )
        context['events'] = self.get_events()

        return context
seasonal_view = SeasonalView.as_view()
