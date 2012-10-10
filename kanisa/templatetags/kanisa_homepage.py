from django import template
from kanisa.models import ScheduledEvent
from kanisa.utils.diary import get_week_bounds


register = template.Library()


@register.assignment_tag
def kanisa_this_sunday():
    monday, sunday = get_week_bounds()

    events = ScheduledEvent.objects.filter(date=sunday)

    return events
