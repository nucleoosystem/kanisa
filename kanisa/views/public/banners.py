from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from kanisa.models import Banner


class VisitBannerView(RedirectView):
    permanent = False

    def get_redirect_url(self, banner_id):
        banner = get_object_or_404(Banner, pk=banner_id)

        if not banner.url:
            raise Http404

        banner.visits = F('visits') + 1
        banner.save()

        return banner.url
