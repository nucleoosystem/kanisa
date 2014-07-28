import calendar
from datetime import date, timedelta
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import (
    DetailView,
    RedirectView,
    TemplateView
)
from kanisa.models import RegularEvent, ScheduledEvent, EventCategory
from kanisa.utils.diary import get_this_week


class DiaryBaseView(object):
    def get_diary_context_data(self, **kwargs):
        return {'events': RegularEvent.objects.all()}


class DiaryIndexView(DiaryBaseView, TemplateView):
    template_name = 'kanisa/public/diary/index.html'

    def get_category(self, request):
        category_key = request.GET.get('category', 0)

        try:
            category = int(category_key)
        except ValueError:
            raise Http404("Bad category value '%s' provided."
                          % category_key)

        if category == 0:
            return None

        try:
            return EventCategory.objects.get(pk=category)
        except EventCategory.DoesNotExist:
            raise Http404("Non-existent category value provided.")

    def get(self, request, *args, **kwargs):
        self.category = self.get_category(request)
        context = self.get_context_data(**kwargs)

        if request.is_ajax():
            req = RequestContext(request)
            tmpl = 'kanisa/public/diary/_regular_event_list.html'
            return render_to_response(tmpl,
                                      context,
                                      context_instance=req)

        return self.render_to_response(context)

    def get_events(self):
        if self.category is None:
            return None
        else:
            return self.category.regularevent_set.all()

    def get_context_data(self, **kwargs):
        context = super(DiaryIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())
        context['thisweek'] = get_this_week()
        context['kanisa_title'] = 'What\'s On'
        categories = EventCategory.objects.filter(num_events__gt=0)
        context['event_categories'] = categories
        context['category'] = self.category

        events = self.get_events()
        if events is None:
            context['events_to_display'] = context['events']
        else:
            context['events_to_display'] = events

        return context
diary_index = DiaryIndexView.as_view()


class RegularEventDetailView(DiaryBaseView, DetailView):
    model = RegularEvent
    template_name = 'kanisa/public/diary/regularevent.html'

    def get_context_data(self, **kwargs):
        context = super(RegularEventDetailView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())

        context['kanisa_title'] = unicode(self.object)

        return context
regular_event_detail = RegularEventDetailView.as_view()


class ScheduledEventDetailView(DiaryBaseView, DetailView):
    model = ScheduledEvent
    template_name = 'kanisa/public/diary/scheduledevent.html'

    def get_object(self, queryset=None):
        object = super(ScheduledEventDetailView, self).get_object(queryset)

        if not object.is_special():
            raise Http404("You can't view details for events that aren't "
                          "special.")

        return object

    def get_context_data(self, **kwargs):
        context = super(ScheduledEventDetailView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())

        context['kanisa_title'] = unicode(self.object)

        return context
scheduled_event_detail = ScheduledEventDetailView.as_view()


class DiaryPrintableRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        current = date.today()
        year = '%d' % current.year
        month = '%02d' % current.month
        return reverse(
            'kanisa_public_diary_printable',
            args=[year, month]
        )
diary_printable_redirect = DiaryPrintableRedirectView.as_view()


class DiaryPrintableView(TemplateView):
    template_name = 'kanisa/public/diary/print.html'

    def get_date_bounds(self):
        current = date(
            int(self.kwargs['year']),
            int(self.kwargs['month']),
            1
        )
        day_range = calendar.monthrange(current.year, current.month)
        first = current
        last = current.replace(day=day_range[1])
        return first, last

    def get_context_data(self, **kwargs):
        ctx = super(DiaryPrintableView, self).get_context_data(
            **kwargs
        )

        bounds = self.get_date_bounds()
        nextmonth = bounds[1] + timedelta(days=1)

        ctx['startdate'] = bounds[0]
        ctx['events'] = ScheduledEvent.events_between(*bounds)
        ctx['nextmonth'] = nextmonth
        ctx['nexturl'] = reverse(
            'kanisa_public_diary_printable',
            args=[
                '%d' % nextmonth.year,
                '%02d' % nextmonth.month
            ]
        )

        return ctx
diary_printable = DiaryPrintableView.as_view()
