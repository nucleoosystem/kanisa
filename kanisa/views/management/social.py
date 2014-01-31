from constance import config
from datetime import time
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.base import RedirectView
import tweepy
from kanisa.forms.social import ScheduledTweetForm
from kanisa.models import ScheduledTweet
from kanisa.utils.social import (
    TwitterException,
    post_to_twitter,
    get_cached_twitter_handle,
    delete_cached_twitter_handle,
    get_authorisation_url
)
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaTemplateView,
    KanisaCreateView,
    KanisaUpdateView,
    KanisaDeleteView,
    KanisaListView
)


class SocialBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Having a presence on social networks allows your Church '
                   'to communicate with people it might not otherwise reach.')
    kanisa_root_crumb = {'text': 'Social',
                         'url': reverse_lazy('kanisa_manage_social')}
    permission = 'kanisa.manage_social'
    kanisa_nav_component = 'social'

    def get_twitter_context(self):
        context = {}

        if not config.TWITTER_ACCESS_TOKEN or not config.TWITTER_ACCESS_SECRET:
            try:
                context['redirect_url'] = get_authorisation_url(self.request)
            except tweepy.TweepError as e:
                context['error'] = e
            return context

        try:
            twitter = get_cached_twitter_handle()
            context['twitter_username'] = twitter.screen_name
            context['followers'] = twitter.followers_count
            context['statuses'] = twitter.statuses_count
            context['current_status'] = twitter.status
        except TwitterException, e:
            context['twitter_status'] = e.value

        return context


class SocialIndexView(SocialBaseView, KanisaTemplateView):
    template_name = 'kanisa/management/social/index.html'
    kanisa_title = 'Manage Social Networks'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(SocialIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_twitter_context())
        return context
social_management = SocialIndexView.as_view()


class TwitterAuthVerifyView(SocialBaseView, RedirectView):
    permanent = False

    def get_redirect_url(self):
        if 'denied' in self.request.GET:
            messages.error(
                self.request,
                ("You denied Kanisa permission to post to Twitter, please try "
                 "again.")
            )
            return reverse('kanisa_manage_social_twitter')

        if 'oauth_verifier' in self.request.GET:
            verifier = self.request.GET['oauth_verifier']
            auth = tweepy.OAuthHandler(
                settings.TWITTER_CONSUMER_KEY,
                settings.TWITTER_CONSUMER_SECRET
            )
            token = self.request.session['request_token']
            del self.request.session['request_token']
            auth.set_request_token(token[0], token[1])

            try:
                auth.get_access_token(verifier)
            except tweepy.TweepError:
                messages.error(
                    self.request,
                    "Failed to get an authentication token from Twitter."
                )
                return reverse('kanisa_manage_social_twitter')

            config.TWITTER_ACCESS_TOKEN = auth.access_token.key
            config.TWITTER_ACCESS_SECRET = auth.access_token.secret

            messages.success(
                self.request,
                "Kanisa can now post to Twitter for you."
            )
            return reverse('kanisa_manage_social_twitter')

        messages.error(
            self.request,
            ("Error authorising Kanisa - an unexpected response was received "
             "from Twitter.")
        )

        return reverse('kanisa_manage_social_twitter')
twitter_auth_verify = TwitterAuthVerifyView.as_view()


class TwitterDeauthoriseView(SocialBaseView, RedirectView):
    permanent = False

    def get_redirect_url(self):
        config.TWITTER_ACCESS_TOKEN = ''
        config.TWITTER_ACCESS_SECRET = ''
        delete_cached_twitter_handle()
        return reverse('kanisa_manage_social_twitter')
twitter_deauth = TwitterDeauthoriseView.as_view()


class SocialTwitterIndexView(SocialBaseView, KanisaListView):
    kanisa_title = 'Manage Twitter'
    queryset = ScheduledTweet.future_objects.all
    template_name = 'kanisa/management/social/twitter.html'

    def get_context_data(self, **kwargs):
        context = super(SocialTwitterIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_twitter_context())
        return context
twitter_management = SocialTwitterIndexView.as_view()


class ScheduledTweetCreateView(SocialBaseView, KanisaCreateView):
    form_class = ScheduledTweetForm
    kanisa_title = 'Schedule Tweet'
    success_url = reverse_lazy('kanisa_manage_social_twitter')

    def get_initial(self):
        initial = super(ScheduledTweetCreateView, self).get_initial()
        initial['time'] = time(17, 0, 0)
        return initial
scheduled_tweet_create = ScheduledTweetCreateView.as_view()


class ScheduledTweetUpdateView(SocialBaseView, KanisaUpdateView):
    form_class = ScheduledTweetForm
    queryset = ScheduledTweet.future_objects.all()
    success_url = reverse_lazy('kanisa_manage_social_twitter')
    kanisa_title = 'Edit Scheduled Tweet'
scheduled_tweet_update = ScheduledTweetUpdateView.as_view()


class ScheduledTweetDeleteView(SocialBaseView, KanisaDeleteView):
    queryset = ScheduledTweet.future_objects.all()
    kanisa_title = 'Delete Scheduled Tweet'

    def get_cancel_url(self):
        return reverse('kanisa_manage_social_twitter')

    def get_success_url(self):
        messages.success(self.request, 'Tweet deleted')
        return reverse('kanisa_manage_social_twitter')

    def get_deletion_confirmation_message(self):
        return 'Are you sure you want to delete this tweet?'

    def get_extra_context(self):
        return self.object

    def get_deletion_button_title(self):
        return 'Yes, delete this tweet'
scheduled_tweet_delete = ScheduledTweetDeleteView.as_view()


class SocialTwitterPostView(SocialBaseView, RedirectView):
    permanent = False

    def get_redirect_url(self):
        twitter_status = self.request.POST.get('twitter-status', None)

        if not twitter_status:
            messages.error(self.request, "You must enter a Twitter status.")
            return reverse('kanisa_manage_social')

        try:
            post_to_twitter(twitter_status)
        except TwitterException, e:
            messages.error(self.request, "Error posting tweet: %s" % e.value)
            return reverse('kanisa_manage_social')

        message = 'Tweet posted.'
        messages.success(self.request, message)

        return reverse('kanisa_manage_social')
twitter_post = SocialTwitterPostView.as_view()
