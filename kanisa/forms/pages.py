from kanisa.forms import KanisaBaseForm
from kanisa.widgets import EpicWidget
from kanisa.models import Page


class PageForm(KanisaBaseForm):
    class Meta:
        model = Page
        widgets = {'contents': EpicWidget(), }
