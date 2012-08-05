from django.conf import settings
import tweepy


class TwitterException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


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
            raise TwitterException(msg)

    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                               settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                          settings.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        user = api.verify_credentials()

        if user:
            return api
        raise TwitterException('Your Twitter authentication credentials are '
                               'invalid.')
    except tweepy.TweepError:
        raise TwitterException('Twitter appears to be unreachable.')
