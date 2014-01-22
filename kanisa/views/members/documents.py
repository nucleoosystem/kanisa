from django.core.urlresolvers import reverse_lazy
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from kanisa.models import Document
from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import KanisaListView


class MembersDocumentView(MembersBaseView, KanisaListView):
    template_name = 'kanisa/members/documents.html'
    kanisa_title = 'Documents'
    model = Document
    kanisa_root_crumb = {'text': 'Documents',
                         'url': reverse_lazy('kanisa_members_documents')}
    kanisa_is_root_view = True
    paginate_by = 10
index = MembersDocumentView.as_view()


class MembersDocumentDownloadView(MembersBaseView, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        document = get_object_or_404(Document, pk=int(kwargs['document_pk']))

        document.downloads = F('downloads') + 1
        document.save()

        return document.file.url
download = MembersDocumentDownloadView.as_view()
