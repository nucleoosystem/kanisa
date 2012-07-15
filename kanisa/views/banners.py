from django.contrib import messages
from django.db.models import F
from django.http import Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from kanisa.models import Banner
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaCreateView, KanisaUpdateView,
                                  KanisaListView)
from kanisa.forms import BannerForm


class BannerBaseView:
    kanisa_lead = ('Banners are a high-impact way of advertising content or '
                   'events for your site.')
    kanisa_root_crumb = {'text': 'Banners',
                         'url': reverse_lazy('kanisa_manage_banners')}


class BannerManagementView(KanisaAuthorizationMixin,
                           KanisaListView, BannerBaseView):
    model = Banner
    queryset = Banner.active_objects.all()
    template_name = 'kanisa/management/banners/index.html'
    kanisa_title = 'Manage Banners'
    kanisa_is_root_view = True


class InactiveBannerManagementView(KanisaAuthorizationMixin,
                                   KanisaListView, BannerBaseView):
    model = Banner
    queryset = Banner.inactive_objects.all()
    template_name = 'kanisa/management/banners/inactive.html'
    kanisa_title = 'Manage Inactive Banners'


class BannerCreateView(KanisaAuthorizationMixin,
                       KanisaCreateView, BannerBaseView):
    form_class = BannerForm
    kanisa_title = 'Create Banner'
    success_url = reverse_lazy('kanisa_manage_banners')


class BannerUpdateView(KanisaAuthorizationMixin,
                       KanisaUpdateView, BannerBaseView):
    form_class = BannerForm
    model = Banner

    def get_success_url(self):
        if self.object.active():
            return reverse('kanisa_manage_banners')
        return reverse('kanisa_manage_banners_inactive')


class RetireBannerView(KanisaAuthorizationMixin,
                       RedirectView):
    permanent = False

    def get_redirect_url(self, banner_id):
        banner = get_object_or_404(Banner, pk=banner_id)
        banner.set_retired()

        message = u'Banner "%s" retired.' % unicode(banner)
        messages.success(self.request, message)

        return reverse('kanisa_manage_banners')


class VisitBannerView(RedirectView):
    permanent = False

    def get_redirect_url(self, banner_id):
        banner = get_object_or_404(Banner, pk=banner_id)

        if not banner.url:
            raise Http404

        banner.visits = F('visits') + 1
        banner.save()

        return banner.url
