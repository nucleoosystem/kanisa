from django.views.generic.detail import DetailView
from kanisa.models import RegularEvent


class RegularEventDetailView(DetailView):
    model = RegularEvent
    template_name = 'kanisa/public/diary/regularevent.html'
