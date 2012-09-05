from datetime import timedelta
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from kanisa.models import RegularEvent, ScheduledEvent
from kanisa.utils.diary import get_week_bounds


class DiaryBaseView(object):
    def get_diary_context_data(self, **kwargs):
        return {'events': RegularEvent.objects.all()}


class DiaryIndexView(DiaryBaseView, TemplateView):
    template_name = 'kanisa/public/diary/index.html'

    def get_this_week(self):
        monday, sunday = get_week_bounds()
        events = ScheduledEvent.objects.filter(date__gte=monday,
                                               date__lte=sunday)

        thisweek = []

        for i in range(0, 7):
            thedate = monday + timedelta(days=i)
            thisweek.append((thedate,
                            [e for e in events if e.date == thedate]))

        return thisweek

    def get_context_data(self, **kwargs):
        context = super(DiaryIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())
        context['thisweek'] = self.get_this_week()

        return context


class RegularEventDetailView(DiaryBaseView, DetailView):
    model = RegularEvent
    template_name = 'kanisa/public/diary/regularevent.html'

    def get_context_data(self, **kwargs):
        context = super(RegularEventDetailView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())

        return context