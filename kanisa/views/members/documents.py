from django.core.urlresolvers import reverse_lazy
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from kanisa.models import Document
from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import KanisaListView


class MembersDocumentView(MembersBaseView, KanisaListView):
    kanisa_title = 'Documents'
    kanisa_root_crumb = {'text': 'Documents',
                         'url': reverse_lazy('kanisa_members_documents')}
    kanisa_is_root_view = True

    def get_context_data(self, *args, **kwargs):
        ctx = super(MembersDocumentView, self).get_context_data(
            *args, **kwargs
        )

        ctx['title_filter'] = self.request.GET.get('title', '')

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
            return 'kanisa/members/_document_table.html'
        else:
            return 'kanisa/members/documents.html'
index = MembersDocumentView.as_view()


class MembersDocumentDownloadView(MembersBaseView, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        document = get_object_or_404(Document, pk=int(kwargs['document_pk']))

        document.downloads = F('downloads') + 1
        document.save()

        return document.file.url
download = MembersDocumentDownloadView.as_view()
