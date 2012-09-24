from kanisa.forms import KanisaBaseForm
from kanisa.models import Page


class PageForm(KanisaBaseForm):
    class Meta:
        model = Page
