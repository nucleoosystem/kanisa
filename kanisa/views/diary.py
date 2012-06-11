from datetime import time
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext


from kanisa.forms import RegularEventForm
from kanisa.models import RegularEvent
from kanisa.views.generic import (KanisaCreateView, KanisaUpdateView,
                                  KanisaListView)


@staff_member_required
def manage_diary(request):
    return render_to_response('kanisa/management/diary/index.html',
                              {},
                              context_instance=RequestContext(request))


class DiaryBaseView:
    kanisa_lead = ('Diary events are regularly occurring events you want to '
                   'display on your church\'s calendar.')


class DiaryRegularEventsView(KanisaListView, DiaryBaseView):
    model = RegularEvent
    template_name = 'kanisa/management/diary/regular_events.html'
    kanisa_title = 'Manage Regular Events'


class DiaryCreateView(KanisaCreateView, DiaryBaseView):
    form_class = RegularEventForm
    template_name = 'kanisa/management/diary/create.html'
    kanisa_title = 'Create a Regular Event'

    def get_success_url(self):
        return reverse('kanisa_manage_diary')

    def get_initial(self):
        initial = super(DiaryCreateView, self).get_initial()
        initial['start_time'] = time(9, 0, 0)
        return initial


class DiaryUpdateView(KanisaUpdateView, DiaryBaseView):
    form_class = RegularEventForm
    template_name = 'kanisa/management/diary/create.html'
    model = RegularEvent

    def get_kanisa_title(self):
        return 'Edit Event: %s' % unicode(self.object)

    def get_success_url(self):
        return reverse('kanisa.views.manage_diary')
