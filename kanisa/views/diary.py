from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext


from kanisa.forms import DiaryForm
from kanisa.models import DiaryEvent
from kanisa.views.generic import KanisaCreateView, KanisaUpdateView


@staff_member_required
def manage_diary(request):
    events = DiaryEvent.objects.all()
    return render_to_response('kanisa/management/diary/index.html',
                              {'events': events},
                              context_instance=RequestContext(request))


class DiaryCreateView(KanisaCreateView):
    form_class = DiaryForm
    template_name = 'kanisa/management/diary/create.html'

    def get_success_url(self):
        return reverse('kanisa.views.manage_diary')


class DiaryUpdateView(KanisaUpdateView):
    form_class = DiaryForm
    template_name = 'kanisa/management/diary/create.html'
    model = DiaryEvent

    def get_success_url(self):
        return reverse('kanisa.views.manage_diary')
