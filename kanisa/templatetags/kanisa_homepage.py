from django import template
from django.core.cache import cache
from kanisa.models import ScheduledEvent, Sermon
from kanisa.utils.diary import get_week_bounds
from kanisa.utils.social import get_tweepy_handle, TwitterException


register = template.Library()


@register.assignment_tag
def kanisa_this_sunday():
    monday, sunday = get_week_bounds()

    events = ScheduledEvent.objects.filter(date=sunday)

    return events


@register.assignment_tag
def kanisa_sermons():
    return Sermon.objects.all()[:5]


@register.assignment_tag
def kanisa_twitter_status():
    twitter = cache.get('twitter_handle')

    try:
        if not twitter:
            api = get_tweepy_handle()
            twitter = api.me()
            cache.set('twitter_handle', twitter, 120)

        return twitter.status
    except TwitterException:
        return None


@register.assignment_tag
def kanisa_twitter_username():
    twitter = cache.get('twitter_handle')

    try:
        if not twitter:
            api = get_tweepy_handle()
            twitter = api.me()
            cache.set('twitter_handle', twitter, 120)

        return twitter.screen_name
    except TwitterException:
        return None
