from django import template
from kanisa.models import Banner, ScheduledTweet


register = template.Library()


@register.simple_tag()
def kanisa_active_banners():
    return Banner.active_objects.count()


@register.simple_tag()
def kanisa_future_scheduled_tweets():
    return ScheduledTweet.future_objects.count()


@register.simple_tag(takes_context=True)
def kanisa_user_has_perm(context, perm):
    user = context['theuser']
    input = '<input %s/>'

    attributes = {}
    attributes['type'] = 'checkbox'
    attributes['data-permission-id'] = perm
    attributes['data-user-id'] = user.pk
    attributes['class'] = 'kanisa_user_perm'

    if user.is_superuser:
        attributes['disabled'] = 'disabled'
        attributes['checked'] = 'checked'

    if user.has_perm(perm):
        attributes['checked'] = 'checked'

    html_attr = ['%s="%s"' % (k, v) for k, v in attributes.items()]

    return input % ' '.join(html_attr)
