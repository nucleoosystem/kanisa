from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.base import RedirectView
from kanisa.models import Document
from kanisa.utils import get_tweepy_handle
from kanisa.views.generic import KanisaTemplateView


class SocialBaseView:
    kanisa_lead = ('Having a presence on social networks allows your Church '
                   'to communicate with people it might not otherwise reach.')
    kanisa_root_crumb = {'text': 'Social',
                         'url': reverse_lazy('kanisa_manage_social')}


class SocialIndexView(KanisaTemplateView, SocialBaseView):
    template_name = 'kanisa/management/social/index.html'
    kanisa_title = 'Manage Social Networks'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(SocialIndexView,
                        self).get_context_data(**kwargs)

        twitter = cache.get('twitter_handle')

        if not twitter:
            api = get_tweepy_handle(self.request)
            if api:
                twitter = api.me()
                cache.set('twitter_handle', twitter, 120)

        if twitter:
            context['twitter_username'] = twitter.screen_name
            context['followers'] = twitter.followers_count
            context['statuses'] = twitter.statuses_count
            context['current_status'] = twitter.status

        return context


class SocialTwitterPostView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        twitter = get_tweepy_handle(self.request)

        if not twitter:
            messages.error(self.request, "No active Twitter connection available.")
            return reverse('kanisa_manage_social')

        if 'twitter-status' not in self.request.POST:
            messages.error(self.request, "You must enter a Twitter status.")
            return reverse('kanisa_manage_social')

        twitter_status = self.request.POST['twitter-status']

        if not twitter_status:
            messages.error(self.request, "You must enter a Twitter status.")
            return reverse('kanisa_manage_social')

        twitter.update_status(twitter_status)

        message = 'Tweet posted.'
        messages.success(self.request, message)

        cache.delete('twitter_handle')

        return reverse('kanisa_manage_social')
