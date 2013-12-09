from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from kanisa.models import Banner
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaCreateView,
                                  KanisaUpdateView,
                                  KanisaListView)
from kanisa.forms.banners import BannerForm


class BannerBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Banners are the images that scroll across the home page, '
                   'and are a high-impact way of advertising content or '
                   'events for your site.')
    kanisa_root_crumb = {'text': 'Banners',
                         'url': reverse_lazy('kanisa_manage_banners')}
    permission = 'kanisa.manage_banners'
    kanisa_nav_component = 'banners'


class BannerManagementView(BannerBaseView,
                           KanisaListView):
    model = Banner
    queryset = Banner.active_objects.all()
    template_name = 'kanisa/management/banners/index.html'
    kanisa_title = 'Manage Banners'
    kanisa_is_root_view = True
banner_management = BannerManagementView.as_view()


class InactiveBannerManagementView(BannerBaseView,
                                   KanisaListView):
    model = Banner
    queryset = Banner.inactive_objects.all()
    template_name = 'kanisa/management/banners/inactive.html'
    kanisa_title = 'Manage Inactive Banners'
banner_inactive_management = InactiveBannerManagementView.as_view()


class BannerCreateView(BannerBaseView,
                       KanisaCreateView):
    form_class = BannerForm
    kanisa_title = 'Create Banner'
    success_url = reverse_lazy('kanisa_manage_banners')
banner_create = BannerCreateView.as_view()


class BannerUpdateView(BannerBaseView,
                       KanisaUpdateView):
    form_class = BannerForm
    model = Banner

    def get_success_url(self):
        if self.object.active():
            return reverse('kanisa_manage_banners')
        return reverse('kanisa_manage_banners_inactive')
banner_update = BannerUpdateView.as_view()


class RetireBannerView(BannerBaseView,
                       RedirectView):
    permanent = False

    def get_redirect_url(self, banner_id):
        banner = get_object_or_404(Banner, pk=banner_id)
        banner.set_retired()

        message = 'Banner "%s" retired.' % unicode(banner)
        messages.success(self.request, message)

        return reverse('kanisa_manage_banners')
banner_retire = RetireBannerView.as_view()
