from django.core.urlresolvers import reverse_lazy
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
index = MembersDocumentView.as_view()
