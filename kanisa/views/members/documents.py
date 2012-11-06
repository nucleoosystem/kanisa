from kanisa.models import Document
from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import KanisaListView


class MembersDocumentView(MembersBaseView, KanisaListView):
    template_name = 'kanisa/members/documents.html'
    kanisa_title = 'Documents'
    model = Document
index = MembersDocumentView.as_view()
