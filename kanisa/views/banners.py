from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from kanisa.models.banners import Banner
from kanisa.views.generic import (KanisaCreateView, KanisaUpdateView,
                                  KanisaListView)
from kanisa.forms import BannerForm


class BannerBaseView:
    kanisa_lead = ('Banners are a high-impact way of advertising content or '
                   'events for your site.')

    def get_kanisa_root_crumb(self):
        return {'text': 'Banners',
                'url': reverse('kanisa_manage_banners')}


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


class RetireBannerView(RedirectView):
    permanent = False

    def get_redirect_url(self, banner_id):
        banner = get_object_or_404(Banner, pk=banner_id)
        banner.set_retired()

        message = u'Banner "%s" retired.' % unicode(banner)
        messages.success(self.request, message)

        return reverse('kanisa_manage_banners')
