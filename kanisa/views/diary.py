from datetime import date, datetime, time, timedelta

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import formats
from django.views.generic.base import RedirectView

from kanisa.forms import (RegularEventForm, ScheduledEventEditForm,
                          ScheduledEventCreationForm)
from kanisa.models import RegularEvent, ScheduledEvent
from kanisa.utils import get_schedule, get_week_bounds
from kanisa.views.generic import (KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaTemplateView,
                                  KanisaDeleteView,
                                  StaffMemberRequiredMixin)


class DiaryBaseView:
    kanisa_lead = ('Diary events are regularly occurring events you want to '
                   'display on your church\'s calendar.')
    kanisa_root_crumb = {'text': 'Diary',
                         'url': reverse_lazy('kanisa_manage_diary')}

    def date_from_yyymmdd(self):
        yyyymmdd = self.request.GET.get('date', None)
        if not yyyymmdd:
            return date.today()

        try:
            thedate = datetime.strptime(yyyymmdd, '%Y%m%d').date()
        except ValueError:
            return date.today()

        return thedate

    def get_relative_root_url(self, input_date=None):
        path = reverse('kanisa_manage_diary')
        yyyymmdd = self.request.GET.get('date', input_date)

        if not yyyymmdd:
            return path

        return path + '?date=%s' % yyyymmdd


class DiaryEventIndexView(StaffMemberRequiredMixin,
                          KanisaTemplateView, DiaryBaseView):
    template_name = 'kanisa/management/diary/index.html'
    kanisa_title = 'Manage Diary'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        thedate = self.date_from_yyymmdd()

        context = super(DiaryEventIndexView,
                        self).get_context_data(**kwargs)

        schedule = get_schedule(thedate)
        context['previousdate'] = (schedule.monday -
                                   timedelta(days=7)).strftime("%Y%m%d")
        context['nextdate'] = (schedule.monday +
                               timedelta(days=7)).strftime("%Y%m%d")
        context['monday'] = schedule.monday
        context['calendar'] = schedule.calendar_entries
        context['events_to_schedule'] = schedule.events_to_schedule

        return context


class DiaryRegularEventsView(StaffMemberRequiredMixin,
                             KanisaListView, DiaryBaseView):
    model = RegularEvent
    template_name = 'kanisa/management/diary/regular_events.html'
    kanisa_title = 'Regular Events'


class DiaryRegularEventCreateView(StaffMemberRequiredMixin,
                                  KanisaCreateView, DiaryBaseView):
    form_class = RegularEventForm
    kanisa_title = 'Create a Regular Event'
    success_url = reverse_lazy('kanisa_manage_diary_regularevents')

    def get_initial(self):
        initial = super(DiaryRegularEventCreateView, self).get_initial()
        initial['start_time'] = time(9, 0, 0)
        return initial


class DiaryRegularEventUpdateView(StaffMemberRequiredMixin,
                                  KanisaUpdateView, DiaryBaseView):
    form_class = RegularEventForm
    model = RegularEvent
    success_url = reverse_lazy('kanisa_manage_diary_regularevents')
    kanisa_form_warning = ('Changes made here will not affect events already '
                           'in the diary (whether they\'re future events or '
                           'not).')


class DiaryScheduledEventBaseView(DiaryBaseView):
    kanisa_lead = ('Scheduled events are particularly entries in a week\'s '
                   'diary - with an associated date and time.')


class DiaryScheduledEventCreateView(StaffMemberRequiredMixin,
                                    KanisaCreateView,
                                    DiaryScheduledEventBaseView):
    form_class = ScheduledEventCreationForm
    model = ScheduledEvent
    kanisa_title = 'Create Scheduled Event'

    def get_success_url(self):
        return self.get_relative_root_url(self.object.date.strftime('%Y%m%d'))

    def get_initial(self):
        initial = super(DiaryScheduledEventCreateView, self).get_initial()
        initial['start_time'] = time(9, 0, 0)
        initial['date'] = date.today()

        if 'date' in self.request.GET:
            thedate = self.request.GET['date']
            try:
                initial['date'] = datetime.strptime(thedate, '%Y%m%d').date()
            except ValueError:
                pass

        return initial


class DiaryScheduledEventUpdateView(StaffMemberRequiredMixin,
                                    KanisaUpdateView,
                                    DiaryScheduledEventBaseView):
    form_class = ScheduledEventEditForm
    model = ScheduledEvent

    def get_success_url(self):
        return self.get_relative_root_url(self.object.date.strftime('%Y%m%d'))


class DiaryScheduledEventCloneView(StaffMemberRequiredMixin,
                                   KanisaCreateView,
                                   DiaryScheduledEventBaseView):
    form_class = ScheduledEventCreationForm
    model = ScheduledEvent
    kanisa_title = 'Create Scheduled Event'

    def get_initial(self):
        try:
            pk = int(self.request.GET['event'])
        except ValueError:
            raise Http404
        except KeyError:
            raise Http404

        original = get_object_or_404(ScheduledEvent, pk=pk)
        initial = super(DiaryScheduledEventCloneView, self).get_initial()

        initial['title'] = original.title
        initial['event'] = original.event
        initial['start_time'] = original.start_time
        initial['duration'] = original.duration
        initial['details'] = original.details

        return initial

    def get_success_url(self):
        return self.get_relative_root_url(self.object.date.strftime('%Y%m%d'))


class DiaryScheduleRegularEventView(StaffMemberRequiredMixin,
                                    RedirectView, DiaryBaseView):
    permanent = False

    def get_redirect_url(self, pk, thedate):
        event = get_object_or_404(RegularEvent, pk=pk)

        try:
            event_date = datetime.strptime(thedate, '%Y%m%d').date()
            event_time = event.start_time
            parsed_date = datetime.combine(event_date, event_time)
        except ValueError:
            raise Http404

        formatted_date = formats.date_format(parsed_date,
                                             "DATE_FORMAT")
        formatted_time = formats.date_format(parsed_date,
                                             "TIME_FORMAT")
        date_string = '%s at %s' % (formatted_date, formatted_time)

        event_exists = ScheduledEvent.objects.filter(event=event,
                                                     date=parsed_date)
        if len(event_exists) != 0:
            message = u'%s already scheduled for %s' % (unicode(event),
                                                        date_string)
            messages.info(self.request, message)
            return self.get_relative_root_url(thedate)

        event.schedule(parsed_date, parsed_date + timedelta(days=1))

        message = u'%s scheduled for %s' % (unicode(event),
                                            date_string)
        messages.success(self.request, message)

        return self.get_relative_root_url(thedate)


class DiaryScheduleWeeksRegularEventView(StaffMemberRequiredMixin,
                                         RedirectView, DiaryBaseView):
    permanent = False

    def get_redirect_url(self):
        thedate = self.date_from_yyymmdd()
        monday, sunday = get_week_bounds(thedate)
        next_monday = sunday + timedelta(days=1)

        done_something = False

        for event in RegularEvent.objects.filter(autoschedule=True):
            exists = ScheduledEvent.objects.filter(event=event).\
                exclude(date__lt=monday).exclude(date__gt=next_monday)
            if not exists:
                done_something = True
                event.schedule(monday, next_monday)

        if done_something:
            messages.success(self.request, ('I\'ve scheduled this week\'s '
                                            'events for you - enjoy!'))
        else:
            messages.info(self.request, 'No events to schedule.')

        return self.get_relative_root_url()


class DiaryCancelScheduledEventView(StaffMemberRequiredMixin,
                                    KanisaDeleteView,
                                    DiaryScheduledEventBaseView):
    model = ScheduledEvent

    def get_date_string(self):
        parsed_date = datetime.combine(self.object.date,
                                       self.object.start_time)
        formatted_date = formats.date_format(parsed_date,
                                             "DATE_FORMAT")
        formatted_time = formats.date_format(parsed_date,
                                             "TIME_FORMAT")
        return '%s at %s' % (formatted_date, formatted_time)

    def get_deletion_confirmation_message(self):
        return 'Are you sure you want to cancel %s on %s?'\
            % (unicode(self.object), self.get_date_string())

    def get_kanisa_title(self):
        return 'Cancel Scheduled Event'

    def get_cancel_url(self):
        return self.get_relative_root_url(self.object.date.strftime('%Y%m%d'))

    def get_success_url(self):
        message = u'%s cancelled on %s' % (unicode(self.object),
                                           self.get_date_string())
        messages.success(self.request, message)

        return self.get_relative_root_url(self.object.date.strftime('%Y%m%d'))
