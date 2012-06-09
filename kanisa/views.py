from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from kanisa.models.banners import Banner
from kanisa.forms import BannerCreationForm


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


@staff_member_required
def manage_banners(request):
    banners = Banner.active_objects.all()

    return render_to_response('kanisa/management/banners/index.html',
                              {'banners': banners},
                              context_instance=RequestContext(request))


@staff_member_required
def create_banner(request):
    if request.method == 'POST':
        form = BannerCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('kanisa.views.manage_banners'))
    else:
        form = BannerCreationForm()
    
    return render_to_response('kanisa/management/banners/create.html',
                              {'form': form},
                              context_instance=RequestContext(request))


@staff_member_required
def retire_banner(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    banner.set_retired()

    message = u'Banner "%s" retired.' % unicode(banner)
    messages.success(request, message)

    return HttpResponseRedirect(reverse('kanisa.views.manage_banners'))
