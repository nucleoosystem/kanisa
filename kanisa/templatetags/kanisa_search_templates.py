from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def search_template(value):
    return u'kanisa/management/search/results/{0}.html'.format(value)
