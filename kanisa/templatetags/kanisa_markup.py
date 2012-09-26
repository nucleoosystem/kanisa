from django import template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.filter(is_safe=True)
def kanisa_markdown(value):
    return mark_safe(markdown.markdown(force_unicode(value),
                                       extensions=['nl2br', ]))
