from datetime import time
from django.core.urlresolvers import reverse


from kanisa.forms import RegularEventForm
from kanisa.models import RegularEvent
from kanisa.views.generic import (KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaTemplateView)


class DiaryBaseView:
    kanisa_lead = ('Diary events are regularly occurring events you want to '
                   'display on your church\'s calendar.')

    def get_kanisa_root_crumb(self):
        return {'text': 'Diary',
                'url': reverse('kanisa_manage_diary')}


class DiaryEventIndexView(KanisaTemplateView, DiaryBaseView):
    template_name = 'kanisa/management/diary/index.html'
    kanisa_title = 'Manage Diary'
    kanisa_is_root_view = True


class DiaryRegularEventsView(KanisaListView, DiaryBaseView):
    model = RegularEvent
    template_name = 'kanisa/management/diary/regular_events.html'
    kanisa_title = 'Manage Regular Events'


class DiaryCreateView(KanisaCreateView, DiaryBaseView):
    form_class = RegularEventForm
    template_name = 'kanisa/management/create.html'
    kanisa_title = 'Create a Regular Event'

    def get_success_url(self):
        return reverse('kanisa_manage_diary')

    def get_initial(self):
        initial = super(DiaryCreateView, self).get_initial()
        initial['start_time'] = time(9, 0, 0)
        return initial


class DiaryUpdateView(KanisaUpdateView, DiaryBaseView):
    form_class = RegularEventForm
    template_name = 'kanisa/management/create.html'
    model = RegularEvent

    def get_kanisa_title(self):
        return 'Edit Event: %s' % unicode(self.object)

    def get_success_url(self):
        return reverse('kanisa.views.manage_diary')
