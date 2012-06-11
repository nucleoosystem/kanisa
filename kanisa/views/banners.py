from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


from kanisa.models.banners import Banner
from kanisa.views.generic import (KanisaCreateView, KanisaUpdateView,
                                  KanisaListView)
from kanisa.forms import BannerForm


class BannerBaseView:
    kanisa_lead = ('Banners are a high-impact way of advertising content or '
                   'events for your site.')


class BannerManagementView(KanisaListView, BannerBaseView):
    model = Banner
    queryset = Banner.active_objects.all()
    template_name = 'kanisa/management/banners/index.html'
    context_object_name = 'banners'


class InactiveBannerManagementView(KanisaListView, BannerBaseView):
    model = Banner
    queryset = Banner.inactive_objects.all()
    template_name = 'kanisa/management/banners/inactive.html'
    context_object_name = 'banners'


class BannerCreateView(KanisaCreateView, BannerBaseView):
    form_class = BannerForm
    template_name = 'kanisa/management/banners/create.html'
    kanisa_title = 'Create Banner'

    def get_success_url(self):
        return reverse('kanisa_manage_banners')


class BannerUpdateView(KanisaUpdateView, BannerBaseView):
    form_class = BannerForm
    template_name = 'kanisa/management/banners/create.html'
    model = Banner

    def get_kanisa_title(self):
        return 'Edit Banner: %s' % unicode(self.object)

    def get_success_url(self):
        if self.object.active():
            return reverse('kanisa_manage_banners')
        return reverse('kanisa_manage_inactive_banners')


@staff_member_required
def retire_banner(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    banner.set_retired()

    message = u'Banner "%s" retired.' % unicode(banner)
    messages.success(request, message)

    return HttpResponseRedirect(reverse('kanisa_manage_banners'))
