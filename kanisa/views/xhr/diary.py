from datetime import datetime
from django.db.models import Q
from django.http import (HttpResponse,
                         HttpResponseBadRequest)
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse

from kanisa.models import RegularEvent, ScheduledEvent
from kanisa.utils.diary import get_schedule, get_this_week
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


class DiaryGetWeekPublic(XHRBaseGetView):
    required_arguments = ['start_date', ]
    permission = None

    def get_date(self, request, *args, **kwargs):
        date = request.GET['start_date']
        try:
            return datetime.strptime(date, '%Y%m%d').date()
        except ValueError:
            raise BadArgument("Invalid date '%s' provided."
                              % date)

    def render(self, request, *args, **kwargs):
        thedate = self.get_date(request, *args, **kwargs)

        tmpl = 'kanisa/public/diary/_this_week_table.html'
        return render_to_response(tmpl,
                                  {'thisweek': get_this_week(thedate)},
                                  context_instance=RequestContext(request))
get_week_public_view = DiaryGetWeekPublic.as_view()


class ScheduledEventFindView(XHRBasePostView):
    permission = 'kanisa.manage_diary'
    required_arguments = ['event_name', 'event_date', ]

    def render(self, request, *args, **kwargs):
        event_name = self.arguments['event_name']
        event_date = self.arguments['event_date']

        by_title = Q(title__icontains=event_name)
        by_event_title = Q(event__title__icontains=event_name)
        events = ScheduledEvent.objects.filter(
            by_title | by_event_title
        ).order_by('-date')[:5]

        ctx = {
            'events': events,
            'event_name': event_name,
            'event_date': event_date,
        }

        return TemplateResponse(
            request,
            'kanisa/management/diary/xhr_events.html',
            ctx
        )
diary_scheduled_event_find = ScheduledEventFindView.as_view()
