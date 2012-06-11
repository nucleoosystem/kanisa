from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView


class KanisaCreateView(CreateView):
    def form_valid(self, form):
        model_name = form.instance._meta.verbose_name.title()
        message = u'%s "%s" created.' % (model_name,
                                         unicode(form.instance))
        messages.success(self.request, message, extra_tags='msg')
        return super(KanisaCreateView, self).form_valid(form)

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(KanisaCreateView, self).dispatch(*args, **kwargs)


class KanisaUpdateView(UpdateView):
    def form_valid(self, form):
        model_name = form.instance._meta.verbose_name.title()
        message = u'%s "%s" saved.' % (model_name,
                                       unicode(form.instance))
        messages.success(self.request, message, extra_tags='msg')
        return super(KanisaUpdateView, self).form_valid(form)

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(KanisaUpdateView, self).dispatch(*args, **kwargs)


class KanisaListView(ListView):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(KanisaListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(KanisaListView,
                        self).get_context_data(**kwargs)

        if hasattr(self, 'kanisa_title'):
            context['kanisa_title'] = self.kanisa_title

        return context
