from django import template
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag(takes_context=True)
def kanisa_facebook_like_widget(context):
    return render_to_string(
        'kanisa/public/_facebook_like.html',
        {'url': context['request'].build_absolute_uri()}
    )
