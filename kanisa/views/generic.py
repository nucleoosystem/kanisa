from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView


def add_kanisa_context(cls, context):
    if hasattr(cls, 'get_kanisa_title'):
        context['kanisa_title'] = cls.get_kanisa_title()
    elif hasattr(cls, 'kanisa_title'):
        context['kanisa_title'] = cls.kanisa_title

    if hasattr(cls, 'kanisa_lead'):
        context['kanisa_lead'] = cls.kanisa_lead

    if hasattr(cls, 'get_kanisa_root_crumb'):
        context['kanisa_root_crumb'] = cls.get_kanisa_root_crumb()
        
    context['kanisa_is_root_view'] = getattr(cls, 'kanisa_is_root_view', False)

    return context


class KanisaTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(KanisaTemplateView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context


class KanisaCreateView(CreateView):
    def form_valid(self, form):
        model_name = form.instance._meta.verbose_name.title()
        message = u'%s "%s" created.' % (model_name,
                                         unicode(form.instance))
        messages.success(self.request, message, extra_tags='msg')
        return super(KanisaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(KanisaCreateView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context


class KanisaUpdateView(UpdateView):
    def form_valid(self, form):
        model_name = form.instance._meta.verbose_name.title()
        message = u'%s "%s" saved.' % (model_name,
                                       unicode(form.instance))
        messages.success(self.request, message, extra_tags='msg')
        return super(KanisaUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(KanisaUpdateView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context


class KanisaListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(KanisaListView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context
