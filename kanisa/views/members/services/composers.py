from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from kanisa.forms.services import ComposerForm
from kanisa.views.members.services import ServiceRestrictedBaseView
from kanisa.views.generic import KanisaCreateView


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
            req = self.request
            tmpl = 'kanisa/members/services/composer_popup_close.html'
            return render_to_response(
                tmpl,
                {'object': self.object},
                context_instance=RequestContext(req)
            )

        rval = super(KanisaCreateView, self).form_valid(form)

        messages.success(self.request, self.get_message(form.instance))

        return rval
composer_create = ComposerCreateView.as_view()
