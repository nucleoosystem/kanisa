from datetime import timedelta
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from kanisa.models import RegularEvent, ScheduledEvent
from kanisa.utils.diary import get_week_bounds, event_covers_date


class DiaryBaseView(object):
    def get_diary_context_data(self, **kwargs):
        return {'events': RegularEvent.objects.all()}


class DiaryIndexView(DiaryBaseView, TemplateView):
    template_name = 'kanisa/public/diary/index.html'

    def get_this_week(self):
        monday, sunday = get_week_bounds()
        events = ScheduledEvent.events_between(monday,
                                               sunday)

        thisweek = []

        for i in range(0, 7):
            thedate = monday + timedelta(days=i)
            thisweek.append((thedate,
                            [e for e in events
                             if event_covers_date(e, thedate)]))

        return thisweek

    def get_context_data(self, **kwargs):
        context = super(DiaryIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())
        context['thisweek'] = self.get_this_week()
        context['kanisa_title'] = 'What\'s On'

        return context


class RegularEventDetailView(DiaryBaseView, DetailView):
    model = RegularEvent
    template_name = 'kanisa/public/diary/regularevent.html'

    def get_context_data(self, **kwargs):
        context = super(RegularEventDetailView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())

        context['kanisa_title'] = unicode(self.object)

        return context


class ScheduledEventDetailView(DiaryBaseView, DetailView):
    queryset = ScheduledEvent.objects.filter(event__isnull=True)
    template_name = 'kanisa/public/diary/scheduledevent.html'

    def get_context_data(self, **kwargs):
        context = super(ScheduledEventDetailView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())

        context['kanisa_title'] = unicode(self.object)

        return context
