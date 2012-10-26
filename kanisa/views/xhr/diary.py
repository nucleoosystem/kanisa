from datetime import datetime
from django.http import (HttpResponse,
                         HttpResponseBadRequest)
from django.shortcuts import render_to_response
from django.template import RequestContext

from kanisa.models import RegularEvent, EventCategory
from kanisa.utils.diary import get_schedule
from kanisa.views.xhr.base import XHRBasePostView, XHRBaseGetView, BadArgument


class ScheduleRegularEventView(XHRBasePostView):
    required_arguments = ['event', 'date', ]
    permission = 'kanisa.manage_diary'

    def get_date(self):
        try:
            event_date = datetime.strptime(self.arguments['date'], '%Y%m%d')
            return event_date
        except ValueError:
            given = self.arguments['date']
            raise BadArgument("'%s' is not a valid date." % given)

    def get_event(self):
        try:
            event_pk = int(self.arguments['event'])
            return RegularEvent.objects.get(pk=event_pk)
        except (RegularEvent.DoesNotExist, ValueError):
            raise BadArgument("No event found with ID '%s'."
                              % self.arguments['event'])

    def render(self, request, *args, **kwargs):
        event_date = self.get_date()
        event = self.get_event()

        try:
            event.schedule_once(event_date)
            return HttpResponse("Event scheduled.")
        except event.AlreadyScheduled:
            return HttpResponseBadRequest("That event is already scheduled.")
schedule_regular_events = ScheduleRegularEventView.as_view()


class DiaryGetSchedule(XHRBaseGetView):
    permission = 'kanisa.manage_diary'

    def get_date(self, request, *args, **kwargs):
        date = kwargs['date']
        try:
            return datetime.strptime(date, '%Y%m%d').date()
        except ValueError:
            raise BadArgument("Invalid date '%s' provided."
                              % date)

    def render(self, request, *args, **kwargs):
        thedate = self.get_date(request, *args, **kwargs)
        schedule = get_schedule(thedate)

        tmpl = 'kanisa/management/diary/_diary_page.html'
        return render_to_response(tmpl,
                                  {'calendar': schedule.calendar_entries},
                                  context_instance=RequestContext(request))
get_schedule_view = DiaryGetSchedule.as_view()


class DiaryGetRegularEvents(XHRBaseGetView):
    permission = None
    required_arguments = ['category', ]

    def get_category(self, category_key):
        try:
            category = int(category_key)
        except ValueError:
            raise BadArgument("Bad category value '%s' provided."
                              % category_key)

        if category == 0:
            return None

        try:
            return EventCategory.objects.get(pk=category)
        except EventCategory.DoesNotExist:
            raise BadArgument("Non-existent category value provided.")

    def render(self, request, *args, **kwargs):
        category = self.get_category(request.GET['category'])

        if category is None:
            events = RegularEvent.objects.all()
        else:
            events = category.regularevent_set.all()

        tmpl = 'kanisa/public/diary/_regular_event_list.html'
        return render_to_response(tmpl,
                                  {'events': events},
                                  context_instance=RequestContext(request))
get_regular_events_view = DiaryGetRegularEvents.as_view()
