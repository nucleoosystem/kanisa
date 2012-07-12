from datetime import time
from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.base import RedirectView
from kanisa.forms import ScheduledTweetForm
from kanisa.models import ScheduledTweet
from kanisa.utils import get_tweepy_handle, TwitterException
from kanisa.views.generic import (KanisaTemplateView,
                                  KanisaCreateView,
                                  KanisaUpdateView,
                                  KanisaDeleteView,
                                  KanisaListView)


class SocialBaseView:
    kanisa_lead = ('Having a presence on social networks allows your Church '
                   'to communicate with people it might not otherwise reach.')
    kanisa_root_crumb = {'text': 'Social',
                         'url': reverse_lazy('kanisa_manage_social')}

    def get_twitter_context(self):
        twitter = cache.get('twitter_handle')

        context = {}

        try:
            api = get_tweepy_handle(self.request)
            twitter = api.me()
            cache.set('twitter_handle', twitter, 120)
            context['twitter_username'] = twitter.screen_name
            context['followers'] = twitter.followers_count
            context['statuses'] = twitter.statuses_count
            context['current_status'] = twitter.status
        except TwitterException, e:
            context['twitter_status'] = e.value

        return context


class SocialIndexView(KanisaTemplateView, SocialBaseView):
    template_name = 'kanisa/management/social/index.html'
    kanisa_title = 'Manage Social Networks'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(SocialIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_twitter_context())
        return context


class SocialTwitterIndexView(KanisaListView, SocialBaseView):
    kanisa_title = 'Manage Twitter'
    model = ScheduledTweet
    template_name = 'kanisa/management/social/twitter.html'

    def get_context_data(self, **kwargs):
        context = super(SocialTwitterIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_twitter_context())
        return context


class ScheduledTweetCreateView(KanisaCreateView, SocialBaseView):
    form_class = ScheduledTweetForm
    kanisa_title = 'Schedule Tweet'
    success_url = reverse_lazy('kanisa_manage_social_twitter')

    def get_initial(self):
        initial = super(ScheduledTweetCreateView, self).get_initial()
        initial['time'] = time(17, 0, 0)
        return initial


class ScheduledTweetUpdateView(KanisaUpdateView, SocialBaseView):
    form_class = ScheduledTweetForm
    model = ScheduledTweet
    success_url = reverse_lazy('kanisa_manage_social_twitter')


class ScheduledTweetDeleteView(KanisaDeleteView, SocialBaseView):
    model = ScheduledTweet

    def get_cancel_url(self):
        return reverse('kanisa_manage_social_twitter')

    def get_success_url(self):
        messages.success(self.request, 'Tweet deleted')
        return reverse('kanisa_manage_social_twitter')


class SocialTwitterPostView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        twitter_status = self.request.POST.get('twitter-status', None)

        if not twitter_status:
            messages.error(self.request, "You must enter a Twitter status.")
            return reverse('kanisa_manage_social')

        try:
            twitter = get_tweepy_handle(self.request)
        except TwitterException, e:
            messages.error(self.request, "Error posting tweet: %s" % e.value)
            return reverse('kanisa_manage_social')

        twitter.update_status(twitter_status)

        message = 'Tweet posted.'
        messages.success(self.request, message)

        cache.delete('twitter_handle')
        return reverse('kanisa_manage_social')
