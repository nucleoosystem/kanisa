from django import template
from django.contrib.auth.models import Permission
from django.core.cache import cache
from kanisa.utils.auth import has_any_kanisa_permission


register = template.Library()


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


@register.assignment_tag(takes_context=True)
def kanisa_is_permissioned_user(context):
    if 'user' not in context:
        return False

    return has_any_kanisa_permission(context['user'])


@register.filter
def get_range(value):
    """
    From http://djangosnippets.org/snippets/1357/

    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
    <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
    <li>0. Do something</li>
    <li>1. Do something</li>
    <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)
