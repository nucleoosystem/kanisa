from datetime import date, datetime, time, timedelta
from time import strptime

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from kanisa.forms.diary import (
    RegularEventForm,
    RegularEventMothballForm,
    ScheduledEventEditForm,
    ScheduledEventCreationForm,
    ScheduledEventSeriesForm,
    EventContactForm,
    EventCategoryForm
)
from kanisa.models import (
    EventContact,
    RegularEvent,
    ScheduledEvent,
    ScheduledEventSeries,
    EventCategory
)
from kanisa.utils.diary import (
    get_schedule,
    get_week_bounds,
    datetime_to_string
)
from kanisa.views.generic import (
    KanisaCreateView,
    KanisaUpdateView,
    KanisaListView,
    KanisaTemplateView,
    KanisaDeleteView,
    KanisaAuthorizationMixin
)


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
        context = super(DiaryEventIndexView,
                        self).get_context_data(**kwargs)

        thedate = self.date_from_yyymmdd()
        schedule = get_schedule(thedate)
        context['previousdate'] = (schedule.monday -
                                   timedelta(days=7)).strftime("%Y%m%d")
        context['nextdate'] = (schedule.monday +
                               timedelta(days=7)).strftime("%Y%m%d")
        context['monday'] = schedule.monday
        context['calendar'] = schedule.calendar_entries
        context['events_to_schedule'] = schedule.events_to_schedule

        return context
diary_management = DiaryEventIndexView.as_view()


class DiaryRegularEventsBaseView(DiaryBaseView):
    def get_kanisa_intermediate_crumbs(self):
        return [{'url': reverse('kanisa_manage_diary_regularevents'),
                 'title': 'Regular Events'},
                ]


class DiaryRegularEventsView(DiaryBaseView,
                             KanisaListView):
    model = RegularEvent
    template_name = 'kanisa/management/diary/regular_events.html'
    kanisa_title = 'Regular Events'

    def get_queryset(self, *args, **kwargs):
        return RegularEvent.objects.filter(mothballed=False)
diary_regular_events = DiaryRegularEventsView.as_view()


class DiaryRegularEventCreateView(DiaryRegularEventsBaseView,
                                  KanisaCreateView):
    form_class = RegularEventForm
    kanisa_title = 'Create a Regular Event'
    success_url = reverse_lazy('kanisa_manage_diary_regularevents')

    def get_initial(self):
        initial = super(DiaryRegularEventCreateView, self).get_initial()
        initial['start_time'] = time(9, 0, 0)
        return initial
diary_regular_event_create = DiaryRegularEventCreateView.as_view()


class DiaryRegularEventUpdateView(DiaryRegularEventsBaseView,
                                  KanisaUpdateView):
    form_class = RegularEventForm
    model = RegularEvent
    success_url = reverse_lazy('kanisa_manage_diary_regularevents')
    kanisa_form_warning = ('Changes made here will not affect events '
                           'already in the diary (whether they\'ve '
                           'happened already or not).')
diary_regular_event_update = DiaryRegularEventUpdateView.as_view()


class DiaryRegularEventMothballView(DiaryRegularEventsBaseView,
                                    KanisaUpdateView):
    form_class = RegularEventMothballForm
    model = RegularEvent
    success_url = reverse_lazy('kanisa_manage_diary_regularevents')
    kanisa_form_warning = ('Changes made here will not affect events '
                           'already in the diary (whether they\'ve '
                           'happened already or not).')

    def get_form(self, form_class):
        # Skipping the save-and-continue button added by
        # KanisaUpdateView.
        return super(KanisaUpdateView, self).get_form(form_class)

    def get_message(self, form):
        return u'"%s" has been mothballed.' % (unicode(form.instance))

    def form_valid(self, form):
        messages.success(self.request, self.get_message(form))
        self.object.mothballed = True
        self.object.autoschedule = False
        return super(KanisaUpdateView, self).form_valid(form)

    def get_kanisa_default_title(self):
        return 'Mothball %s: %s' % (self.object._meta.verbose_name.title(),
                                unicode(self.object))

diary_regular_event_mothball = DiaryRegularEventMothballView.as_view()

class DiaryRegularEventBulkEditView(DiaryRegularEventsBaseView,
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

    def save_event(self, pk, intro, start_time, series):
        event = ScheduledEvent.objects.get(pk=pk)
        event.intro = intro

        if start_time:
            event.start_time = start_time

        if series:
            event.series = series

        event.save()

    def get_event_pks(self, items):
        pks = []
        for key, value in items:
            if key.startswith("intro_"):
                pks.append(int(key[len("intro_"):]))

        return pks

    def post(self, request, *args, **kwargs):
        def get_event_time(value):
            try:
                event_time = strptime(
                    value,
                    "%I:%M %p"
                )
                return time(
                    event_time.tm_hour,
                    event_time.tm_min
                )
            except ValueError:
                # TODO - this is a horrible hack that needs stripping
                # out, we should really re-display the form if this
                # happens.
                return None

        def get_event_series(value):
            if not value:
                return None

            return ScheduledEventSeries.objects.get(pk=value)

        pks = self.get_event_pks(self.request.POST.items())

        for pk in pks:
            event_time = get_event_time(
                self.request.POST['start_time_%d' % pk]
            )

            event_series = get_event_series(
                self.request.POST['series_%d' % pk]
            )

            self.save_event(
                pk,
                self.request.POST['intro_%d' % pk],
                event_time,
                event_series
            )

        messages.success(request, "Events saved.")

        url = reverse('kanisa_manage_diary_regularevents')

        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(DiaryRegularEventBulkEditView,
                        self).get_context_data(**kwargs)

        context['events'] = self.get_events()
        context['object'] = self.get_object()
        context['series'] = ScheduledEventSeries.objects.all()

        return context
diary_regular_event_bulk_edit = DiaryRegularEventBulkEditView.as_view()


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
diary_scheduled_event_create = DiaryScheduledEventCreateView.as_view()


class DiaryScheduledEventUpdateView(DiaryScheduledEventBaseView,
                                    KanisaUpdateView):
    form_class = ScheduledEventEditForm
    model = ScheduledEvent

    def get_initial(self):
        initial = super(DiaryScheduledEventUpdateView, self).get_initial()

        if not self.object.title and self.object.event:
            initial['title'] = self.object.event.title

        return initial

    def get_success_url(self):
        return self.get_relative_root_url(self.object.date.strftime('%Y%m%d'))
diary_scheduled_event_update = DiaryScheduledEventUpdateView.as_view()


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
        initial['contact'] = original.contact
        initial['intro'] = original.intro
        initial['series'] = original.series

        return initial

    def get_success_url(self):
        return self.get_relative_root_url(self.object.date.strftime('%Y%m%d'))
diary_scheduled_event_clone = DiaryScheduledEventCloneView.as_view()


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
diary_schedule_regular_event = DiaryScheduleRegularEventView.as_view()


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
diary_schedule_weeks_events = DiaryScheduleWeeksRegularEventView.as_view()


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
diary_cancel_scheduled_event = DiaryCancelScheduledEventView.as_view()


class EventContactBaseView(DiaryBaseView):
    kanisa_lead = ('Event contacts help people get in touch with the person '
                   'relevant to their questions about your events.')

    def get_kanisa_intermediate_crumbs(self):
        return [{'url': reverse('kanisa_manage_diary_contacts'),
                 'title': 'Contacts'},
                ]


class EventContactIndexView(EventContactBaseView,
                            KanisaListView):
    model = EventContact
    queryset = EventContact.objects.all()

    template_name = 'kanisa/management/diary/contacts.html'
    kanisa_title = 'Contacts'

    def get_kanisa_intermediate_crumbs(self):
        return []
diary_event_contact_management = EventContactIndexView.as_view()


class EventContactCreateView(EventContactBaseView,
                             KanisaCreateView):
    form_class = EventContactForm
    kanisa_title = 'Add an Event Contact'
    success_url = reverse_lazy('kanisa_manage_diary_contacts')
diary_event_contact_create = EventContactCreateView.as_view()


class EventContactUpdateView(EventContactBaseView,
                             KanisaUpdateView):
    form_class = EventContactForm
    model = EventContact
    success_url = reverse_lazy('kanisa_manage_diary_contacts')
diary_event_contact_update = EventContactUpdateView.as_view()


class EventCategoryBaseView(DiaryBaseView):
    kanisa_lead = ('Event categories help people find events relevant to '
                   'them')

    def get_kanisa_intermediate_crumbs(self):
        return [{'url': reverse('kanisa_manage_diary_categories'),
                 'title': 'Categories'},
                ]


class EventCategoryIndexView(EventCategoryBaseView,
                             KanisaListView):
    model = EventCategory
    queryset = EventCategory.objects.all()

    template_name = 'kanisa/management/diary/categories.html'
    kanisa_title = 'Categories'

    def get_kanisa_intermediate_crumbs(self):
        return []
diary_event_category_management = EventCategoryIndexView.as_view()


class EventCategoryCreateView(EventCategoryBaseView,
                              KanisaCreateView):
    form_class = EventCategoryForm
    kanisa_title = 'Add an Event Category'
    success_url = reverse_lazy('kanisa_manage_diary_categories')
diary_event_category_create = EventCategoryCreateView.as_view()


class EventCategoryUpdateView(EventCategoryBaseView,
                              KanisaUpdateView):
    form_class = EventCategoryForm
    model = EventCategory
    success_url = reverse_lazy('kanisa_manage_diary_categories')
diary_event_category_update = EventCategoryUpdateView.as_view()


class EventSeriesBaseView(DiaryBaseView):
    kanisa_lead = 'Event series help people find links between events.'

    def get_kanisa_intermediate_crumbs(self):
        return [{'url': reverse('kanisa_manage_diary_series'),
                 'title': 'Event Series'},
                ]


class ScheduledEventSeriesView(EventSeriesBaseView,
                               KanisaListView):
    model = ScheduledEventSeries
    template_name = 'kanisa/management/diary/series.html'
    kanisa_title = 'Series'

    def get_kanisa_intermediate_crumbs(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ScheduledEventSeriesView,
                        self).get_context_data(**kwargs)
        relevant_events = ScheduledEvent.objects.filter(
            series__isnull=False
        )
        for series in context['object_list']:
            series.cached_events = [e for e in relevant_events
                                    if e.series == series]
        return context
diary_event_series = ScheduledEventSeriesView.as_view()


class ScheduledEventSeriesCreateView(EventSeriesBaseView,
                                     KanisaCreateView):
    form_class = ScheduledEventSeriesForm
    kanisa_title = 'Add an Event Series'
    success_url = reverse_lazy('kanisa_manage_diary_series')
diary_event_series_create = ScheduledEventSeriesCreateView.as_view()


class ScheduledEventSeriesUpdateView(EventSeriesBaseView,
                                     KanisaUpdateView):
    form_class = ScheduledEventSeriesForm
    model = ScheduledEventSeries
    success_url = reverse_lazy('kanisa_manage_diary_series')
diary_event_series_update = ScheduledEventSeriesUpdateView.as_view()
