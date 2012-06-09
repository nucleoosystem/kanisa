from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView


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
