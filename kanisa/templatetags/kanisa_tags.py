from django import template
from kanisa.models import Banner


register = template.Library()


@register.simple_tag()
def kanisa_active_banners():
    return Banner.active_objects.count()
