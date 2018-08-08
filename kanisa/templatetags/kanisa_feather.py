from django import template
from django.template.loader import render_to_string


register = template.Library()


@register.inclusion_tag('kanisa/public/_feather.html')
def kanisa_feather(icon, title=None, klass=None):
    if title is None:
        title = ""
    if klass is None:
        klass = "feather"

    return {
        'icon': icon,
        'title': title,
        'class': klass,
    }
