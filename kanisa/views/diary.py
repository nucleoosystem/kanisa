from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from kanisa.models import DiaryEvent


@staff_member_required
def manage_diary(request):
    events = DiaryEvent.objects.all()
    return render_to_response('kanisa/management/diary/index.html',
                              {'events': events},
                              context_instance=RequestContext(request))
