from django.views.generic.base import TemplateView
from kanisa.models import Document
from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import KanisaListView


class MembersIndexView(MembersBaseView, TemplateView):
    template_name = 'kanisa/members/index.html'
index = MembersIndexView.as_view()


class MembersDocumentView(MembersBaseView, KanisaListView):
    template_name = 'kanisa/members/documents.html'
    kanisa_title = 'Documents'
    model = Document

documents = MembersDocumentView.as_view()
