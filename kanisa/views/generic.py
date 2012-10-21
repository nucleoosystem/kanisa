from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import (HttpResponse,
                         HttpResponseForbidden,
                         HttpResponseRedirect)
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlquote
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView,
                                       FormView)
from django.views.generic.list import ListView
from kanisa.utils.auth import has_any_kanisa_permission


def add_kanisa_context(cls, context):
    if hasattr(cls, 'get_kanisa_title'):
        context['kanisa_title'] = cls.get_kanisa_title()
    elif hasattr(cls, 'kanisa_title'):
        context['kanisa_title'] = cls.kanisa_title
    elif hasattr(cls, 'get_kanisa_default_title'):
        context['kanisa_title'] = cls.get_kanisa_default_title()

    if hasattr(cls, 'kanisa_lead'):
        context['kanisa_lead'] = cls.kanisa_lead

    if hasattr(cls, 'kanisa_root_crumb'):
        context['kanisa_root_crumb'] = cls.kanisa_root_crumb

    context['kanisa_is_root_view'] = getattr(cls, 'kanisa_is_root_view', False)

    if hasattr(cls, 'kanisa_form_warning'):
        context['kanisa_form_warning'] = cls.kanisa_form_warning

    if hasattr(cls, 'kanisa_nav_component'):
        context['kanisa_nav_component'] = cls.kanisa_nav_component

    return context


class KanisaAuthorizationMixin(object):
    redirect_field_name = REDIRECT_FIELD_NAME

    def authorization_check(self, user):
        return user.has_perm(self.permission)

    def handle_failure(self, request):
        if request.user.is_authenticated():
            # Logged in, but no permission
            return HttpResponseForbidden()

        path = urlquote(request.get_full_path())
        login_url = settings.LOGIN_URL
        tup = login_url, self.redirect_field_name, path
        return HttpResponseRedirect("%s?%s=%s" % tup)

    def dispatch(self, request, *args, **kwargs):
        if self.authorization_check(request.user):
            return super(KanisaAuthorizationMixin, self).dispatch(
                request,
                *args,
                **kwargs)

        return self.handle_failure(request)


class KanisaAnyAuthorizationMixin(KanisaAuthorizationMixin):
    def authorization_check(self, user):
        return has_any_kanisa_permission(user)


class KanisaTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(KanisaTemplateView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context


class KanisaFormView(FormView):
    def get_context_data(self, **kwargs):
        context = super(KanisaFormView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context


class KanisaDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(KanisaDetailView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context

    def get_kanisa_default_title(self):
        return unicode(self.object)


class KanisaCreateView(CreateView):
    def is_popup(self):
        return '_popup' in self.request.META['QUERY_STRING']

    def get_template_names(self):
        if self.is_popup():
            return ['kanisa/management/popup.html', ]

        return ['kanisa/management/create.html', ]

    def get_message(self, instance):
        model_name = instance._meta.verbose_name.title()
        return '%s "%s" created.' % (model_name,
                                     unicode(instance))

    def form_valid(self, form):
        if self.is_popup():
            self.object = form.save()
            req = self.request
            return render_to_response('kanisa/management/popup_close.html',
                                      {},
                                      context_instance=RequestContext(req))

        rval = super(KanisaCreateView, self).form_valid(form)

        messages.success(self.request, self.get_message(form.instance))

        return rval

    def get_context_data(self, **kwargs):
        context = super(KanisaCreateView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context


class KanisaUpdateView(UpdateView):
    template_name = 'kanisa/management/create.html'

    def form_valid(self, form):
        model_name = form.instance._meta.verbose_name.title()
        message = u'%s "%s" saved.' % (model_name,
                                       unicode(form.instance))
        messages.success(self.request, message)
        return super(KanisaUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(KanisaUpdateView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context

    def get_kanisa_default_title(self):
        return 'Edit %s: %s' % (self.object._meta.verbose_name.title(),
                                unicode(self.object))


class KanisaListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(KanisaListView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)

        return context


class KanisaDeleteView(DeleteView):
    template_name = 'kanisa/management/delete.html'

    def get_deletion_confirmation_message(self):
        return 'Are you sure you want to delete %s?' % unicode(self.object)

    def get_kanisa_default_title(self):
        return 'Delete %s' % self.model._meta.verbose_name.title()

    def get_context_data(self, **kwargs):
        context = super(KanisaDeleteView,
                        self).get_context_data(**kwargs)

        context = add_kanisa_context(self, context)
        msg = self.get_deletion_confirmation_message()
        context['kanisa_delete_confirm'] = msg
        context['kanisa_cancel_url'] = self.get_cancel_url()

        return context

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            self.object.delete()
            return HttpResponse('"%s" deleted' % self.object)

        return super(KanisaDeleteView, self).delete(request, *args, **kwargs)
