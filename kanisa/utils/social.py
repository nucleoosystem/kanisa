from constance import config
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
import logging
import tweepy


logger = logging.getLogger(__name__)


class TwitterException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_tweepy_handle():
    required_attrs = ['TWITTER_CONSUMER_KEY',
                      'TWITTER_CONSUMER_SECRET']

    for attr in required_attrs:
        if not hasattr(settings, attr):
            required_bits = ', '.join(required_attrs)
            msg = ('Cannot connect to Twitter. '
                   'Please ensure you have all '
                   'the following settings: %s.') % required_bits
            raise TwitterException(msg)

        if not config.TWITTER_ACCESS_TOKEN or not config.TWITTER_ACCESS_SECRET:
            msg = ('Cannot connect to Twitter. '
                   'You need to authorise Kanisa to post on your behalf.')
            raise TwitterException(msg)

    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                               settings.TWITTER_CONSUMER_SECRET)

    auth.set_access_token(config.TWITTER_ACCESS_TOKEN,
                          config.TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)

    try:
        user = api.verify_credentials()

        if user:
            return api
        raise TwitterException('Your Twitter authentication credentials are '
                               'invalid.')
    except tweepy.TweepError as e:
        logger.error(e, exc_info=True)
        raise TwitterException('Twitter appears to be unreachable.')


def get_cached_twitter_handle():
    twitter = cache.get('twitter_handle')

    if not twitter:
        api = get_tweepy_handle()
        twitter = api.me()
        cache.set('twitter_handle', twitter, 120)

    return twitter


def delete_cached_twitter_handle():
    cache.delete('twitter_handle')


def post_to_twitter(status):
    twitter = get_tweepy_handle()
    twitter.update_status(status)
    delete_cached_twitter_handle()


def get_authorisation_url(request):
    callback_url = reverse('kanisa_manage_social_twitter_auth_verify')
    callback_url = request.build_absolute_uri(callback_url)

    auth = tweepy.OAuthHandler(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        callback_url
    )

    url = auth.get_authorization_url()
    request.session['request_token'] = (auth.request_token.key,
                                        auth.request_token.secret)
    return url
