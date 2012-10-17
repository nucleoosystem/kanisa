from datetime import date, datetime, time, timedelta

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from kanisa.forms.diary import (RegularEventForm,
                                ScheduledEventEditForm,
                                ScheduledEventCreationForm,
                                EventContactForm)
from kanisa.models import EventContact, RegularEvent, ScheduledEvent
from kanisa.utils.diary import (get_schedule, get_week_bounds,
                                datetime_to_string)
from kanisa.views.generic import (KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaTemplateView,
                                  KanisaDeleteView,
                                  KanisaAuthorizationMixin)


class DiaryBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Diary events are regularly occurring events you want to '
                   'display on your church\'s calendar.')
    kanisa_root_crumb = {'text': 'Diary',
                         'url': reverse_lazy('kanisa_manage_diary')}
    permission = 'kanisa.manage_diary'
    kanisa_nav_component = 'diary'

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


class DiaryEventIndexView(DiaryBaseView,
                          KanisaTemplateView):
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


class DiaryRegularEventsView(DiaryBaseView,
                             KanisaListView):
    model = RegularEvent
    template_name = 'kanisa/management/diary/regular_events.html'
    kanisa_title = 'Regular Events'


class DiaryRegularEventCreateView(DiaryBaseView,
                                  KanisaCreateView):
    form_class = RegularEventForm
    kanisa_title = 'Create a Regular Event'
    success_url = reverse_lazy('kanisa_manage_diary_regularevents')

    def get_initial(self):
        initial = super(DiaryRegularEventCreateView, self).get_initial()
        initial['start_time'] = time(9, 0, 0)
        return initial


class DiaryRegularEventUpdateView(DiaryBaseView,
                                  KanisaUpdateView):
    form_class = RegularEventForm
    model = RegularEvent
    success_url = reverse_lazy('kanisa_manage_diary_regularevents')
    kanisa_form_warning = ('Changes made here will not affect events '
                           'already in the diary (whether they\'ve '
                           'happened already or not).')


class DiaryRegularEventBulkEditView(DiaryBaseView,
                                    KanisaTemplateView):
    template_name = 'kanisa/management/diary/bulk_edit.html'
    model = RegularEvent

    def get_object(self):
        if hasattr(self, 'object'):
            return self.object

        pk = int(self.kwargs.get('pk', None))

        return get_object_or_404(RegularEvent, pk=pk)

    def get_kanisa_title(self):
        return 'Bulk Edit: %s' % unicode(self.get_object())

    def get_events(self):
        events = ScheduledEvent.objects.filter(event=self.get_object())
        events = events.filter(date__gte=datetime.today())
        return events

    def save_event(self, pk, intro, start_time):
        event = ScheduledEvent.objects.get(pk=pk)
        event.intro = intro
        event.start_time = start_time
        event.save()

    def get_event_pks(self, items):
        pks = []
        for key, value in items:
            if key.startswith("intro_"):
                pks.append(int(key[len("intro_"):]))

        return pks

    def post(self, request, *args, **kwargs):
        pks = self.get_event_pks(self.request.POST.items())
        for pk in pks:
            self.save_event(pk,
                            self.request.POST['intro_%d' % pk],
                            self.request.POST['start_time_%d' % pk])

        messages.success(request, "Events saved.")

        url = reverse('kanisa_manage_diary_regularevents')

        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(DiaryRegularEventBulkEditView,
                        self).get_context_data(**kwargs)

        context['events'] = self.get_events()
        context['object'] = self.get_object()

        return context


class DiaryScheduledEventBaseView(DiaryBaseView):
    kanisa_lead = ('Scheduled events are particular entries in a week\'s '
                   'diary - with an associated date and time.')


class DiaryScheduledEventCreateView(DiaryScheduledEventBaseView,
                                    KanisaCreateView):
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


class DiaryScheduledEventUpdateView(DiaryScheduledEventBaseView,
                                    KanisaUpdateView):
    form_class = ScheduledEventEditForm
    model = ScheduledEvent

    def get_success_url(self):
        return self.get_relative_root_url(self.object.date.strftime('%Y%m%d'))


class DiaryScheduledEventCloneView(DiaryScheduledEventBaseView,
                                   KanisaCreateView):
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


class DiaryScheduleRegularEventView(DiaryBaseView,
                                    RedirectView):
    permanent = False

    def parse_date_to_datetime(self, thedate, event):
        try:
            event_date = datetime.strptime(thedate, '%Y%m%d').date()
            return datetime.combine(event_date, event.start_time)
        except ValueError:
            raise Http404

    def get_redirect_url(self, pk, thedate):
        event = get_object_or_404(RegularEvent, pk=pk)
        parsed_date = self.parse_date_to_datetime(thedate, event)

        try:
            event.schedule_once(parsed_date)
            message = '%s scheduled for %s' % (unicode(event),
                                               datetime_to_string(parsed_date))
            messages.success(self.request, message)
        except event.AlreadyScheduled:
            date_string = datetime_to_string(parsed_date)
            message = '%s already scheduled for %s' % (unicode(event),
                                                       date_string)

            messages.info(self.request, message)

        return self.get_relative_root_url(thedate)


class DiaryScheduleWeeksRegularEventView(DiaryBaseView,
                                         RedirectView):
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


class DiaryCancelScheduledEventView(DiaryScheduledEventBaseView,
                                    KanisaDeleteView):
    model = ScheduledEvent

    def get_date_string(self):
        parsed_date = datetime.combine(self.object.date,
                                       self.object.start_time)
        return datetime_to_string(parsed_date)

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


class EventContactBaseView(DiaryBaseView):
    kanisa_lead = ('Event contacts help people get in touch with the person '
                   'relevant to their questions about your events.')


class EventContactIndexView(EventContactBaseView,
                            KanisaListView):
    model = EventContact
    queryset = EventContact.objects.all()

    template_name = 'kanisa/management/diary/contacts.html'
    kanisa_title = 'Manage Contacts'


class EventContactCreateView(EventContactBaseView,
                             KanisaCreateView):
    form_class = EventContactForm
    kanisa_title = 'Add an Event Contact'
    success_url = reverse_lazy('kanisa_manage_sermons_speaker')


class EventContactUpdateView(EventContactBaseView,
                             KanisaUpdateView):
    form_class = EventContactForm
    model = EventContact
    success_url = reverse_lazy('kanisa_manage_sermons_speaker')
