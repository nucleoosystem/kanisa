from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy
from kanisa.models import Document
from kanisa.views.generic import KanisaTemplateView
import tweepy


class SocialBaseView:
    kanisa_lead = ('Having a presence on social networks allows your Church '
                   'to communicate with people it might not otherwise reach.')
    kanisa_root_crumb = {'text': 'Social',
                         'url': reverse_lazy('kanisa_manage_social')}


def get_tweepy_handle(request):
    required_attrs = ['TWITTER_CONSUMER_KEY',
                      'TWITTER_CONSUMER_SECRET',
                      'TWITTER_ACCESS_TOKEN',
                      'TWITTER_ACCESS_TOKEN_SECRET', ]

    for attr in required_attrs:
        if not hasattr(settings, attr):
            required_bits = ', '.join(required_attrs)
            msg = ('Cannot connect to Twitter. '
                   'Please ensure you have all '
                   'the following settings: %s.') % required_bits
            messages.info(request, msg)
            return None

    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                               settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                          settings.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        user = api.verify_credentials()

        if user:
            return user
        messages.warning(request, 'Your Twitter credentials are invalid.')
    except tweepy.TweepError:
        messages.warning(request, 'Twitter appears to be unreachable.')

    return None


class SocialIndexView(KanisaTemplateView, SocialBaseView):
    template_name = 'kanisa/management/social/index.html'
    kanisa_title = 'Manage Social Networks'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(SocialIndexView,
                        self).get_context_data(**kwargs)

        twitter = cache.get('twitter_handle')

        if not twitter:
            twitter = get_tweepy_handle(self.request)
            cache.set('twitter_handle', twitter, 120)

        if twitter:
            context['twitter_username'] = twitter.screen_name
            context['followers'] = twitter.followers_count
            context['statuses'] = twitter.statuses_count
            context['current_status'] = twitter.status

        return context
