from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from kanisa.forms import SermonSeriesForm, SermonForm
from kanisa.models import SermonSeries, Sermon
from kanisa.views.generic import (KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaDetailView)


class SermonBaseView:
    kanisa_lead = ('Having sermons on your site allows people who can\'t make '
                   'services to keep up with what you\'re learning.')

    def get_kanisa_root_crumb(self):
        return {'text': 'Sermons',
                'url': reverse('kanisa_manage_sermons')}


class SermonIndexView(KanisaListView, SermonBaseView):
    model = SermonSeries
    queryset = SermonSeries.objects.all()

    template_name = 'kanisa/management/sermons/index.html'
    kanisa_title = 'Manage Sermons'
    kanisa_is_root_view = True


class SermonSeriesDetailView(KanisaDetailView, SermonBaseView):
    model = SermonSeries
    template_name = 'kanisa/management/sermons/series_detail.html'

    def get_kanisa_title(self):
        return unicode(self.object)

    def get_success_url(self):
        return reverse('kanisa_manage_sermons')


class SermonSeriesCreateView(KanisaCreateView, SermonBaseView):
    form_class = SermonSeriesForm
    kanisa_title = 'Create a Sermon Series'

    def get_success_url(self):
        return reverse('kanisa_manage_sermons')


class SermonSeriesUpdateView(KanisaUpdateView, SermonBaseView):
    form_class = SermonSeriesForm
    model = SermonSeries

    def get_kanisa_title(self):
        return 'Edit Sermon Series: %s' % unicode(self.object)

    def get_success_url(self):
        return reverse('kanisa_manage_sermons')


class SermonSeriesCompleteView(RedirectView):
    permanent = False

    def get_redirect_url(self, sermon_id):
        series = get_object_or_404(SermonSeries, pk=sermon_id)
        series.active = False
        series.save()

        message = u'Series "%s" marked as complete.' % unicode(series)
        messages.success(self.request, message)

        return reverse('kanisa_manage_sermons')


class SermonCreateView(KanisaCreateView, SermonBaseView):
    form_class = SermonForm
    kanisa_title = 'Upload a Sermon'

    def get_initial(self):
        initial = super(SermonCreateView, self).get_initial()
        initial = initial.copy()

        if 'series' in self.request.GET:
            initial['series'] = self.request.GET['series']

        return initial

    def get_success_url(self):
        if self.object.series:
            return reverse('kanisa_manage_sermons_series_detail',
                           args=[self.object.series.pk, ])
        return reverse('kanisa_manage_sermons')


class SermonUpdateView(KanisaUpdateView, SermonBaseView):
    form_class = SermonForm
    model = Sermon

    def get_kanisa_title(self):
        return 'Edit Sermon: %s' % unicode(self.object)

    def get_success_url(self):
        if self.object.series:
            return reverse('kanisa_manage_sermons_series_detail',
                           args=[self.object.series.pk, ])
        return reverse('kanisa_manage_sermons')
