from datetime import date, datetime, time, timedelta

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import formats
from django.views.generic.base import RedirectView

from kanisa.forms import (RegularEventForm, ScheduledEventEditForm,
                          ScheduledEventCreationForm)
from kanisa.models import RegularEvent, ScheduledEvent
from kanisa.utils import get_schedule, get_week_bounds
from kanisa.views.generic import (KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaTemplateView)


class DiaryBaseView:
    kanisa_lead = ('Diary events are regularly occurring events you want to '
                   'display on your church\'s calendar.')

    def get_kanisa_root_crumb(self):
        return {'text': 'Diary',
                'url': reverse('kanisa_manage_diary')}


class DiaryEventIndexView(KanisaTemplateView, DiaryBaseView):
    template_name = 'kanisa/management/diary/index.html'
    kanisa_title = 'Manage Diary'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(DiaryEventIndexView,
                        self).get_context_data(**kwargs)

        schedule = get_schedule()
        context['calendar'] = schedule.calendar_entries
        context['events_to_schedule'] = schedule.events_to_schedule

        return context


class DiaryRegularEventsView(KanisaListView, DiaryBaseView):
    model = RegularEvent
    template_name = 'kanisa/management/diary/regular_events.html'
    kanisa_title = 'Manage Regular Events'


class DiaryRegularEventCreateView(KanisaCreateView, DiaryBaseView):
    form_class = RegularEventForm
    template_name = 'kanisa/management/create.html'
    kanisa_title = 'Create a Regular Event'

    def get_success_url(self):
        return reverse('kanisa_manage_diary')

    def get_initial(self):
        initial = super(DiaryRegularEventCreateView, self).get_initial()
        initial['start_time'] = time(9, 0, 0)
        return initial


class DiaryRegularEventUpdateView(KanisaUpdateView, DiaryBaseView):
    form_class = RegularEventForm
    template_name = 'kanisa/management/create.html'
    model = RegularEvent
    kanisa_form_warning = ('Changes made here will not affect events already '
                           'in the diary (whether they\'re future events or '
                           'not).')

    def get_kanisa_title(self):
        return 'Edit Event: %s' % unicode(self.object)

    def get_success_url(self):
        return reverse('kanisa_manage_diary')


class DiaryScheduledEventCreateView(KanisaCreateView, DiaryBaseView):
    form_class = ScheduledEventCreationForm
    template_name = 'kanisa/management/create.html'
    model = ScheduledEvent
    kanisa_title = 'Create Scheduled Event'
    kanisa_lead = ('Scheduled events are particularly entries in a week\'s '
                   'diary - with an associated date and time.')

    def get_success_url(self):
        return reverse('kanisa_manage_diary')

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


class DiaryScheduledEventUpdateView(KanisaUpdateView, DiaryBaseView):
    form_class = ScheduledEventEditForm
    template_name = 'kanisa/management/create.html'
    model = ScheduledEvent
    kanisa_lead = ('Scheduled events are particularly entries in a week\'s '
                   'diary - with an associated date and time.')

    def get_kanisa_title(self):
        return 'Edit Scheduled Event: %s' % unicode(self.object)

    def get_success_url(self):
        return reverse('kanisa_manage_diary')


class DiaryScheduleRegularEventView(RedirectView):
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
            return reverse('kanisa_manage_diary')

        event.schedule(parsed_date, parsed_date + timedelta(days=1))

        message = u'%s scheduled for %s' % (unicode(event),
                                            date_string)
        messages.success(self.request, message)

        return reverse('kanisa_manage_diary')


class DiaryScheduleWeeksRegularEventView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        monday, sunday = get_week_bounds()
        next_monday = sunday + timedelta(days=1)

        done_something = False

        for event in RegularEvent.objects.all():
            exists = ScheduledEvent.objects.filter(event=event).\
                                            exclude(date__lt=monday,
                                                    date__gt=next_monday)
            if not exists:
                done_something = True
                event.schedule(monday, next_monday)

        if done_something:
            messages.success(self.request, ('I\'ve scheduled this week\'s '
                                            'events for you - enjoy!'))
        else:
            messages.info(self.request, 'No events to schedule.')

        return reverse('kanisa_manage_diary')


class DiaryCancelScheduledEventView(RedirectView):
    permanent = False

    def get_redirect_url(self, pk):
        event = get_object_or_404(ScheduledEvent, pk=pk)

        parsed_date = datetime.combine(event.date, event.start_time)

        formatted_date = formats.date_format(parsed_date,
                                             "DATE_FORMAT")
        formatted_time = formats.date_format(parsed_date,
                                             "TIME_FORMAT")
        date_string = '%s at %s' % (formatted_date, formatted_time)

        event.delete()

        message = u'%s cancelled on %s' % (unicode(event),
                                           date_string)
        messages.success(self.request, message)

        return reverse('kanisa_manage_diary')
