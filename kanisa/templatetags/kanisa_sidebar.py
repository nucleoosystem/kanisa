from django import template
from django.contrib.auth import get_user_model
from django.core.cache import cache


register = template.Library()


@register.assignment_tag
def kanisa_inactive_users():
    cached = cache.get('kanisa_inactive_users')

    if cached is not None:
        return cached

    users = get_user_model().objects.all().filter(is_active=False).count()
    cache.set('kanisa_inactive_users', users, 120)

    return users
