from django.contrib import messages
from django.shortcuts import render
from kanisa.forms.services import ComposerForm
from kanisa.models import Composer
from kanisa.views.members.services import ServiceRestrictedBaseView
from kanisa.views.members.services.songs import SongFinderBaseView
from kanisa.views.generic import (
    KanisaCreateView,
    KanisaDetailView,
)


class ComposerCreateView(ServiceRestrictedBaseView,
                         KanisaCreateView):
    form_class = ComposerForm
    kanisa_title = 'Add a Composer'

    def get_template_names(self):
        if self.is_popup():
            return ['kanisa/management/popup.html', ]
        return ['kanisa/members/form.html', ]

    def form_valid(self, form):
        if self.is_popup():
            self.object = form.save()
            tmpl = 'kanisa/members/services/composer_popup_close.html'
            return render(
                self.request,
                tmpl,
                {'object': self.object}
            )

        rval = super(KanisaCreateView, self).form_valid(form)

        messages.success(self.request, self.get_message(form.instance))

        return rval
composer_create = ComposerCreateView.as_view()


class ComposerDetailView(SongFinderBaseView, KanisaDetailView):
    model = Composer
    template_name = 'kanisa/members/services/composer_detail.html'
    pk_url_kwarg = 'composer_pk'

    def get_context_data(self, **kwargs):
        context = super(ComposerDetailView,
                        self).get_context_data(**kwargs)

        context['song_list'] = self.get_songs()
        return context

    def get_songs(self):
        qs = self.object.song_set.prefetch_related('composers')
        return qs.all()
composer_detail = ComposerDetailView.as_view()
