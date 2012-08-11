from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from kanisa.models import RegularEvent


class DiaryIndexView(TemplateView):
    template_name = 'kanisa/public/diary/index.html'

    def get_context_data(self, **kwargs):
        context = super(DiaryIndexView,
                        self).get_context_data(**kwargs)

        context['events'] = RegularEvent.objects.all()

        return context


class RegularEventDetailView(DetailView):
    model = RegularEvent
    template_name = 'kanisa/public/diary/regularevent.html'

    def get_context_data(self, **kwargs):
        context = super(RegularEventDetailView,
                        self).get_context_data(**kwargs)

        context['events'] = RegularEvent.objects.all()

        return context
