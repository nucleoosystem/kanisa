from django.views.generic.base import TemplateView
from kanisa.models import Document
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaListView)


class MembersBaseView(KanisaAuthorizationMixin):
    def authorization_check(self, user):
        return user.is_active


class MembersIndexView(MembersBaseView, TemplateView):
    template_name = 'kanisa/members/index.html'
index = MembersIndexView.as_view()


class MembersDocumentView(MembersBaseView, KanisaListView):
    template_name = 'kanisa/members/documents.html'
    kanisa_title = 'Documents'
    model = Document

documents = MembersDocumentView.as_view()
