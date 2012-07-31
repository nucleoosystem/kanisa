from django import template
from django.contrib.auth.models import Permission
from django.core.cache import cache
from kanisa.models import Banner, ScheduledTweet


register = template.Library()


@register.simple_tag()
def kanisa_active_banners():
    return Banner.active_objects.count()


@register.simple_tag()
def kanisa_future_scheduled_tweets():
    return ScheduledTweet.future_objects.count()


def __cache_all_perms():
    all_perms = Permission.objects.filter(content_type__app_label='kanisa')
    for perm in all_perms:
        cache.set('kanisa_perms_name:%s' % perm.codename, perm.name)


def __get_help_text(perm_text):
    app, perm_code = perm_text.split('.')
    cache_key = 'kanisa_perms_name:%s' % perm_code

    if not cache.get(cache_key):
        __cache_all_perms()

    return cache.get(cache_key)


@register.simple_tag(takes_context=True)
def kanisa_user_has_perm(context, perm):
    user = context['theuser']
    input = '<input %s/>'

    attributes = {}
    attributes['type'] = 'checkbox'
    attributes['data-permission-id'] = perm
    attributes['data-user-id'] = user.pk
    attributes['class'] = 'kanisa_user_perm'

    attributes['title'] = __get_help_text(perm)

    if user.is_superuser:
        attributes['disabled'] = 'disabled'
        attributes['checked'] = 'checked'

    if user.has_perm(perm):
        attributes['checked'] = 'checked'

    html_attr = ['%s="%s"' % (k, v) for k, v in attributes.items()]

    return input % ' '.join(html_attr)
