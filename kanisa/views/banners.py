from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


from kanisa.models.banners import Banner
from kanisa.views.generic import KanisaCreateView
from kanisa.forms import BannerForm


@staff_member_required
def manage_banners(request):
    banners = Banner.active_objects.all()

    return render_to_response('kanisa/management/banners/index.html',
                              {'banners': banners},
                              context_instance=RequestContext(request))


@staff_member_required
def manage_inactive_banners(request):
    banners = Banner.inactive_objects.all()

    return render_to_response('kanisa/management/banners/inactive.html',
                              {'banners': banners},
                              context_instance=RequestContext(request))


class BannerCreateView(KanisaCreateView):
    form_class = BannerForm
    template_name = 'kanisa/management/banners/create.html'

    def get_success_url(self):
        return reverse('kanisa.views.manage_banners')


@staff_member_required
def edit_banner(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)

    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            message = u'Banner "%s" saved.' % unicode(banner)
            messages.success(request, message)

            return HttpResponseRedirect(reverse('kanisa.views.manage_banners'))
    else:
        form = BannerForm(instance=banner)

    return render_to_response('kanisa/management/banners/create.html',
                              {'form': form, 'banner': banner, },
                              context_instance=RequestContext(request))


@staff_member_required
def retire_banner(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    banner.set_retired()

    message = u'Banner "%s" retired.' % unicode(banner)
    messages.success(request, message)

    return HttpResponseRedirect(reverse('kanisa.views.manage_banners'))
