from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from kanisa.models import RegularEvent


class DiaryBaseView(object):
    def get_diary_context_data(self, **kwargs):
        return {'events': RegularEvent.objects.all()}


class DiaryIndexView(DiaryBaseView, TemplateView):
    template_name = 'kanisa/public/diary/index.html'

    def get_context_data(self, **kwargs):
        context = super(DiaryIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())

        return context


class RegularEventDetailView(DiaryBaseView, DetailView):
    model = RegularEvent
    template_name = 'kanisa/public/diary/regularevent.html'

    def get_context_data(self, **kwargs):
        context = super(RegularEventDetailView,
                        self).get_context_data(**kwargs)

        context.update(self.get_diary_context_data())

        return context
