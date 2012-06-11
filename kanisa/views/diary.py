from datetime import time
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext


from kanisa.forms import RegularEventForm
from kanisa.models import RegularEvent
from kanisa.views.generic import KanisaCreateView, KanisaUpdateView


@staff_member_required
def manage_diary(request):
    events = RegularEvent.objects.all()
    return render_to_response('kanisa/management/diary/index.html',
                              {'events': events},
                              context_instance=RequestContext(request))


class DiaryCreateView(KanisaCreateView):
    form_class = RegularEventForm
    template_name = 'kanisa/management/diary/create.html'

    def get_success_url(self):
        return reverse('kanisa.views.manage_diary')

    def get_initial(self):
        initial = super(DiaryCreateView, self).get_initial()
        initial['start_time'] = time(9, 0, 0)
        return initial


class DiaryUpdateView(KanisaUpdateView):
    form_class = RegularEventForm
    template_name = 'kanisa/management/diary/create.html'
    model = RegularEvent

    def get_success_url(self):
        return reverse('kanisa.views.manage_diary')
