from django import template
from django.core.cache import cache
from django.template.loader import render_to_string
from kanisa.models import ScheduledEvent, Sermon, Block
from kanisa.utils.diary import get_week_bounds


register = template.Library()


@register.assignment_tag
def kanisa_this_sunday():
    monday, sunday = get_week_bounds()

    events = ScheduledEvent.objects.filter(date=sunday)

    return events


@register.assignment_tag
def kanisa_sermons():
    return Sermon.preached_objects.all()[:5]


def get_block(slug):
    try:
        block = Block.objects.get(slug=slug)
        if not block.contents:
            return None
        else:
            return block
    except Block.DoesNotExist:
        return None


@register.simple_tag(takes_context=True)
def kanisa_content_block(context, slug):
    cache_key = 'kanisa_content_block:%s' % slug

    block = cache.get(cache_key)

    if block is None:
        block = get_block(slug)

        if block is not None:
            cache.set(cache_key, block)

    if context['user'].has_perm('kanisa.manage_blocks'):
        tmpl = 'kanisa/management/blocks/_fragment_editable.html'
        return render_to_string(tmpl,
                                {'block': block, 'slug': slug})

    return render_to_string('kanisa/management/blocks/_fragment_display.html',
                            {'block': block})
