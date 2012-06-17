from django.core.urlresolvers import reverse
from kanisa.forms import SermonSeriesForm
from kanisa.models import SermonSeries
from kanisa.views.generic import (KanisaCreateView, KanisaUpdateView,
                                  KanisaListView)


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


class SermonSeriesCreateView(KanisaCreateView, SermonBaseView):
    form_class = SermonSeriesForm
    template_name = 'kanisa/management/create.html'
    kanisa_title = 'Create a Sermon Series'

    def get_success_url(self):
        return reverse('kanisa_manage_sermons')


class SermonSeriesUpdateView(KanisaUpdateView, SermonBaseView):
    form_class = SermonSeriesForm
    template_name = 'kanisa/management/create.html'
    model = SermonSeries

    def get_kanisa_title(self):
        return 'Edit Sermon Series: %s' % unicode(self.object)

    def get_success_url(self):
        return reverse('kanisa_manage_sermons')
