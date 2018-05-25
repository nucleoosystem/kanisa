from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from kanisa.forms.documents import DocumentForm, DocumentFormSimple
from kanisa.models import Document
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaDeleteView)


class DocumentBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Storing documents on your site allows people to have '
                   'easy access to the files they need.')
    kanisa_root_crumb = {'text': 'Documents',
                         'url': reverse_lazy('kanisa_manage_documents')}
    permission = 'kanisa.manage_documents'
    kanisa_nav_component = 'documents'


class DocumentIndexView(DocumentBaseView,
                        KanisaListView):
    model = Document

    kanisa_title = 'Manage Documents'
    kanisa_is_root_view = True

    def get_context_data(self, *args, **kwargs):
        ctx = super(DocumentIndexView, self).get_context_data(
            *args, **kwargs
        )
        title_query = self.request.GET.get('title')

        if title_query:
            ctx['title_filter'] = title_query

        return ctx

    def get_paginate_by(self, queryset):
        title_query = self.request.GET.get('title')
        if title_query:
            return None

        return 50

    def get_queryset(self):
        title_query = self.request.GET.get('title')
        if title_query:
            return Document.objects.filter(
                title__icontains=title_query
            )

        return Document.objects.all()

    def get_template_names(self):
        if self.request.is_ajax():
            return 'kanisa/management/documents/_document_table.html'
        else:
            return 'kanisa/management/documents/index.html'
document_management = DocumentIndexView.as_view()


class DocumentCreateView(DocumentBaseView,
                         KanisaCreateView):
    kanisa_title = 'Upload a Document'
    success_url = reverse_lazy('kanisa_manage_documents')

    def get_form_class(self):
        if self.is_popup():
            return DocumentFormSimple
        return DocumentForm
document_create = DocumentCreateView.as_view()


class DocumentUpdateView(DocumentBaseView,
                         KanisaUpdateView):
    form_class = DocumentForm
    model = Document
    success_url = reverse_lazy('kanisa_manage_documents')
document_update = DocumentUpdateView.as_view()


class DocumentDeleteView(DocumentBaseView,
                         KanisaDeleteView):
    model = Document

    def get_cancel_url(self):
        return reverse('kanisa_manage_documents')

    def get_success_url(self):
        message = '%s deleted.' % self.object
        messages.success(self.request, message)
        return reverse('kanisa_manage_documents')
document_delete = DocumentDeleteView.as_view()


class DocumentExpireView(DocumentBaseView,
                         KanisaDeleteView):
    model = Document

    def get_deletion_confirmation_message(self):
        return 'Are you sure you want to mark %s as expired?' % (
            unicode(self.object)
        )

    def get_kanisa_default_title(self):
        return 'Expire %s' % self.model._meta.verbose_name.title()

    def get_deletion_button_title(self):
        return 'Yes, expire "%s"' % unicode(self.object)

    def get_cancel_url(self):
        return reverse('kanisa_manage_documents')

    def get_success_url(self):
        message = '%s marked expired.' % self.get_object()
        messages.success(self.request, message)
        return reverse('kanisa_manage_documents')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.expired = True
        self.object.save()

        if request.is_ajax():
            return HttpResponse('"%s" marked expired' % self.object)

        return HttpResponseRedirect(self.get_success_url())

document_expire = DocumentExpireView.as_view()
