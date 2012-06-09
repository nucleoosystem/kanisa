from kanisa.views.banners import (manage_banners, manage_inactive_banners,
                                  retire_banner)
from kanisa.views.diary import manage_diary
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from kanisa.models.banners import Banner


def index(request):
    banners = Banner.active_objects.all()

    return render_to_response('kanisa/index.html',
                              {'banners': banners},
                              context_instance=RequestContext(request))


@staff_member_required
def manage(request):
    return render_to_response('kanisa/management/index.html',
                              {},
                              context_instance=RequestContext(request))
